from datetime import date
from pydantic import BaseModel, Field
from enum import Enum

class Unit(str, Enum):
    g = "g"
    kg = "kg"
    ml = "ml"
    l = "l"
    piece = "piece"

class ItemPost(BaseModel):
    name: str = Field(min_length=1, max_length = 30)
    ownedBy: str = Field(min_length=1, max_length = 20)
    categoryId: int
    amount: float | None = Field(default=None, ge=0)
    unit: Unit | None = None
    expDate: date | None = None