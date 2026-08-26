from fastapi.testclient import TestClient
from server import app

testApp = TestClient(app)

def testCorrectGet():
    response = testApp.get("/api/v1/fridge")
    assert response.status_code == 200

def testCorrectGetById():
    response = testApp.post("/api/v1/fridge", json={"name": "test", "ownedBy": "testCorrectGetById", "categoryId": 1})
    id = response.json()["id"]
    getResponse = testApp.get(f"/api/v1/fridge/{id}")
    assert getResponse.status_code == 200
    item = getResponse.json()
    assert item["id"] == id
    assert item["name"] == "test"

def testInvalidGetById():
    response = testApp.get("/api/v1/fridge/-----")
    assert response.status_code == 500

def testWrongGetById():
    response = testApp.get("/api/v1/fridge/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 500

def testCorrectGetByOwner():
    testApp.post("/api/v1/fridge", json={"name": "test","ownedBy": "testGetByOwner", "categoryId": 1})
    response = testApp.get("/api/v1/fridge", params={"ownedBy": "testGetByOwner"})
    items = response.json()
    assert all(item["ownedBy"] == "testGetByOwner" for item in items)

def testCorrectGetByExpiresIn():
    response = testApp.get("/api/v1/fridge", params={"expiresIn": 7})
    items = response.json()
    assert isinstance(items, list)

def testCorrectPatch():
    response = testApp.post("/api/v1/fridge", json={"name": "test", "ownedBy": "testCorrectPatch", "categoryId": 1})
    id = response.json()["id"]
    getResponse = testApp.patch(f"/api/v1/fridge/{id}")
    assert getResponse.status_code == 200
    item = getResponse.json()
    assert item["id"] == id
    assert item["openedAt"] is not None

def testPatchNonExistingItem():
    response = testApp.patch(f"/api/v1/fridge/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 500

def testCorrectPost():
    response = testApp.post("/api/v1/fridge", json={"name": "test", "ownedBy": "test", "categoryId": 1})
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "test"
    assert item["ownedBy"] == "test"
    assert item["categoryId"] == 1
    assert "id" in item
    assert item["expDate"] is not None
    assert item["amount"] is not None
    assert item["unit"] is not None

def testCorrectPostAllFields():
    response = testApp.post("/api/v1/fridge", json={"name": "test", "ownedBy": "test", "categoryId": 1, "expDate": "2050-01-01", "amount": "3", "unit": "kg"})
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "test"
    assert item["ownedBy"] == "test"
    assert item["categoryId"] == 1
    assert "id" in item
    assert item["expDate"] == "2050-01-01"
    assert item["amount"] == 3
    assert item["unit"] == "kg"

def testMissingBodyFieldsPost():
    response = testApp.post("/api/v1/fridge", json={"name": "test"})
    assert response.status_code == 422

def testInvalidBodyFieldsPost():
    response = testApp.post("/api/v1/fridge", json={"name": "-------------------------------------------------", "ownedBy": "test", "categoryId": 1})
    assert response.status_code == 422

def testCorrectDelete():
    response = testApp.post("/api/v1/fridge", json={"name": "test", "ownedBy": "testCorrectDelete", "categoryId": 1})
    id = response.json()["id"]
    getResponse = testApp.delete(f"/api/v1/fridge/{id}")
    assert getResponse.status_code == 200

def testDeleteNonExistingItem():
    response = testApp.delete(f"/api/v1/fridge/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 500