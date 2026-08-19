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