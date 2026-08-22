from fastapi import FastAPI, APIRouter
from routers.fridge import fridgeRouter as fr
from classes.Base import Base
from classes.Category import Category
from classes.Item import Item
from database import engine, init_categories

Base.metadata.create_all(engine)
init_categories()

app = FastAPI()
app.include_router(fr)