from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from classes.Item import Item
from database import database_session
from schemas.Item import ItemPost

fridgeRouter = APIRouter(prefix="/fridge")

@fridgeRouter.get("")
async def getFridge(
                    ownedBy: str | None = None,
                    database: Session = Depends(database_session)
                    ):
    if ownedBy is None:
        return database.query(Item).all()
    
    return database.query(Item).filter(Item.ownedBy == ownedBy).all()

@fridgeRouter.post("")
async def postFridge(
                    data: ItemPost,
                    database: Session = Depends(database_session)
                    ):
        item = Item(
            name = data.name,
            ownedBy = data.ownedBy,
            categoryId = data.categoryId,
            amount = data.amount,
            unit = data.unit,
            expDate = data.expDate
        )
    
        database.add(item)
        database.commit()
        database.refresh(item)
    
        return item