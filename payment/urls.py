from django.urls import path
from .views import payment, payment_callback

urlpatterns = [
       path('', payment, name='payment'),
       path('callback/', payment_callback, name='payment_callback'), # type: ignore
   ]