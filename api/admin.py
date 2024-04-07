from django.db import models
from django.db.models.functions import Cast
from django.contrib import admin
from .models import UserData
from django.contrib import admin
from django.utils import timezone

class CustomAdminSite(admin.AdminSite):
    def date_hierarchy_drilldown(self, year, month=None, day=None):
        if day is not None:
            dt = timezone.datetime(year, month, day)
            link_date = dt.strftime('%Y-%m-%d')
            return {
                'year': year,
                'month': month,
                'day': day,
                'link': link_date,
                'link_date': dt.strftime('%B %d, %Y'),
            }
        elif month is not None:
            dt = timezone.datetime(year, month, 1)
            link_date = dt.strftime('%Y-%m')
            return {
                'year': year,
                'month': month,
                'link': link_date,
                'link_date': dt.strftime('%B %Y'),
            }
        else:
            dt = timezone.datetime(year, 1, 1)
            link_date = dt.strftime('%Y')
            return {
                'year': year,
                'link': link_date,
                'link_date': dt.strftime('%Y'),
            }

admin_site = CustomAdminSite()

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'updated_at', 'balance', 'balance_as_float')
    date_hierarchy = 'created_at'
    ordering = ('-balance',)
    search_fields = ('username',)
    def balance_as_float(self, obj):
        return obj.balance_as_float()
    balance_as_float.admin_order_field = 'balance'

admin.site.register(UserData, UserDataAdmin)
