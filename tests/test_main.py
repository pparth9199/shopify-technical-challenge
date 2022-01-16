import os
import sqlite3

import pytest
from fastapi.testclient import TestClient

from api.main import app

DB_PATH = "tests/test_inventory.db"

client = TestClient(app)

# Start of SQL DB Setup
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE inventory (product_id text, name text, description text,
    unit_cost real, unit_weight real, stock integer, last_change text)"""
)

conn.commit()
conn.close()
# End of SQL DB Setup


@pytest.mark.order(1)
def test_add_item():
    response = client.put(
        "/add-item",
        json={
            "product_id": "a",
            "name": "b",
            "description": "c",
            "unit_cost": 0.0,
            "unit_weight": 1.0,
            "stock": 2,
            "last_change": "2000-01-01T12:00:00",
        },
    )
    assert response.status_code == 200
    assert response.json() is True


@pytest.mark.order(2)
def test_add_duplicate_item():
    response = client.put(
        "/add-item",
        json={
            "product_id": "a",
            "name": "b",
            "description": "c",
            "unit_cost": 0.0,
            "unit_weight": 1.0,
            "stock": 2,
            "last_change": "2000-01-01T12:00:00",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Inventory with that Product ID already exists."
    }


@pytest.mark.order(3)
def test_get_inventory():
    response = client.get("/get-inventory")
    assert response.status_code == 200
    assert response.json() == [
        {
            "product_id": "a",
            "name": "b",
            "description": "c",
            "unit_cost": 0.0,
            "unit_weight": 1.0,
            "stock": 2,
            "last_change": "2000-01-01T12:00:00",
        }
    ]


@pytest.mark.order(4)
def test_get_filtered_inventory():
    client.put(
        "/add-item",
        json={
            "product_id": "c",
            "name": "b",
            "description": "c",
            "unit_cost": 0.0,
            "unit_weight": 1.0,
            "stock": 0,
            "last_change": "2000-01-01T12:00:00",
        },
    )

    response = client.get(
        "/get-filtered-inventory",
        params={
            "in_stock": True,
            "min_cost": 0.0,
            "max_cost": 10.0,
            "min_weight": 0.0,
            "max_weight": 10.0,
        },
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "product_id": "a",
            "name": "b",
            "description": "c",
            "unit_cost": 0.0,
            "unit_weight": 1.0,
            "stock": 2,
            "last_change": "2000-01-01T12:00:00",
        }
    ]


@pytest.mark.order(5)
def test_update_inventory():
    response = client.put(
        "/update-inventory",
        json={
            "product_id": "a",
            "name": "d",
            "description": "b",
            "unit_cost": 1.0,
            "unit_weight": 1.5,
            "stock": 5,
            "last_change": "2020-01-01T12:00:00",
        },
    )
    assert response.status_code == 200
    assert response.json() is True


@pytest.mark.order(6)
def test_invalid_update_inventory():
    response = client.put(
        "/update-inventory",
        json={
            "product_id": "b",
            "name": "d",
            "description": "b",
            "unit_cost": 1.0,
            "unit_weight": 1.5,
            "stock": 5,
            "last_change": "2020-01-01T12:00:00",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Inventory Item does not exist."}


@pytest.mark.order(7)
def test_get_item():
    response = client.get("/get-item/a")
    assert response.status_code == 200
    assert response.json() == [
        {
            "product_id": "a",
            "name": "d",
            "description": "b",
            "unit_cost": 1.0,
            "unit_weight": 1.5,
            "stock": 5,
            "last_change": "2020-01-01T12:00:00",
        }
    ]


@pytest.mark.order(8)
def test_get_invalid_item():
    response = client.get("/get-item/b")
    assert response.status_code == 404
    assert response.json() == {"detail": "Inventory Item does not exist."}


@pytest.mark.order(9)
def test_remove_item():
    response = client.delete("/remove-item/a")
    assert response.status_code == 200
    assert response.json() is True


@pytest.mark.order(10)
def test_invalid_remove_item():
    response = client.delete("/remove-item/a")
    assert response.status_code == 404
    assert response.json() == {"detail": "Inventory Product ID does not exist."}
