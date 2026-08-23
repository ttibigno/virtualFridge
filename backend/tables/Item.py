from datetime import date, datetime
from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid
from tables.Base import Base


class Item(Base):
    __tablename__ = "item"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30))
    ownedBy: Mapped[str] = mapped_column(String(20))
    categoryId: Mapped[int | None] = mapped_column(ForeignKey("category.id"))
    amount: Mapped[float | None] = mapped_column()
    unit: Mapped[str | None] = mapped_column(String(5))
    expDate: Mapped[date | None] = mapped_column()
    openedAt: Mapped[datetime | None] = mapped_column(nullable = True)
