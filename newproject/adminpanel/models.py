from django.db import models
from django.contrib.auth.models import User


# Create your models here.


#model for extra fields for hospital admin
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username
