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
        
        print(f"Status: {flights_data.get('status')}")
        print(f"Message: {flights_data.get('message')}")
        date_range = f"{flights_data.get('startDate')} - {flights_data.get('endDate')}"
        print(f"Date Range: {date_range}")
        
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
            
            # Send email alert if recipients are configured
            recipient_emails = os.getenv('ALERT_EMAILS')
            if recipient_emails and email_sender:
                recipients = [email.strip() for email in recipient_emails.split(',')]
                print(f"\nSending email alert to: {', '.join(recipients)}")
                
                success = email_sender.send_flight_alert(
                    recipients, 
                    flights, 
                    date_range,
                    flights_data.get('url')
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
            
            # Send notification if no flights found (optional)
            recipient_emails = os.getenv('ALERT_EMAILS')
            send_no_flights = os.getenv('SEND_NO_FLIGHTS_ALERT', 'false').lower() == 'true'
            
            if recipient_emails and send_no_flights and email_sender:
                recipients = [email.strip() for email in recipient_emails.split(',')]
                message = f"No flights found for date range: {date_range}"
                email_sender.send_simple_alert(recipients, message)
                print("📧 No-flights notification sent")
        
        print(f"\nSource URL: {flights_data.get('url', 'N/A')}")
        print("Flight monitoring task executed successfully")
        print("=== Flights Scheduler Job Completed ===")

    except Exception as e:
        print(f"Error in flights scheduler: {e}")
        print("=== Flights Scheduler Job Failed ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
