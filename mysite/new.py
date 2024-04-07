import json
import hmac
import hashlib
from bs4 import BeautifulSoup
from requests_html import HTMLSession
# Your data, excluding the verify_hash
# data = {
#     "status": "completed",
#     "order_number": "41882303-0fd9-453c-926c-e39a71ed7268",
#     "amount": "200",  # Make sure to replace SomeAmount with the actual amount
# }
# secret_key = "-KJNi4ZYTZa1vsudlJjeH8F2tKFZQnxbRkTU3vn8j4pS5QyWS01to3dqVXDzHEDM"

# # Sort the data and serialize it
# # Note: Sorting may not affect the final string representation if you're manually controlling the order
# sorted_data = sorted(data.items())
# serialized_data = json.dumps(sorted_data, separators=(',', ':'))

# # Calculate the HMAC SHA1 hash
# hmac_hash = hmac.new(secret_key.encode(), serialized_data.encode(), hashlib.sha1).hexdigest()

# print(f"Calculated verify_hash: {hmac_hash}")
session = HTMLSession()
response = session.get('https://plisio.net/invoice/6611a1f0112aa0d8070cc9a8')
response.html.render(timeout=30)
print('response',response)# Increase timeout to 30 seconds
if response.status_code == 200:
    print( response.html.html)
