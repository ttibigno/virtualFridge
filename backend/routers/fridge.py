from fastapi import APIRouter

fridgeRouter = APIRouter(prefix="/fridge")

@fridgeRouter.get("")
async def getFridge():
    return {""}

@fridgeRouter.post("")
async def postFridge():
    return {""}

@fridgeRouter.get("/{name}")
async def getItemsByOwner(name: str):
    return {"name": name}
