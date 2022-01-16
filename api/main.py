"""Inventory System Backend"""

import sqlite3
import sys
from typing import List

from fastapi import FastAPI, HTTPException, Path, status

from api.schema import Item

app = FastAPI()

# Switch to the test database for tests so the normal inventory is untouched
DB_PATH = "tests/test_inventory.db" if "pytest" in sys.modules else "inventory.db"


@app.get("/get-inventory", response_model=List[Item])
def get_inventory():
    """GET request for retrieving the total inventory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")

    total_inventory = cursor.fetchall()

    conn.close()

    return total_inventory


@app.get("/get-filtered-inventory", response_model=List[Item])
def get_filtered_inventory(
    in_stock: bool,
    min_cost: float,
    max_cost: float,
    min_weight: float,
    max_weight: float,
):
    """GET request for retrieving filtered inventory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    inventory_filter = (
        1 if in_stock else 0,
        min_cost,
        max_cost,
        min_weight,
        max_weight,
    )

    cursor.execute(
        """SELECT * FROM inventory WHERE stock>=? AND unit_cost>=? AND unit_cost<=?
        AND unit_weight>=? AND unit_weight<=?""",
        inventory_filter,
    )

    filtered_inventory = cursor.fetchall()

    conn.commit()
    conn.close()

    return filtered_inventory


@app.get("/get-item/{product_id}", response_model=List[Item])
def get_item(
    product_id: str = Path(
        ..., title="The Product ID of the inventory item to retrieve"
    )
):
    """GET request for retrieving info on a single item."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory WHERE product_id=?", (product_id,))

    item = cursor.fetchall()

    conn.close()

    if len(item) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory Item does not exist.",
        )

    return item


@app.put("/add-item", response_model=bool)
def add_item(item: Item):
    """PUT request for adding a new item to the inventory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    new_item = (
        item.product_id,
        item.name,
        item.description,
        item.unit_cost,
        item.unit_weight,
        item.stock,
        item.last_change,
    )

    cursor.execute(
        "SELECT product_id FROM inventory WHERE product_id=?", (item.product_id,)
    )

    if len(cursor.fetchall()) > 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inventory with that Product ID already exists.",
        )

    cursor.execute("INSERT INTO inventory VALUES (?,?,?,?,?,?,?)", new_item)
    conn.commit()
    conn.close()

    return True


@app.put("/update-inventory", response_model=bool)
def update_inventory(item: Item):
    """PUT request for updating an existing item in the inventory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    updated_item = (
        item.product_id,
        item.name,
        item.description,
        item.unit_cost,
        item.unit_weight,
        item.stock,
        item.last_change,
    )

    cursor.execute(
        "SELECT product_id FROM inventory WHERE product_id=?", (item.product_id,)
    )

    if len(cursor.fetchall()) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory Item does not exist.",
        )

    cursor.execute("DELETE FROM inventory WHERE product_id=?", (item.product_id,))
    cursor.execute("INSERT INTO inventory VALUES (?,?,?,?,?,?,?)", updated_item)
    conn.commit()
    conn.close()

    return True


@app.delete("/remove-item/{product_id}", response_model=bool)
def remove_item(
    product_id: str = Path(..., title="The Product ID of the inventory item to delete")
):
    """DELETE request for removing an item from the inventory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT product_id FROM inventory WHERE product_id=?", (product_id,))

    if len(cursor.fetchall()) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory Product ID does not exist.",
        )

    cursor.execute("DELETE FROM inventory WHERE product_id=?", (product_id,))

    conn.commit()
    conn.close()

    return True
