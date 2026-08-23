from tables.Category import Category
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from tables.Item import Base

#https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
engine = create_engine("postgresql+psycopg://postgres:password@postgres/backend_db",
    pool_recycle=3600,
    echo=True)

def database_session():
    with Session(engine) as session:
        yield session

def get_categories():
    return [
        Category(id = 1, name = "Meat", shelfLife = 3, openedLife = 1),
        Category(id = 2, name = "Cured Meat", shelfLife = 25, openedLife = 5),
        Category(id = 3, name = "Fish", shelfLife = 2, openedLife = 1),
        Category(id = 4, name = "Smoked Fish", shelfLife = 10, openedLife = 3),
        Category(id = 5, name = "Egg", shelfLife = 20, openedLife = 20),
        Category(id = 6, name = "Dairy", shelfLife = 14, openedLife = 3),
        Category(id = 7, name = "Butter", shelfLife = 30, openedLife = 30),
        Category(id = 8, name = "Vegetable", shelfLife = 7, openedLife = 7),
        Category(id = 9, name = "Fruit", shelfLife = 7, openedLife = 7),
        Category(id = 10, name = "Fresh Pasta", shelfLife = 3, openedLife = 1),
        Category(id = 11, name = "Baked Good", shelfLife = 3, openedLife = 2),
        Category(id = 12, name = "Fresh Drink", shelfLife = 5, openedLife = 2),
        Category(id = 13, name = "Packaged Drink", shelfLife = 14, openedLife = 5),
        Category(id = 14, name = "Condiment", shelfLife = 365, openedLife = 90),
        Category(id = 15, name = "Bottled/Canned Sauce", shelfLife = 365, openedLife = 5),
        Category(id = 16, name = "Canned Food", shelfLife = 730, openedLife = 4),
        Category(id = 17, name = "Pickled Food", shelfLife = 365, openedLife = 15),
        Category(id = 18, name = "Leftover/Other", shelfLife = 3, openedLife = 3)
    ]

def init_categories():
    with Session(engine) as session:
        if session.query(Category).count() > 0:
            return
        session.add_all(get_categories())
        session.commit()