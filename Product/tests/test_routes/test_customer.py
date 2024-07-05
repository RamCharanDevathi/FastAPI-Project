import pytest
from fastapi.testclient import TestClient
from Product.tests.test_database import client
from Product.main import app

# client = TestClient(app)

def test_create_customer(client):
    response = client.post(
        "/customers/",
        json={"cust_name": "Ram", "contact_info": "ram123@gmail.com"}
    )
    assert response.status_code == 201
    assert response.json()["cust_name"] == "Ram"

def test_read_customer(client):
    response = client.get("/customers/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_customer(client):
    response = client.get("/customers/")
    customer_id = response.json()[0]["id"]
    response = client.put(
        f"/customers/{customer_id}",
        json={"cust_name": "Ram", "contact_info": "ram123@gmail.com"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"

def test_delete_customer(client):
    response = client.get("/customers/")
    customer_id = response.json()[0]["id"]
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
