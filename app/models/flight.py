from pydantic import BaseModel


class Flight(BaseModel):
    start: str
    return_flight: str
    priceText: str
    price: float
