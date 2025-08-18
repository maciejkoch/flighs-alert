from typing import Optional
from pydantic import BaseModel


class Flight(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: str
    total_price: float
    currency: str = "PLN"
