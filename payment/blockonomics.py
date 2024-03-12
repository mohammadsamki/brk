import requests
import json

API_KEY = 'LEtnU8oh3g64vEaUHRuKIvygSn0vAvQd9FuDkaFmUgs'

def create_payment_request(amount, callback_url):
       url = 'https://www.blockonomics.co/api/new_address'
       headers = {'Authorization': API_KEY}
       data = {
           'amount': amount,
           'callback': callback_url
       }
       response = requests.post(url, headers=headers, data=json.dumps(data))
       if response.status_code == 200:
           payment_data = response.json()
           return payment_data['address'], payment_data['bitcoin_amount']
       else:
           return None, None
       
def verify_payment(txid):
       url = 'https://www.blockonomics.co/api/tx_detail'
       headers = {'Authorization': API_KEY}
       data = {'txid': txid}
       response = requests.post(url, headers=headers, data=json.dumps(data))
       if response.status_code == 200:
           payment_data = response.json()
           if payment_data['status'] == '1':
               return True
           else:
               return False
       else:
           return False
       

def create_invoice(amount):
       url = 'https://www.blockonomics.co/api/new_invoice'
       headers = {'Authorization': API_KEY}
       data = {'amount': amount}
       response = requests.post(url, headers=headers, data=json.dumps(data))
       if response.status_code == 200:
           invoice_data = response.json()
           return invoice_data
       else:
           return None
