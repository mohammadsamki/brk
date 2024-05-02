from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

# from seo.models import SeoAbstract

# class MySeo(SeoAbstract):
#     pass

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LogEntry(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    api_client = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    api_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.method} {self.path}'
class BriansclubAddress(models.Model):
       btc_address = models.CharField(max_length=255)
       eth_address = models.CharField(max_length=255)
       ald_address = models.CharField(max_length=255)
       ltc_address = models.CharField(max_length=255)

class SiteConfiguration(models.Model):
    domain = models.CharField(max_length=50)
    google_analytics_id = models.CharField(max_length=50)

from .validators import validate_ticket_reply
from datetime import datetime

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=64, choices=(('open', 'Open'), ('closed', 'Closed')))

    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    admin_reply = models.TextField(blank=True, null=True)
    user_reply = models.ManyToManyField('AdminReply', blank=True, related_name='tickets')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.admin_reply is None:
            AdminReply.objects.create(ticket=self, message=""" we received you ticket and we will contact you soon""")
    def __str__(self):
        return self.subject

class AdminReply(models.Model):

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message} replied to {self.modified_at}'

    class Meta:
        ordering = ['-created_at']
class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(validators=[validate_ticket_reply])
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} replied to {self.ticket}'

    class Meta:
        ordering = ['-created_at']

from django.contrib.auth.models import User

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance_change_counter = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Balance.objects.get(pk=self.pk)
            if orig.balance != self.balance:
                self.balance_change_counter += 1
        super().save(*args, **kwargs)
    @classmethod
    def update_user_balance(cls, user_id, new_balance):
            balance, created = cls.objects.get_or_create(user_id=user_id)
            balance.balance = new_balance
            balance.save()
            print(f"Balance updated: {balance.balance}")

class Transaction(models.Model):
    balance = models.ForeignKey(Balance, related_name='transactions', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    query= models.CharField(max_length=255)
    country= models.CharField(max_length=255)
    issuer= models.CharField(max_length=255)



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bin = models.CharField(max_length=1000,null=True,blank=True)
    type = models.CharField(max_length=1000,null=True,blank=True)
    dc = models.CharField(max_length=1000,null=True,blank=True)
    subtype = models.CharField(max_length=1000,null=True,blank=True)
    card_number = models.CharField(max_length=1000,null=True,blank=True)
    exp = models.CharField(max_length=1000,null=True,blank=True)
    cvv2 = models.CharField(max_length=1000,null=True,blank=True)
    name = models.CharField(max_length=1000,null=True,blank=True)
    address = models.CharField(max_length=1000,null=True,blank=True)
    extra = models.CharField(max_length=1000,null=True,blank=True)
    bank = models.CharField(max_length=1000,null=True,blank=True)
    base = models.CharField(max_length=1000,null=True,blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    status = models.CharField(max_length=1000,null=True,blank=True)
    optional_field1 = models.CharField(max_length=1000, blank=True, null=True ,default='')
    optional_field2 = models.CharField(max_length=1000, blank=True, null=True ,default='')
    optional_field3 = models.CharField(max_length=1000, blank=True, null=True ,default='')
    table = models.TextField( blank=True, null=True ,default='')
    def save(self, *args, **kwargs):
            if not self.pk and Order.objects.filter(card_number=self.card_number).exists():
                # If the order is new and an order with the same card_number already exists,
                # don't save the new order.
                 return
            super().save(*args, **kwargs)
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrdersNumber(models.Model):
    number = models.IntegerField(default=0)
    orders = models.ManyToManyField(Order, related_name='orders_number')
    date = models.DateTimeField(auto_now_add=True )
    def save(self, *args, **kwargs):
            if not self.pk and OrdersNumber.objects.filter(number=self.number).exists():
                # If the order is new and an order with the same card_number already exists,
                # don't save the new order.
                 return
            super().save(*args, **kwargs)
    def __str__(self):
        return f"OrdersNumber #{self.number}"
class DomainAPIKey(models.Model):
    domain = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    def __str__(self) :
        return self.domain
class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    system = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    date = models.DateTimeField()
    details = models.TextField()
    order_number = models.CharField(max_length=100, unique=True,null=True)  # Add this field

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.system} - {self.amount} - {self.status} - {self.date}'
