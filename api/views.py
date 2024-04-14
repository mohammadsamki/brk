from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework import generics
from .models import UserData
from .serializers import UserDataSerializer

from rest_framework.permissions import IsAdminUser, AllowAny

class UserDataListCreate(generics.ListCreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        else:
            return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

    def put(self, request, *args, **kwargs):
        return self.handle_method_not_allowed() # type: ignore

    def patch(self, request, *args, **kwargs):
        return self.handle_method_not_allowed() # type: ignore

    def delete(self, request, *args, **kwargs):
        return self.handle_method_not_allowed() # type: ignore

from rest_framework.response import Response

class UserDataDetail(UserPassesTestMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

    def test_func(self):
        return self.request.user.is_staff # type: ignore

    def get_queryset(self):
        if self.request.user.is_staff: # type: ignore
            return UserData.objects.all()
        else:
            return UserData.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = UserDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class UserDataUpdate(generics.UpdateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    lookup_field = 'username'  # or 'pk' if you want to look up by primary key
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply additional filters if needed
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}

        try:
            return queryset.filter(**filter_kwargs).first()
        except UserData.MultipleObjectsReturned:
            # Handle the case where multiple objects are returned
            # Log an error, return a specific object, or raise an exception.
            # For example, you can handle it by returning the first object found.
            return queryset.filter(**filter_kwargs).first()  # Return the first object

# from rest_framework import viewsets
# from .models import Task, LogEntry, BriansclubAddress, SiteConfiguration, Ticket, AdminReply, Reply, Balance, Transaction, CartItem, Order, OrdersNumber, Billing
# from .serializers import TaskSerializer, LogEntrySerializer, BriansclubAddressSerializer, SiteConfigurationSerializer, TicketSerializer, AdminReplySerializer, ReplySerializer, BalanceSerializer, TransactionSerializer, CartItemSerializer, OrderSerializer, OrdersNumberSerializer, BillingSerializer

# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

# class LogEntryViewSet(viewsets.ModelViewSet):
#     queryset = LogEntry.objects.all()
#     serializer_class = LogEntrySerializer

# class BriansclubAddressViewSet(viewsets.ModelViewSet):
#     queryset = BriansclubAddress.objects.all()
#     serializer_class = BriansclubAddressSerializer

# class SiteConfigurationViewSet(viewsets.ModelViewSet):
#     queryset = SiteConfiguration.objects.all()
#     serializer_class = SiteConfigurationSerializer

# class TicketViewSet(viewsets.ModelViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer

# class AdminReplyViewSet(viewsets.ModelViewSet):
#     queryset = AdminReply.objects.all()
#     serializer_class = AdminReplySerializer

# class ReplyViewSet(viewsets.ModelViewSet):
#     queryset = Reply.objects.all()
#     serializer_class = ReplySerializer

# class BalanceViewSet(viewsets.ModelViewSet):
#     queryset = Balance.objects.all()
#     serializer_class = BalanceSerializer

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

# class CartItemViewSet(viewsets.ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# class OrdersNumberViewSet(viewsets.ModelViewSet):
#     queryset = OrdersNumber.objects.all()
#     serializer_class = OrdersNumberSerializer

# class BillingViewSet(viewsets.ModelViewSet):
#     queryset = Billing.objects.all()
#     serializer_class = BillingSerializer
