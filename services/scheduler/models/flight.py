from typing import List
from pydantic import BaseModel


class Flight(BaseModel):
    start: str
    return_flight: str
    priceText: str
    price: float
    destination: str


class FlightData(BaseModel):
    status: int
    message: str
    flights: List[Flight]
    startDate: str
    endDate: str
    url: str