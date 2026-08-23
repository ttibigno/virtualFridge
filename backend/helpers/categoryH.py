from tables.Category import Category
from tables.Item import Item
from schemas.Item import Unit
from sqlalchemy.orm import Session
from helpers.timeH import now, today, calcDate

def fixItemH(item: Item, session: Session):
    if (item.amount is None):
        item.amount = 1
    if (item.unit is None):
        item.unit = Unit.piece
    if (item.expDate is None):
        category = session.query(Category).filter(Category.id == item.categoryId).one()
        item.expDate = calcDate(today(), category.shelfLife)
    return item

def openItemH(item: Item, session: Session):
    item.openedAt = now()
    category = session.query(Category).filter(Category.id == item.categoryId).one()
    newExpDate = calcDate(item.openedAt.date(), category.openedLife)
    item.expDate = min(item.expDate, newExpDate)
