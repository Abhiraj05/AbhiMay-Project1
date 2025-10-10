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

class Request_Blood(models.Model):
    patient_name = models.CharField(max_length=100, null=False, blank=False)
    blood_group = models.CharField(
    max_length=3, choices=BloodGroup.choices, null=False, blank=False)
    contact_number = models.CharField(max_length=10, null=False, blank=False)
    hospital_name = models.CharField(max_length=100,choices=HospitalChoices.choices, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
