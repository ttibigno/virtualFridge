from fastapi import FastAPI
from routers.fridge import fridgeRouter as fr
from tables.Base import Base
from tables.Category import Category
from tables.Item import Item
from database import engine, init_categories
from routers.metrics import setup_metrics
from prometheus_client import make_asgi_app

app = FastAPI()
app.include_router(fr)

setup_metrics(app)


Base.metadata.create_all(engine)
init_categories()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)