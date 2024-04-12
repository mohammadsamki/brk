from django.contrib import admin
from django.http import HttpResponse

from briansclub.widgets import UserSelect
from .models import BriansclubAddress,SiteConfiguration,Balance,CartItem,Transaction,Order,Billing,OrdersNumber,DomainAPIKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from django.contrib.admin import AdminSite
from django.middleware.csrf import CsrfViewMiddleware
from .middleware import CustomCsrfViewMiddleware
from django.utils.module_loading import import_string
class MyAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry = admin.site._registry
        self.middleware_classes = [CsrfViewMiddleware] + self.middleware_classes if hasattr(self, 'middleware_classes') else [CsrfViewMiddleware]
        self.middleware = [CustomCsrfViewMiddleware(get_response=self._middleware_chain)] + self.middleware_classes

    def _middleware_chain(self, request):
        """
        Return a middleware chain composed of the middleware classes
        defined in the settings and the default middleware classes.
        """
        middleware = []
        for middleware_path in self.settings.MIDDLEWARE:
            middleware_class = import_string(middleware_path)
            middleware.append(middleware_class)
        middleware += self.middleware_classes
        return self.resolve_request(request, middleware)

admin_site = MyAdminSite()
@csrf_exempt
class BriansclubAddressAdmin(admin.ModelAdmin):
       list_display = ('btc_address', 'eth_address', 'ald_address', 'ltc_address')
@csrf_exempt

class CustomUserAdmin(UserAdmin):
    list_display = ('username','last_login', 'date_joined')
    search_fields = ['username', 'first_name', 'last_name', 'email']

    ordering = ('-last_login','-date_joined')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(BriansclubAddress, BriansclubAddressAdmin)
admin.site.register(SiteConfiguration)

from .models import Ticket, Reply,AdminReply
from .forms import AdminReplyForm

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0

class AdminReplyInline(admin.TabularInline):
    model = AdminReply
    extra = 0
@csrf_exempt

class TicketAdmin(admin.ModelAdmin):
    inlines = [ReplyInline,AdminReplyInline]
    list_display = ['subject', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['subject', 'description', 'user__username']
    readonly_fields = ['user', 'created_at', 'updated_at']
    fieldsets = [
        (None, {'fields': ['user', 'subject', 'description']}),
        ('Date information', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
        ('Admin reply', {'fields': ['admin_reply'], 'classes': ['collapse']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_staff:
            self.form = AdminReplyForm
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if request.user.is_staff:
            obj.save()
            message = form.cleaned_data['admin_reply']
            if message:  # <-- check if the message field is not empty
                reply = Reply.objects.create(ticket=obj, user=request.user, message=message)
@csrf_exempt

class AdminReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'message', 'created_at', 'modified_at')
    actions = ['delete_user_replies']

    def delete_user_replies(self, request, queryset):
        for reply in queryset.filter(user__is_staff=False):
            reply.delete()
        ticket = queryset.first().ticket
        message = request.POST.get('admin_reply', '').strip()
        if message:
            AdminReply.objects.create(ticket=ticket, message=message)

    delete_user_replies.short_description = "Delete user replies and create admin reply"
admin.site.register(AdminReply, AdminReplyAdmin)


admin.site.register(Ticket, TicketAdmin)


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from briansclub.models import LogEntry

class UserAgentFilter(admin.SimpleListFilter):
    title = _('User agent')
    parameter_name = 'user_agent'

    def lookups(self, request, model_admin):
        return (
            ('curl', 'curl'),
            ('postman', 'Postman'),
            ('browser', 'Browser'),
            ('googlebot', 'Googlebot'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'curl':
            return queryset.filter(user_agent__icontains='curl')
        elif self.value() == 'postman':
            return queryset.filter(user_agent__icontains='postman')
        elif self.value() == 'browser':
            return queryset.exclude(user_agent__icontains='curl').exclude(user_agent__icontains='postman')
        elif self.value() == 'googlebot':
            return queryset.filter(user_agent__icontains='googlebot')

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'user_agent', 'ip_address', 'timestamp', 'api_client', 'user', 'api_url')
    list_filter = (UserAgentFilter, 'api_client')

admin.site.register(LogEntry, LogEntryAdmin)
from django.db import models
from django.contrib.auth.models import User
from django.forms import Select

class UserSelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        user = User.objects.get(id=option_value)
        return super().render_option(selected_choices, option_value, user.username)

class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'balance_change_counter',  'updated_at']
    list_filter = ('user',)
    search_fields = ('user__username',)
    formfield_overrides = {
        models.OneToOneField: {'widget': UserSelect},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["widget"] = Select(attrs={'class': 'select2'})
            kwargs["queryset"] = User.objects.order_by('username')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css',)
        }
        js = ('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js',)

admin.site.register(Balance, BalanceAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'price')
    list_filter = ('user',)

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Transaction)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','type','card_number','exp','cvv2','bank','address', 'user', 'status', 'price')  # Add other fields you want to display in the list
    actions = ['download_orders']
    list_filter = ('type',)
    def download_orders(self, request, queryset):
        # Create a HttpResponse with the text/csv content type
        response = HttpResponse(content_type='text')
        response['Content-Disposition'] = 'attachment; filename="orders.txt"'

        # Write the header
        response.write("bin|exp|cvv2\n")

        # Write the data
        for order in queryset:
            response.write(f"{order.card_number}|{order.exp}|{order.cvv2}\n")

        return response

    download_orders.short_description = "Download selected orders (bin|exp|cvv2)"

admin.site.register(Order, OrderAdmin)

class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'system','status','order_number')
    list_filter = ('user','order_number')

admin.site.register(Billing, BillingAdmin)
class OrdersNumberAdmin(admin.ModelAdmin):
    list_display = ('number',)
    list_filter = ('number',)

admin.site.register(OrdersNumber, OrdersNumberAdmin)
admin.site.register(DomainAPIKey)
