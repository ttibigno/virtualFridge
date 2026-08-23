from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from tables.Base import Base

class Category(Base):
    __tablename__ = "category"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(20))
    shelfLife: Mapped[int] = mapped_column()
    openedLife: Mapped[int | None] = mapped_column()
