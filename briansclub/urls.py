from django.urls import path, include
from . import views
from django.contrib.sitemaps.views import sitemap

from .sitemaps import TaskSitemap,StaticSitemap
from django.views.generic import TemplateView



sitemaps = {
    'tasks': TaskSitemap,
    'static':StaticSitemap


}

urlpatterns = [
        path('create_deposit/', views.create_deposit, name='create_deposit'),
path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('plisio_callback/',views.plisio_callback,name='plisio_callback'),
    path('wallet/', views.wallet_transactions, name='wallet_transactions'),
    path('tickets/admin', views.ticket_view, name='ticket_view'),
    # path('admin/admin_replies/', views.admin_reply_view, name='admin_reply_view'),
    # path('admin/replies/', views.reply_view, name='reply_view'),
    path('balances/admin', views.balance_view, name='balance_view'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_selected_from_cart/', views.remove_selected_from_cart, name='remove_selected_from_cart'),
    path("Billing", views.address_list, name="tasklist"),
    path("", views.dashboard, name="home"), # type: ignore
    path("official/", views.loginreq, name="official"), # type: ignore
    path("welcome/", views.loginreq, name="welcome"), # type: ignore
    path("briansclub/", views.loginreq, name="briansclub"), # type: ignore
    path("login", views.loginreq, name="login"), # type: ignore
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("dumps", views.dumps, name="dumps"),
    path("cvv", views.cvv, name="cvv"),
    path("fullz", views.fullz, name="fullz"),
    path("wholesale", views.wholesale, name="wholesale"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders"),
    path("auction", views.auction, name="auction"),
    path("tools", views.tools, name="tools"),
    path("profile/", views.profile, name="profile"),
#    path('brinsclubcom/sitemap.xml', TemplateView.as_view(template_name='main/brianclubcom/sitemap.xml', content_type='application/xml')),
path('sitemap.xml', views.dynamic_sitemap, name='dynamic_sitemap'),    # path('fack/sitemap.xml', TemplateView.as_view(template_name='main/fack/sitemap.xml', content_type='application/xml')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # robots.txt
        path("robots.txt", views.robots, name="robots.txt"),
    path('change_password/', views.change_password, name='change_password'),
        path('tickets/', views.ticket, name='ticket'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    # path('replay/tickets/', views.ticket_list, name='ticket_list'),
    # path('my-view/', views.my_view, name='my-view'),




]
