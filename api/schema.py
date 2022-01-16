"""Definitions for all the custom objects used in the backend"""

import datetime

from pydantic import BaseModel


class Item(BaseModel):
    """Custom object for each unique item in the inventory."""

    product_id: str
    name: str
    description: str
    unit_cost: float
    unit_weight: float
    stock: int
    last_change: datetime.datetime
