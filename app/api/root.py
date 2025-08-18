from fastapi import APIRouter
from app.services.flights import FlightsService

router = APIRouter()
flights_service = FlightsService()

@router.get("/")
def read_root():
    return flights_service.getFlights()
