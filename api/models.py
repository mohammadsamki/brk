from django.db import models


class UserData(models.Model):
       username = models.CharField(max_length=50)
       password = models.CharField(max_length=50)
       # balance = models.CharField(max_length=50, default=0) # type: ignore
       balance = models.FloatField(  default=0.00) # type: ignore
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
       class Meta:
        unique_together = ('username', 'password',)

       def save(self, *args, **kwargs):
              if not self.pk and UserData.objects.filter(username=self.username, password=self.password).exists():
              # If the user is being created (i.e., it doesn't have a primary key yet)
              # and a user with the same username and password already exists,
              # don't save the current user.
                     return
              super().save(*args, **kwargs)
       def balance_as_float(self):
        try:
            return float(self.balance)
        except ValueError:
            return 0