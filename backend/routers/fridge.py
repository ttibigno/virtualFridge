from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from classes.Item import Item
from database import database_session
from schemas.Item import ItemPost

fridgeRouter = APIRouter(prefix="/fridge")

@fridgeRouter.get("")
async def getFridge(database: Session = Depends(database_session)):
    itemList = database.query(Item).all()
    return itemList

@fridgeRouter.post("")
async def postFridge(
                    data: ItemPost,
                    database: Session = Depends(database_session)
                    ):
        item = Item(
            name=data.name,
            ownedBy=data.ownedBy
        )
    
        database.add(item)
        database.commit()
        database.refresh(item)
    
        return item
