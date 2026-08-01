from fastapi import FastAPI, APIRouter
from routers.fridge import fridgeRouter as fr

app = FastAPI()

app.include_router(fr)