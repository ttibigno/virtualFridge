from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "item"
    
    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    ownedBy: Mapped[str] = mapped_column(String(30))