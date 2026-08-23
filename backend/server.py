from fastapi import FastAPI
from routers.fridge import fridgeRouter as fr
from tables.Base import Base
from tables.Category import Category
from tables.Item import Item
from database import engine, init_categories

app = FastAPI()
app.include_router(fr)

Base.metadata.create_all(engine)
init_categories()