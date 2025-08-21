#!/usr/bin/env python3
"""
Flights scheduler script for Railway cron service.
This script handles scheduled flight price monitoring tasks.
"""
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from services.azair_scraper import FlightsService
from services.email_sender import EmailSender


def main():
    """Main function that executes the scheduled flight monitoring job."""
    print("=== Flights Scheduler Job Started ===")
    print(f"Timestamp: {datetime.now().isoformat()}")

    try:
        # Initialize services
        flights_service = FlightsService()
        
        # Initialize email service only if credentials are available
        email_sender = None
        try:
            if os.getenv('EMAIL_USER') and os.getenv('EMAIL_PASSWORD'):
                email_sender = EmailSender()
                print("📧 Email service initialized")
            else:
                print("📧 Email service disabled (credentials not provided)")
        except Exception as e:
            print(f"⚠️ Email service initialization failed: {e}")
            email_sender = None
        
        print("Fetching flight data...")
        
        # Get flights data
        flights_data = flights_service.getFlights()
        
        print(f"Status: {flights_data.status}")
        print(f"Message: {flights_data.message}")
        date_range = f"{flights_data.startDate} - {flights_data.endDate}"
        print(f"Date Range: {date_range}")
        
        flights = flights_data.flights
        print(f"Found {len(flights)} flights")

        destinations = list(set([flight.destination for flight in flights]))
        print(f"Destinations: {destinations}")
        
        if flights:
            print("\n--- Flight Results ---")
            for i, flight in enumerate(flights[:5], 1):  # Show first 5 flights
                print(f"\n{i}. {flight.start}")
                print(f"   Return: {flight.return_flight}")
                print(f"   Price: {flight.priceText}")
            
            if len(flights) > 5:
                print(f"\n... and {len(flights) - 5} more flights")
            
            # Send email alert if recipients are configured
            recipient_emails = os.getenv('ALERT_EMAILS')
            if recipient_emails and email_sender:
                recipients = [email.strip() for email in recipient_emails.split(',')]
                print(f"\nSending email alert to: {', '.join(recipients)}")
                
                success = email_sender.send_flight_alert(
                    recipients, 
                    flights, 
                    date_range,
                    flights_data.url
                )
                
                if success:
                    print("✅ Email alert sent successfully!")
                else:
                    print("❌ Failed to send email alert")
            elif recipient_emails and not email_sender:
                print("⚠️ Email recipients configured but email service unavailable")
            else:
                print("📧 No email recipients configured (ALERT_EMAILS not set)")
                
        else:
            print("No flights found.")

    except Exception as e:
        print(f"Error in flights scheduler: {e}")
        print("=== Flights Scheduler Job Failed ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
