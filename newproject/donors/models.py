from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class BloodGroup(models.TextChoices):
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"


class HospitalChoices(models.TextChoices):
    GOA_MEDICAL_COLLEGE = "Goa Medical College Blood Bank", "Goa Medical College Blood Bank"
    MANIPAL_HOSPITAL = "Manipal Hospital Blood Bank", "Manipal Hospital Blood Bank"
    HOSPICIO_HOSPITAL = "Hospicio Hospital Blood Bank", "Hospicio Hospital Blood Bank"
    ASILO_HOSPITAL = "Asilo Hospital Blood Bank", "Asilo Hospital Blood Bank"
    DISTRICT_HOSPITAL = "District Hospital Blood Bank", "District Hospital Blood Bank"
    RED_CROSS = "Red Cross Blood Bank", "Red Cross Blood Bank"
    SUB_DISTRICT_HOSPITAL = "Sub District Hospital Blood Bank", "Sub District Hospital Blood Bank"
    VRUNDAVAN_HOSPITAL = "Vrundavan Hospital Blood Bank", "Vrundavan Hospital Blood Bank"
    APOLLO_VICTOR_HOSPITAL = "Apollo Victor Hospital Blood Bank", "Apollo Victor Hospital Blood Bank"
    SHRI_SAI_CENTRAL = "Shri Sai Central Blood Bank & Lab", "Shri Sai Central Blood Bank & Lab"
    FONSECAS_PATHOLOGY = "Fonsecas Pathology Laboratory / Blood Bank", "Fonsecas Pathology Laboratory / Blood Bank"
    JEEVANDHARA = "Jeevandhara Blood Bank", "Jeevandhara Blood Bank"

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=False)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, blank=False, null=False)
    phone_number = PhoneNumberField(region="IN", null=True, blank=True, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    hospital=models.CharField(max_length=100,choices=HospitalChoices.choices, blank=True,null=True)
    last_donation_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
