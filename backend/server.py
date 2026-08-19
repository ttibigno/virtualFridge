from fastapi import FastAPI, APIRouter
from routers.fridge import fridgeRouter as fr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

#https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
engine = create_engine("postgresql+psycopg://postgresql:password@localhost/postgresql")

app = FastAPI()

app.include_router(fr)

#with Session(engine) as session:
#    session.commit()