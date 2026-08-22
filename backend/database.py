from classes.Category import Category
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from classes.Item import Base

#https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
engine = create_engine("postgresql+psycopg://postgres:password@postgres/backend_db",
    pool_recycle=3600,
    echo=True)

def database_session():
    with Session(engine) as session:
        yield session

def get_categories():
    return [
        Category(id = 1, name = "Meat", shelfLife = 0, openedLife = 0),
        Category(id = 2, name = "Cooked/Cured Meat", shelfLife = 0, openedLife = 0),
        Category(id = 3, name = "Fish", shelfLife = 0, openedLife = 0),
        Category(id = 4, name = "Cooked/Smoked Fish", shelfLife = 0, openedLife = 0),
        Category(id = 5, name = "Egg", shelfLife = 0, openedLife = 0),
        Category(id = 6, name = "Dairy", shelfLife = 0, openedLife = 0),
        Category(id = 7, name = "Butter", shelfLife = 0, openedLife = 0),
        Category(id = 8, name = "Vegetable", shelfLife = 0, openedLife = 0),
        Category(id = 9, name = "Fruit", shelfLife = 0, openedLife = 0),
        Category(id = 10, name = "Fresh Pasta", shelfLife = 0, openedLife = 0),
        Category(id = 11, name = "Baked Good", shelfLife = 0, openedLife = 0),
        Category(id = 12, name = "Fresh Drink", shelfLife = 0, openedLife = 0),
        Category(id = 13, name = "Pasturized Drink", shelfLife = 0, openedLife = 0),
        Category(id = 14, name = "Sauce/Canned Good", shelfLife = 0, openedLife = 0),
        Category(id = 15, name = "Leftover/Other", shelfLife = 0, openedLife = 0),
    ]

def init_categories():
    with Session(engine) as session:
        if session.query(Category).count() > 0:
            return
        session.add_all(get_categories())
        session.commit()