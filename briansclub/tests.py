from time import timezone
from django.test import TestCase

# Create your tests here.
# tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Billing, Balance
import json
import hmac
import hashlib

class PlisioCallbackTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.billing = Billing.objects.create(
            user=self.user,
            system='Plisio',
            amount=10.00,
            status='pending',
            date=timezone.now(),
            details=''
        )
        self.client = Client()

    def test_plisio_callback(self):
        # Construct callback data
        callback_data = {
            'order_number': self.billing.id,
            'amount': '10.00',
            'status': 'completed',
            # ... other necessary fields
        }

        # Calculate verify_hash
        secret_key = 'oCjqcMcbsH1eQrXCnwkF0vdcbqdUq6QVy3AqghvYwD5GIk9iE0ox67oHxHz5Zaeh'  # Replace with your actual Plisio secret key
        post_data = callback_data.copy()
        post_data.pop('verify_hash', None)
        sorted_data = sorted(post_data.items())
        message = json.dumps(sorted_data, separators=(',', ':'))
        hmac_hash = hmac.new(secret_key.encode(), message.encode(), hashlib.sha1).hexdigest()
        callback_data['verify_hash'] = hmac_hash

        # Send POST request to the callback URL
        response = self.client.post(reverse('plisio_callback'), json.dumps(callback_data), content_type='application/json')

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Verify that the Billing and Balance records were updated
        self.billing.refresh_from_db()
        self.assertEqual(self.billing.status, 'completed')

        balance = Balance.objects.get(user=self.user)
        self.assertEqual(balance.balance, 10.00)

# Don't forget to replace 'plisio_callback' with the actual name of your callback URL
