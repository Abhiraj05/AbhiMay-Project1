from django.db import models

# Create your models here.
class BloodGroup(models.TextChoices):
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"

class Donor(models.Model):
    name = models.CharField(max_length=100, blank = False)
    age = models.IntegerField()
    gender = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, blank=False , null=False)
    phone_number = models.CharField(max_length=10, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=False, null=False)
    last_donation_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

