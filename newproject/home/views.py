from django.shortcuts import render
from django.contrib import messages
from home.models import Request_Blood
from django.core.mail import send_mail

# Create your views here.
def send_email(request,hospital_email,donor_email,message,mail_subject):
    try:
        send_mail(
        "Blood Request Pending ",
         f"""Hello! {name}, 
        your blood request has been sent. 
        Once it is approved, we will contact you. 
        Thank you!
        """,
        hospital_email,
        [donor_email],
        fail_silently=False,
        )
    except:
        messages.error(request, "email not sent!")

def blood_request(request):
    error = None
    message = False
    if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        blood_group = request.POST.get("blood_group")
        contact_number = request.POST.get("contact_number")
        email_id = request.POST.get("email_id")
        hospital_name = request.POST.get("hospital_name")

        if not patient_name:
            error = "Please enter your name."
        elif not blood_group:
            error = "Please select the blood group."
        elif len(contact_number) < 10 or not contact_number:
            error = "Please enter your phone number."
        elif not hospital_name:
            error = "Please enter your hospital name."

        if error:
            return render(request, "request_blood.html", {"error": error})
        else:
            request_blood=Request_Blood.objects.create(patient_name=patient_name,
                                         blood_group=blood_group,
                                         contact_number=contact_number,
                                         hospital_name=hospital_name)
            request_blood.save()
            hospital=Profile.objects.filter(hospital=hospital_name).first()
            hospital_email=hospital.email
            hospital_name=hospital.hospital
            mail_subject="Blood Request Pending — Awaiting Approval"
            message=f"""
            Hello {patient_name},

            Your blood request has been successfully submitted.

            It is currently pending approval, and once it is reviewed and approved, we will contact you with further details.

            Thank you for your patience and for trusting our service.

            Warm regards,
            {hospital_name} Team
            """
            send_email(request,hospital_email,email_id,message,mail_subject)
            message = True
            return render(request, "request_blood.html", {"message": message})

    return render(request, "request_blood.html")


def about(request):
    return render(request, "about.html")


def contact_us(request):
    return render(request, "contact_us.html")
