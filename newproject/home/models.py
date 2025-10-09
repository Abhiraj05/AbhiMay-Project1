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


class Request_Blood(models.Model):
    patient_name = models.CharField(max_length=100, null=False, blank=False)
    blood_group = models.CharField(
        max_length=3, choices=BloodGroup.choices, null=False, blank=False)
    contact_number = models.CharField(max_length=10, null=False, blank=False)
    hospital_name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
