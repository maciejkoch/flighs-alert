import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from app.models.flight import Flight


class FlightsService:
    def __init__(self):
        self.url = "https://www.azair.eu/azfin.php?tp=0&searchtype=flexi&srcAirport=Katowice+%5BKTW%5D+%28%2BKRK%2COSR%2CLCJ%2CWRO%29&srcTypedText=&srcFreeTypedText=&srcMC=&srcap0=KRK&srcap1=OSR&srcap2=LCJ&srcap3=WRO&srcFreeAirport=&dstAirport=Gdziekolwiek+%5BXXX%5D&dstTypedText=gdziek&dstFreeTypedText=&dstMC=&adults=2&children=3&infants=0&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=17%3A00&maxHourOutbound=24%3A00&minHourInbound=20%3A00&maxHourInbound=24%3A00&depdate=18.8.2025&arrdate=31.12.2025&minDaysStay=4&maxDaysStay=5&nextday=0&autoprice=true&currency=PLN&wizzxclub=false&flyoneclub=false&blueairbenefits=false&megavolotea=false&schengen=false&transfer=false&samedep=true&samearr=true&dep0=false&dep1=false&dep2=false&dep3=true&dep4=true&dep5=false&dep6=false&arr0=true&arr1=false&arr2=false&arr3=false&arr4=false&arr5=false&arr6=true&maxChng=2&isOneway=return&resultSubmit=Szukaj"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.price_limit = 300
    
    def getFlights(self) -> Dict[str, Any]:
        try:
            response = requests.get(self.url, headers=self.headers)
            
            if response.status_code == 200:
                flights = self._parse_flights(response.text)
                filtered_flights = self._filter_flights_by_price(flights)
                return {
                    "status": response.status_code,
                    "message": "Success",
                    "flights": filtered_flights
                }
            else:
                return {
                    "status": response.status_code,
                    "message": "Failed to fetch flights data",
                    "flights": []
                }
        except Exception as e:
            return {
                "status": 500,
                "message": f"Error: {str(e)}",
                "flights": []
            }
    
    def _parse_flights(self, html_content: str) -> List[Flight]:
        flights = []
        return flights
    
    def _filter_flights_by_price(self, flights: List[Flight]) -> List[Dict[str, Any]]:
        filtered_flights = [
            flight.model_dump()
            for flight in flights
            if flight.total_price < self.price_limit
        ]
        return filtered_flights