from django.middleware.csrf import get_token

class CustomCsrfViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            # Set the CSRF token in the cookie for GET requests
            csrf_token = get_token(request)
            request.session['csrftoken'] = csrf_token
        elif request.method == 'POST':
            # Check the CSRF token for POST requests
            csrf_token = request.POST.get('csrfmiddlewaretoken', '')
            session_csrf_token = request.session.get('csrftoken', '')
            if csrf_token != session_csrf_token:
                return HttpResponseForbidden('CSRF verification failed.')
        response = self.get_response(request)
        return response
import re
import logging
from django.utils import timezone
from briansclub.models import LogEntry

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request method and URL
        logger.info(f'{request.method} {request.path}')

        # Determine if the request is coming from a browser or an API client
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'curl' in user_agent.lower():
            api_client = 'curl'
        elif 'postman' in user_agent.lower():
            api_client = 'Postman'
        elif 'googlebot' in user_agent.lower():
            api_client = 'Googlebot'
        else:
            api_client = re.findall(r'^\w+', user_agent)[0]

        # Extract the user information from the request
        user = None
        if request.user.is_authenticated:
            user = request.user.username

        # Extract the URL of the API endpoint from the request
        api_url = None
        if request.path.startswith('/api/'):
            api_url = request.build_absolute_uri()

        # Save the log to the database
        log = LogEntry(
            method=request.method,
            path=request.path,
            user_agent=user_agent,
            api_client=api_client,
            user=user,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            api_url=api_url,
            timestamp=timezone.now(),
        )
        log.save()

        # Call the next middleware or view
        response = self.get_response(request)

        return response
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden

class BlockCurlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        api_client = request.META.get('HTTP_API_CLIENT', '').lower()
        if 'curl' in api_client:
            return HttpResponse('Curl requests are not allowed', status=403)
        if 'curl' in user_agent:
            return HttpResponse('Curl requests are not allowed', status=403)
        return self.get_response(request)
from django.http import HttpResponseRedirect

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:  # Check if the response is a 404 Not Found
            return HttpResponseRedirect('https://bclub.cc')  # Redirect to Google
        return response
