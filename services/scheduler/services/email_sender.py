import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging


class EmailSender:
    """Service for sending emails via SMTP."""

    def __init__(self):
        """Initialize EmailSender with config from environment variables."""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', self.email_user)
        self.from_name = os.getenv('FROM_NAME', 'Flights Alert')

        # Validate required environment variables
        if not self.email_user or not self.email_password:
            raise ValueError(
                "EMAIL_USER and EMAIL_PASSWORD environment variables required"
            )
    
    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        text_content: str,
        html_content: Optional[str] = None
    ) -> bool:
        """
        Send an email to the specified recipients.

        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            text_content: Plain text content of the email
            html_content: Optional HTML content of the email

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = ', '.join(to_emails)
            
            # Add plain text part
            text_part = MIMEText(text_content, 'plain')
            message.attach(text_part)
            
            # Add HTML part if provided
            if html_content:
                html_part = MIMEText(html_content, 'html')
                message.attach(html_part)

            # Connect to server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable security
                server.login(self.email_user, self.email_password)
                server.send_message(message)

            logging.info(f"Email sent to {', '.join(to_emails)}")
            return True

        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_flight_alert(
        self,
        to_emails: List[str],
        flights: List[dict],
        date_range: str,
        source_url: Optional[str] = None,
        ai_destination_content: Optional[str] = None
    ) -> bool:
        """
        Send a flight alert email with formatted flight information.

        Args:
            to_emails: List of recipient email addresses
            flights: List of flight dictionaries
            date_range: Date range for the search
            source_url: Optional URL to the flight search results
            ai_destination_content: Optional AI-generated destination 
                descriptions

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not flights:
            return True  # No flights to report

        subject = f"✈️ Flight Alert: {len(flights)} flights found"

        # Create text content
        text_content = f"""Flight Alert - {date_range}

Found {len(flights)} flights:

"""

        for i, flight in enumerate(flights[:10], 1):  # Limit to 10 flights
            text_content += f"{i}. {flight.start}\n"
            text_content += f"   Return: {flight.return_flight}\n"
            text_content += f"   Price: {flight.priceText}\n\n"

        if len(flights) > 10:
            text_content += f"... and {len(flights) - 10} more flights\n\n"

        # Add AI destination content if provided
        if ai_destination_content:
            text_content += "🌍 Destination Highlights:\n\n"
            text_content += ai_destination_content + "\n\n"

        text_content += "Happy travels! ✈️\n\n"
        
        # Add source URL if provided
        if source_url:
            text_content += f"🔗 View all results: {source_url}"

        # Create HTML content
        html_content = f"""<html><body>
<h2>✈️ Flight Alert - {date_range}</h2>
<p>Found <strong>{len(flights)}</strong> flights:</p>
<div style="margin: 20px 0;">"""

        for i, flight in enumerate(flights[:10], 1):
            start = flight.start
            return_flight = flight.return_flight
            price = flight.priceText
            html_content += f"""<div style="border: 1px solid #ddd;
padding: 15px; margin: 10px 0; border-radius: 5px;">
<h3 style="color: #2c3e50; margin: 0 0 10px 0;">{i}. Flight Deal</h3>
<p style="margin: 5px 0;"><strong>Departure:</strong> {start}</p>
<p style="margin: 5px 0;"><strong>Return:</strong> {return_flight}</p>
<p style="margin: 5px 0; color: #e74c3c; font-weight: bold;">
<strong>Price:</strong> {price}</p></div>"""

        if len(flights) > 10:
            extra = len(flights) - 10
            html_content += f"<p><em>... and {extra} more flights</em></p>"

        html_content += "</div>"
        
        # Add AI destination content if provided
        if ai_destination_content:
            html_content += """
<div style="margin: 25px 0; padding: 20px; background-color: #f8f9fa;
border-left: 4px solid #17a2b8; border-radius: 5px;">
<h3 style="color: #17a2b8; margin: 0 0 15px 0;">🌍 Destination Highlights</h3>
<div style="line-height: 1.6; color: #495057;">"""
            
            # Convert plain text to HTML with proper line breaks
            for line in ai_destination_content.split('\n'):
                if line.strip():
                    html_content += (
                        f"<p style='margin: 10px 0;'>{line.strip()}</p>"
                    )
            
            html_content += "</div></div>"
        
        # Add source URL if provided
        if source_url:
            html_content += f"""
<div style="margin: 20px 0; text-align: center;">
<a href="{source_url}" style="background-color: #3498db; color: white;
padding: 12px 24px; text-decoration: none; border-radius: 5px;
display: inline-block; font-weight: bold;">
🔗 View All Results on Azair.eu
</a>
</div>"""

        html_content += """
<p style="color: #7f8c8d;">Happy travels! ✈️</p>
</body></html>"""

        return self.send_email(to_emails, subject, text_content, html_content)

    def send_simple_alert(self, to_emails: List[str], message: str) -> bool:
        """
        Send a simple text alert.

        Args:
            to_emails: List of recipient email addresses
            message: Message to send

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = "🔔 Flights Alert Notification"
        return self.send_email(to_emails, subject, message)
