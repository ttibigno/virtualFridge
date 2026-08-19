from fastapi import FastAPI, APIRouter
from routers.fridge import fridgeRouter as fr
from classes.Item import Item, Base
from database import engine

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(fr)