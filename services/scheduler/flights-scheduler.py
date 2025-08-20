#!/usr/bin/env python3
"""
Flights scheduler script for Railway cron service.
This script handles scheduled flight price monitoring tasks.
"""
import sys
import os
from datetime import datetime

# Add local services to path
sys.path.insert(0, os.path.dirname(__file__))

from services.azair_scraper import FlightsService


def main():
    """Main function that executes the scheduled flight monitoring job."""
    print("=== Flights Scheduler Job Started ===")
    print(f"Timestamp: {datetime.now().isoformat()}")

    try:
        # Initialize flights service
        flights_service = FlightsService()
        
        print("Fetching flight data...")
        
        # Get flights data
        flights_data = flights_service.getFlights()
        
        print(f"Status: {flights_data.get('status')}")
        print(f"Message: {flights_data.get('message')}")
        print(f"Date Range: {flights_data.get('startDate')} - {flights_data.get('endDate')}")
        
        flights = flights_data.get('flights', [])
        print(f"Found {len(flights)} flights")
        
        if flights:
            print("\n--- Flight Results ---")
            for i, flight in enumerate(flights[:5], 1):  # Show first 5 flights
                print(f"\n{i}. {flight.get('start', 'N/A')}")
                print(f"   Return: {flight.get('return_flight', 'N/A')}")
                print(f"   Price: {flight.get('priceText', 'N/A')}")
            
            if len(flights) > 5:
                print(f"\n... and {len(flights) - 5} more flights")
        else:
            print("No flights found.")
        
        print(f"\nSource URL: {flights_data.get('url', 'N/A')}")
        print("Flight monitoring task executed successfully")
        print("=== Flights Scheduler Job Completed ===")

    except Exception as e:
        print(f"Error in flights scheduler: {e}")
        print("=== Flights Scheduler Job Failed ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
