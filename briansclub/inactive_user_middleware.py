from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import resolve

class InactiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Calculate the date one week ago
            one_week_ago = timezone.now() - timedelta(weeks=1)

            # Check if the user hasn't logged in for more than a week
            if request.user.last_login and request.user.last_login < one_week_ago:
                # Get the current view name
                current_view_name = resolve(request.path_info).url_name

                # Check if the current view is not the restricted view
                if current_view_name != 'tasklist':
                    # Redirect the user to the specific view
                    return redirect('tasklist')

        response = self.get_response(request)
        return response