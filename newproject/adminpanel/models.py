from django.db import models

# Create your models here.
class User_Registration(models.Model):
    username=models.CharField(max_length=10,blank=False)
    password=models.CharField(max_length=8,blank=False)
    