from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from classes.Item import Item
from database import database_session
from schemas.Item import ItemPost
from helpers.categoryH import fixItemH, openItemH

fridgeRouter = APIRouter(prefix="/fridge")

@fridgeRouter.get("")
async def getItem(
                    ownedBy: str | None = None,
                    currDbSession: Session = Depends(database_session)
                    ):
    if ownedBy is None:
        return currDbSession.query(Item).all()
    
    return currDbSession.query(Item).filter(Item.ownedBy == ownedBy).all()

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