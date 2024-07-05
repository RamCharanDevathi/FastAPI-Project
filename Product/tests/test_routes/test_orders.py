import pytest
# from fastapi.testclient import TestClient
from Product.tests.test_database import client
from Product.main import app

# client = TestClient(app)

def test_create_order(client):
    response = client.post(
        "/customers/",
        json={"cust_name": "Charan", "contact_info": "charan@example.com"}
    )
    customer_id = response.json()["id"]
    response = client.post(
        "/orders/",
        json={"customer_id": customer_id, "order_date": "2023-07-05", "status": "Pending"}
    )
    assert response.status_code == 201
    assert response.json()["customer_id"] == customer_id

def test_read_order(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_order(client):
    response = client.get("/orders")
    print(response.json())
    order_id = response.json()[0]["id"]
    response = client.put(
        f"/orders/{order_id}",
        json={"customer_id": response.json()[0]["customer_id"], "order_date": "2023-07-05", "status": "Fulfilled"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Fulfilled"

def test_delete_order(client):
    response = client.get("/orders/")
    order_id = response.json()[0]["id"]
    print(order_id)
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
