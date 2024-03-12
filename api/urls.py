from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserDataDetail,UserDataListCreate,UserDataUpdate
# from .views import TaskViewSet, LogEntryViewSet, BriansclubAddressViewSet, SiteConfigurationViewSet, TicketViewSet, AdminReplyViewSet, ReplyViewSet, BalanceViewSet, TransactionViewSet, CartItemViewSet, OrderViewSet, OrdersNumberViewSet, BillingViewSet

# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet)
# router.register(r'log_entries', LogEntryViewSet)
# router.register(r'briansclub_addresses', BriansclubAddressViewSet)
# router.register(r'site_configurations', SiteConfigurationViewSet)
# router.register(r'tickets', TicketViewSet)
# router.register(r'admin_replies', AdminReplyViewSet)
# router.register(r'replies', ReplyViewSet)
# router.register(r'balances', BalanceViewSet)
# router.register(r'transactions', TransactionViewSet)
# router.register(r'cart_items', CartItemViewSet)
# router.register(r'orders', OrderViewSet)
# router.register(r'orders_numbers', OrdersNumberViewSet)
# router.register(r'billings', BillingViewSet)
urlpatterns = [
    #  path('', include(router.urls)),

       path('userdata/', UserDataDetail.as_view()),
       path('userdata/create/', UserDataListCreate.as_view()),
       path('userdata/<str:username>/update/', UserDataUpdate.as_view(), name='user_data_update'),
   ]