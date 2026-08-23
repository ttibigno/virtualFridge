from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from tables.Item import Item
from database import database_session
from schemas.Item import ItemPost
from helpers.categoryH import fixItemH, openItemH
from helpers.timeH import calcDate, today

fridgeRouter = APIRouter(prefix="/fridge")

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
async def postItem(
                    data: ItemPost,
                    currDbSession: Session = Depends(database_session)
                    ):
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
    return item

@fridgeRouter.get("/{itemId}")
async def getItemById(
                        itemId: str,
                        currDbSession: Session = Depends(database_session)
                    ):
    return currDbSession.query(Item).filter(Item.id == itemId).one()

@fridgeRouter.patch("/{itemId}")
async def openItem(
                    itemId: str,
                    currDbSession: Session = Depends(database_session)
                    ):
    item = currDbSession.query(Item).filter(Item.id == itemId).one()
    openItemH(item, currDbSession)

    currDbSession.commit()
    currDbSession.refresh(item)
    return item

@fridgeRouter.delete("/{itemId}")
async def deleteItem(
                        itemId: str,
                        currDbSession: Session = Depends(database_session)
                    ):
    item = currDbSession.query(Item).filter(Item.id == itemId).one()
    currDbSession.delete(item)
    currDbSession.refresh(item)
    return item