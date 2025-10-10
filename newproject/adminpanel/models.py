from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class User_Registration(models.Model):
#     username=models.CharField(max_length=10,blank=False,null=False)
#     email=models.CharField(max_length=10,blank=False,null=False)
#     password=models.CharField(max_length=8,blank=False,null=False)
    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username
