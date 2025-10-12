from django.shortcuts import render
from django.contrib import messages
from home.models import Request_Blood
from django.core.mail import send_mail
from adminpanel.models import Profile

# Create your views here.


def send_email(request, hospital_email, donor_email, message, mail_subject):
    try:
        send_mail(
            f"{mail_subject}",
            f"""
        {message}
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
        hospital_name_from_form = request.POST.get("hospital_name")

        if not patient_name:
            error = "Please enter your name."
        elif not blood_group:
            error = "Please select the blood group."
        elif len(contact_number) < 10 or not contact_number:
            error = "Please enter your phone number."
        elif not email_id:
            error = "Please enter your email id."
        elif not hospital_name_from_form:
            error = "Please enter your hospital name."

        if error:
            return render(request, "request_blood.html", {"error": error})
        else:
            request_blood = Request_Blood.objects.create(patient_name=patient_name,
                                                         blood_group=blood_group,
                                                         contact_number=contact_number,
                                                         email_id=email_id,
                                                         hospital_name=hospital_name_from_form)
            request_blood.save()

            # Safely get the hospital profile
            hospital_profile = Profile.objects.filter(
                hospital=hospital_name_from_form).first()

            # Only send an email if the hospital profile exists
            if hospital_profile and hospital_profile.email:
                hospital_email = hospital_profile.email
                hospital_name = hospital_profile.hospital
                mail_subject = "Blood Request Pending — Awaiting Approval"
                message_body = f"""
                Hello {patient_name},

                Your blood request has been successfully submitted.

                It is currently pending approval, and once it is reviewed and approved, we will contact you with further details.

                Thank you for your patience and for trusting our service.

                Warm regards,
                {hospital_name} Team
                """
                send_email(request, hospital_email, email_id,
                           message_body, mail_subject)
            else:
                # Optional: Inform the user that a notification could not be sent to the hospital
                messages.warning(
                    request, "Your request was submitted, but we could not notify the hospital. Please contact them directly.")

            message = True
            return render(request, "request_blood.html", {"message": message})

    return render(request, "request_blood.html")


def about(request):
    return render(request, "about.html")


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not name:
            messages.error(request, "Please enter your name.")
        elif not email:
            messages.error(request, "Please enter your email.")
        elif not subject:
            messages.error(request, "Please enter the subject.")
        elif not message:
            messages.error(request, "Please enter your message.")

        default_mail = "contact@rakthadaan.org"
        if name and email and subject and message:
             send_email(request, email, default_mail, message, subject)
             messages.success(request, "your message successfully submitted.")
      

    return render(request, "contact_us.html")
