from django.core.management.base import BaseCommand
from django.utils import timezone
from briansclub.models import Billing
import json
import hmac
import hashlib
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Command(BaseCommand):
    help = 'Check billing status and perform actions'

    def handle(self, *args, **options):
        self.stdout.write("Checking billing status...")
        # Iterate through Billing objects with status 'pending'
        pending_orders = Billing.objects.filter(status='pending')
        for order in pending_orders:
            self.stdout.write(f"Processing order {order.order_number}...")
            # Fetch HTML content from the Plisio invoice URL
            invoice_html = self.fetch_invoice_html(order.details)
            if invoice_html is not None:
                # Check if payment completed in the invoice HTML
                if self.payment_completed(invoice_html):
                    self.stdout.write("Payment completed for order. Updating balance and removing billing...")
                    # Update balance and remove billing entry
                    self.update_balance_and_remove_billing(order)
                else:
                    self.stdout.write("Payment not completed for order. Rechecking other orders...")
            else:
                self.stderr.write("Failed to fetch invoice HTML content.")

    def fetch_invoice_html(self, url):
        try:
            # Fetch HTML content from the URL
            session = HTMLSession()
            response = session.get(url)
            response.html.render(timeout=30)
            print('response',response)# Increase timeout to 30 seconds
            if response.status_code == 200:
                return response.html.html  # Return HTML content
            else:
                self.stderr.write(f"Failed to fetch HTML content. Status code: {response.status_code}")
                return None
        except Exception as e:
            self.stderr.write(f"Error fetching invoice HTML content: {e}")
            return None

    def payment_completed(self, invoice_html):
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(invoice_html, 'html.parser')
        # Check if the specific element indicating payment completion is present
        return soup.find('div', class_='invoice-title') is not None and soup.find('div', class_='invoice-title').text.strip() == 'Payment completed'

    def update_balance_and_remove_billing(self, order):
        # Perform actions for completed payments
        order.status = 'completed'
        order.date = timezone.now()

        # Your verification logic using the provided code snippet
        data = {
            "status": order.status,
            "order_number": order.order_number,
            "amount": str(order.amount)
        }
        secret_key = "-KJNi4ZYTZa1vsudlJjeH8F2tKFZQnxbRkTU3vn8j4pS5QyWS01to3dqVXDzHEDM"

        sorted_data = sorted(data.items())
        serialized_data = json.dumps(sorted_data, separators=(',', ':'))
        hmac_hash = hmac.new(secret_key.encode(), serialized_data.encode(), hashlib.sha1).hexdigest()

        # Send POST request with updated status and details
        payload = {
            "status": order.status,
            "order_number": order.order_number,
            "amount": str(order.amount),
            "verify_hash": hmac_hash
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post("http://bclub.cc/plisio_callback", json=payload, headers=headers)

        if response.status_code == 200:
            self.stdout.write("POST request successful. Processing response...")
            # Assuming the response contains the updated balance information
            updated_balance = response.json().get('user_balance', {}).get('balance')
            if updated_balance is not None:
                order.user.balance = updated_balance
                order.user.save()

            # Remove the billing entry
            order.delete()
            self.stdout.write(self.style.SUCCESS(f"Balance updated to {updated_balance}%"))
        else:
            self.stderr.write("Failed to update balance and remove billing.")

        return
