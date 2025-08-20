import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any, Optional
import re
from datetime import datetime, timedelta

from shared.models.flight import Flight


class FlightsService:
    """Service for fetching and parsing flight data from Azair."""
    
    # Constants
    DEFAULT_PRICE_LIMIT = 300
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
    BASE_URL_TEMPLATE = (
        "https://www.azair.eu/azfin.php?tp=0&searchtype=flexi&"
        "srcAirport=Katowice+%5BKTW%5D+%28%2BKRK%2COSR%2CLCJ%2CWRO%29&"
        "srcTypedText=&srcFreeTypedText=&srcMC=&srcap0=KRK&srcap1=OSR&"
        "srcap2=LCJ&srcap3=WRO&srcFreeAirport=&"
        "dstAirport=Gdziekolwiek+%5BXXX%5D&dstTypedText=gdziek&"
        "dstFreeTypedText=&dstMC=&adults=2&children=3&infants=0&"
        "minHourStay=0%3A45&maxHourStay=23%3A20&"
        "minHourOutbound=17%3A00&maxHourOutbound=24%3A00&"
        "minHourInbound=20%3A00&maxHourInbound=24%3A00&"
        "depdate={depdate}&arrdate={arrdate}&"
        "minDaysStay=4&maxDaysStay=5&nextday=0&autoprice=true&"
        "currency=PLN&wizzxclub=false&flyoneclub=false&"
        "blueairbenefits=false&megavolotea=false&schengen=false&"
        "transfer=false&samedep=true&samearr=true&dep0=false&"
        "dep1=false&dep2=false&dep3=true&dep4=true&dep5=false&"
        "dep6=false&arr0=true&arr1=false&arr2=false&arr3=false&"
        "arr4=false&arr5=false&arr6=true&maxChng=2&"
        "isOneway=return&resultSubmit=Szukaj"
    )
    
    def __init__(self, price_limit: float = DEFAULT_PRICE_LIMIT):
        """Initialize the FlightsService with optional price limit."""
        self.url = self._generate_url()
        self.headers = {"User-Agent": self.USER_AGENT}
        self.price_limit = price_limit
    
    def _generate_url(self) -> str:
        """Generate URL with current date and current date + 3 months."""
        today = datetime.now()
        three_months_later = today + timedelta(days=90)  # Approximately 3 months
        
        # Format dates as d.m.yyyy (e.g., 18.8.2025)
        depdate = today.strftime("%-d.%-m.%Y")
        arrdate = three_months_later.strftime("%-d.%-m.%Y")
        
        return self.BASE_URL_TEMPLATE.format(
            depdate=depdate,
            arrdate=arrdate
        )
    
    def _get_date_range(self) -> tuple[str, str]:
        """Get the start and end dates used in the search."""
        today = datetime.now()
        three_months_later = today + timedelta(days=90)
        
        # Format dates as d.m.yyyy
        start_date = today.strftime("%-d.%-m.%Y")
        end_date = three_months_later.strftime("%-d.%-m.%Y")
        
        return start_date, end_date
    
    def getFlights(self) -> Dict[str, Any]:
        try:
            # Get the date information
            start_date, end_date = self._get_date_range()
            
            response = requests.get(self.url, headers=self.headers)
            
            if response.status_code == 200:
                flights = self._parse_flights(response.text)
                filtered_flights = self._filter_flights_by_price(flights)
                return {
                    "status": response.status_code,
                    "message": "Success",
                    "flights": filtered_flights,
                    "startDate": start_date,
                    "endDate": end_date,
                    "url": self.url
                }
            else:
                return {
                    "status": response.status_code,
                    "message": "Failed to fetch flights data",
                    "flights": [],
                    "startDate": start_date,
                    "endDate": end_date,
                    "url": self.url
                }
        except Exception as e:
            # Get dates even in error case
            start_date, end_date = self._get_date_range()
            return {
                "status": 500,
                "message": f"Error: {str(e)}",
                "flights": [],
                "startDate": start_date,
                "endDate": end_date,
                "url": self.url
            }
    
    def _parse_flights(self, html_content: str) -> List[Flight]:
        """Parse HTML content and return a list of Flight objects."""
        soup = BeautifulSoup(html_content, 'html.parser')
        flights = []
        
        result_divs = soup.find_all('div', class_='result')
        
        for result_div in result_divs:
            try:
                flight = self._parse_single_flight(result_div)
                if flight:
                    flights.append(flight)
            except Exception:
                # Skip flights that fail to parse
                continue
        
        return flights
    
    def _parse_single_flight(self, result_div: Tag) -> Optional[Flight]:
        """Parse a single flight result div into a Flight object."""
        # Find departure and return paragraphs
        depart_p = result_div.find("span", class_="caption tam")
        return_p = result_div.find("span", class_="caption sem")
        
        if not depart_p or not return_p:
            return None
            
        depart_p = depart_p.find_parent("p")
        return_p = return_p.find_parent("p")
        
        if not depart_p or not return_p:
            return None
        
        # Extract journey information
        start = self._extract_journey_info(depart_p)
        return_flight = self._extract_journey_info(return_p)
        
        # Extract price information
        price_text, price = self._extract_price_info(result_div)
        
        return Flight(
            start=start,
            return_flight=return_flight,
            priceText=price_text,
            price=price
        )
    
    def _extract_journey_info(self, paragraph: Tag) -> str:
        """Extract journey information from a paragraph element."""
        date = self._extract_date(paragraph)
        start_info = self._extract_location_info(paragraph, "from")
        stop_info = self._extract_location_info(paragraph, "to")
        
        return f"{date} {start_info} → {stop_info}"
    
    def _extract_date(self, paragraph: Tag) -> str:
        """Extract date from paragraph."""
        date_span = paragraph.find("span", class_="date")
        if date_span:
            return date_span.get_text(strip=True).replace("\xa0", " ")
        return ""
    
    def _extract_location_info(self, paragraph: Tag, location_type: str) -> str:
        """Extract location information (time, city, airport code)."""
        span = paragraph.find("span", class_=location_type)
        if not span:
            return ""
        
        # Extract time
        time = self._extract_time(span)
        
        # Extract airport code (direct text content only)
        code = self._extract_airport_code(span)
        
        # Extract city name (clean, without nested elements)
        city = self._extract_city_name(span, time)
        
        return f"{time} {city} ({code})"
    
    def _extract_time(self, span: Tag) -> str:
        """Extract time from location span."""
        time_elem = span.find("strong")
        if time_elem:
            return time_elem.get_text(strip=True)
        
        # Fallback: get first word as time
        text = span.get_text(strip=True)
        return text.split()[0] if text else ""
    
    def _extract_airport_code(self, span: Tag) -> str:
        """Extract airport code from location span."""
        code_span = span.find("span", class_="code")
        if code_span and code_span.contents:
            # Get only direct text content, excluding nested elements
            return code_span.contents[0].strip()
        return ""
    
    def _extract_city_name(self, span: Tag, time_to_remove: str) -> str:
        """Extract clean city name from location span."""
        # Create a copy and remove the code span to get clean city name
        span_copy = BeautifulSoup(str(span), 'html.parser').find("span")
        
        # Remove the entire code span from the copy
        code_span_in_copy = span_copy.find("span", class_="code")
        if code_span_in_copy:
            code_span_in_copy.decompose()
        
        # Get clean text and remove time
        city = span_copy.get_text(strip=True).replace(time_to_remove, "").strip()
        return city
    
    def _extract_price_info(self, result_div: Tag) -> tuple[str, float]:
        """Extract price information from result div."""
        price_span = result_div.find('span', class_='tp')
        
        if not price_span:
            return "0", 0.0
        
        price_text = price_span.get_text(strip=True)
        
        # Extract numeric price using regex
        price_match = re.search(r'([\d,]+\.?\d*)', price_text)
        if price_match:
            price_str = price_match.group(1).replace(',', '.')
            try:
                price = float(price_str)
            except ValueError:
                price = 0.0
        else:
            price = 0.0
        
        return price_text, price
    
    def _filter_flights_by_price(self, flights: List[Flight]) -> List[Dict[str, Any]]:
        filtered_flights = [
            flight.model_dump()
            for flight in flights
            if flight.price < self.price_limit
        ]
        return filtered_flights