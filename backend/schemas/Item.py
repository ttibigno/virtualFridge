from datetime import date

from pydantic import BaseModel
from enum import Enum

class Unit(str, Enum):
    g = "g"
    kg = "kg"
    ml = "ml"
    l = "l"
    unit = "unit"
    

class ItemPost(BaseModel):
    name: str
    ownedBy: str
    categoryId: str
    amount: float | None = None
    unit: Unit | None = None
    expDate: date | None = None