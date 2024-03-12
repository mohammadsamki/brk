from django.contrib.auth.models import User
from django.forms import Select

class UserSelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        user = User.objects.get(id=option_value)
        return super().render_option(selected_choices, option_value, user.username) # type: ignore