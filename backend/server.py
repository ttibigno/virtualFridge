from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routers.fridge import fridgeRouter as fr
from routers.category import categoryRouter as cr
from tables.Base import Base
from tables.Category import Category
from tables.Item import Item
from database import engine, init_categories
from middleware.observability import setup_observability
from prometheus_client import make_asgi_app

app = FastAPI()

app.include_router(fr, prefix="/api/v1")
app.include_router(cr, prefix="/api/v1")

setup_observability(app)

Base.metadata.create_all(engine)
init_categories()

metrics_app = make_asgi_app()
app.mount("/metrics/", metrics_app)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")