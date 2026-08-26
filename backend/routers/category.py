from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tables.Category import Category
from database import database_session

categoryRouter = APIRouter(prefix="/categories")

@categoryRouter.get("")
async def getCategories(currDbSession: Session = Depends(database_session)):
    return currDbSession.query(Category).all()
