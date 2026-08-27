from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tables.Item import Item
from database import database_session
from schemas.Item import ItemPost
from helpers.categoryH import fixItemH, openItemH
from helpers.timeH import calcDate, today
from middleware.observability import fridge_additions, things, opened_items
import structlog

structlog.configure(processors = [structlog.processors.TimeStamper(fmt="iso"), structlog.stdlib.add_log_level, structlog.processors.JSONRenderer()])
logger = structlog.getLogger()

fridgeRouter = APIRouter(prefix="/api/v1/fridge")

@fridgeRouter.get("")
async def getItem(
                    ownedBy: str | None = None,
                    expiresIn: int | None = None,
                    currDbSession: Session = Depends(database_session)
                    ):
    query = currDbSession.query(Item)
    if (ownedBy is not None):
        query = query.filter(Item.ownedBy == ownedBy)
    if (expiresIn is not None):
        query = query.filter(Item.expDate <= calcDate(today(), expiresIn), Item.expDate >= today())
    return query.all()

@fridgeRouter.post("")
async def postItem(data: ItemPost, currDbSession: Session = Depends(database_session)):
    item = Item(
        name = data.name,
        ownedBy = data.ownedBy,
        categoryId = data.categoryId,
        amount = data.amount,
        unit = data.unit,
        expDate = data.expDate
    )
    item = fixItemH(item, currDbSession)
    
    currDbSession.add(item)
    currDbSession.commit()
    currDbSession.refresh(item)

    fridge_additions.inc()
    things.inc(item.amount)
    logger.info("itemCreated", itemId = str(item.id), owner = item.ownedBy, categoryId = item.categoryId)
    return item

@fridgeRouter.get("/{itemId}")
async def getItemById(itemId: str, currDbSession: Session = Depends(database_session)):
    return currDbSession.query(Item).filter(Item.id == itemId).one()

@fridgeRouter.patch("/{itemId}")
async def openItem(itemId: str, currDbSession: Session = Depends(database_session)):
    item = currDbSession.query(Item).filter(Item.id == itemId).one()
    if item.openedAt is not None:
            raise HTTPException(status_code=409, detail="Item is already opened")
    openItemH(item, currDbSession)

    currDbSession.commit()
    currDbSession.refresh(item)
    logger.info("itemOpened", itemId = str(item.id), owner = item.ownedBy, categoryId = item.categoryId, openedAt = item.openedAt)
    opened_items.inc()
    return item

@fridgeRouter.delete("/{itemId}")
async def deleteItem(itemId: str, currDbSession: Session = Depends(database_session)):
    item = currDbSession.query(Item).filter(Item.id == itemId).one()

    currDbSession.delete(item)
    currDbSession.commit()
    things.dec(item.amount)
    logger.info("itemDeleted", itemId = str(item.id), owner = item.ownedBy, categoryId = item.categoryId)
    return item
