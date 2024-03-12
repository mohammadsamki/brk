from .models import UserData
from rest_framework import serializers

class UserDataSerializer(serializers.ModelSerializer):
       class Meta:
           model = UserData
           fields = ['id', 'username', 'password', 'balance']

# from rest_framework import serializers
# from briansclub.models import Task, LogEntry, BriansclubAddress, SiteConfiguration, Ticket, AdminReply, Reply, Balance, Transaction, CartItem, Order, OrdersNumber, Billing

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'

# class LogEntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LogEntry
#         fields = '__all__'

# class BriansclubAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BriansclubAddress
#         fields = '__all__'

# class SiteConfigurationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SiteConfiguration
#         fields = '__all__'

# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = '__all__'

# class AdminReplySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdminReply
#         fields = '__all__'

# class ReplySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reply
#         fields = '__all__'

# class BalanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Balance
#         fields = '__all__'

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'

# class CartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'

# class OrdersNumberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrdersNumber
#         fields = '__all__'

# class BillingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Billing
#         fields = '__all__'
