from pydantic import BaseModel

class ItemPost(BaseModel):
    name: str
    ownedBy: str