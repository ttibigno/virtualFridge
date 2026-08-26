import sys
import random
import requests
from values import owners, products, incorrectCategoryIds, incorrectNames, incorrectOwners, incorrectItemIds, incorrectExpiresIn

unopenedItemPool = []
openedItemPool = []

def getItem(correct: bool):
    if (correct == True):
        params = {}
        if random.choice([True, False]):
            params["ownedBy"] = random.choice(owners)
        if random.choice([True, False]):
            params["expiresIn"] = random.randint(0, 30)
        requests.get(f"http://backend:8000/api/v1/fridge", params=params)
    else:
        params = {}
        if random.choice([True, False]):
            params["ownedBy"] = random.choice(incorrectOwners)
        if random.choice([True, False]):
            params["expiresIn"] = random.choice(incorrectExpiresIn)
        if not params:
            params["ownedBy"] = random.choice(incorrectOwners)
        requests.get(f"http://backend:8000/api/v1/fridge", params=params)

def postItem(correct: bool):
    if (correct == True):
        itemNames = random.choice(list(products.keys()))
        data = {
            "name": itemNames,
            "ownedBy": random.choice(owners),
            "categoryId": products[itemNames]
        }
        response = requests.post("http://backend:8000/api/v1/fridge", json=data)
        unopenedItemPool.append(response.json()["id"])
    else:
        data = {
            "name": random.choice(incorrectNames),
            "ownedBy": random.choice(incorrectOwners),
            "categoryId": random.choice(incorrectCategoryIds)
        }
        requests.post("http://backend:8000/api/v1/fridge", json=data)

def openItem(correct: bool):
    if (correct == True):
        itemId = random.choice(unopenedItemPool)
        requests.patch(f"http://backend:8000/api/v1/fridge/{itemId}")
        unopenedItemPool.remove(itemId)
        openedItemPool.append(itemId)
    else:
        if openedItemPool and random.choice([True, False]):
            itemId = random.choice(openedItemPool)
        else:
            itemId = random.choice(incorrectItemIds)
        requests.patch(f"http://backend:8000/api/v1/fridge/{itemId}")

def deleteItem(correct: bool):
    if (correct == True):
        if not unopenedItemPool and not openedItemPool:
            return
        itemId = random.choice(unopenedItemPool + openedItemPool)
        requests.delete(f"http://backend:8000/api/v1/fridge/{itemId}")
        if itemId in openedItemPool:
            openedItemPool.remove(itemId)
        else:
            unopenedItemPool.remove(itemId)
    else:
        itemId = random.choice(incorrectItemIds)
        requests.delete(f"http://backend:8000/api/v1/fridge/{itemId}")
    
def callRequests(correct: bool):
    requestList = [getItem, postItem]
    if unopenedItemPool:
        requestList.append(openItem)
    if unopenedItemPool or openedItemPool:
        requestList.append(deleteItem)
    request = random.choice(requestList)
    request(correct)

n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
errorRate = int(sys.argv[2]) if len(sys.argv) > 2 else 0

errors = int(n*errorRate / 100)

requestsTypes = [True] * (n - errors) + [False] * errors
random.shuffle(requestsTypes)

for condition in requestsTypes:
    callRequests(condition)
