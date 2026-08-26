import sys
import random
from values import owners, products
import requests

def scan():
    name = random.choice(list(products.keys()))
    data = {
        "name": name,
        "ownedBy": random.choice(owners),
        "categoryId": products[name]
    }
    requests.post("http://backend:8000/api/v1/fridge", json=data)

n = int(sys.argv[1]) if len(sys.argv) > 1 else 50

for _ in range(n):
    scan()
