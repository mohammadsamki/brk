from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from .models import Ticket
from django import forms
from .models import AdminReply, Balance
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

from captcha.fields import ReCaptchaField

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()

class BalanceForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())


    class Meta:
        model = Balance
        fields = ['user', 'balance']
class UserReplyForm(forms.ModelForm):
    user_reply = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Ticket
        fields = ['user_reply']

class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['admin_reply']
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description']

# Create your forms here.

class NewUserForm(UserCreationForm):
	alt_pass= forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
        

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.save()
		return user
	
class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error alert alert-danger mt-1">%s</div>' % e for e in self])