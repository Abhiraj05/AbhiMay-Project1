from django.shortcuts import render, redirect
from donors.models import Donor
from django.contrib import messages
from django.contrib.auth.models import User # Import the User model
from django.core.mail import send_mail

def send_email(name,hospital_email,donor_email):
    try:
        send_mail(
           "Request Is Under Review",
        f"""Hello! {name}, 
        your donor registration request is pending. 
        Once the verication is done, we will contact you.
        Thank you!.
        """,
        hospital_email,
        [donor_email],
        fail_silently=False,
        )
    except:
        messages.error("email not sent!")
    
def donor_data(request):
    error = None 
    if request.method == "POST":
        name = request.POST.get("donor_name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        blood_group = request.POST.get("blood_group")
        address = request.POST.get("location")
        last_donation_date = request.POST.get("last_donation_date")

        if not name:
            error = "Please enter your name."
        elif not age:
            error = "Please enter your age."
        elif int(age) < 18:
            error = "Sorry, you must be at least 18 years old to register."
        elif not phone_no:
            error = "Please enter your phone number."
        elif not email:
            error = "Please enter your email."
        elif User.objects.filter(email=email).exists():
            error = "A user with this email address already exists."
        elif not password or not confirm_password:
            error = "Please enter and confirm your password."
        elif password != confirm_password:
            error = "Passwords do not match."

        if error:
            
            context = {
                'error': error, 'name': name, 'age': age, 'gender': gender, 
                'phone_no': phone_no, 'email': email, 'address': address, 
                'last_donation_date': last_donation_date
            }
            return render(request, "form.html", context)

        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
       
        user.first_name = name.split(' ')[0]
        user.save()
        
        
        Donor.objects.create(
            user=user,
            name=name,
            age=age,
            blood_group=blood_group,
            gender=gender,
            phone_number=phone_no,
            email=email,
            address=address,
            last_donation_date=last_donation_date if last_donation_date else None
        )
        hospital_email="xyzhospital@gmail.com"
        send_email(name,hospital_email,email)
        return redirect("/eligibility")

    return render(request, "form.html")


def donor_eligibility(request):
    if request.method == "POST":
        age_check = request.POST.get("age")
        weight_check = request.POST.get("weight")
        health_condition = request.POST.get("health")
        tattoo_check = request.POST.get("tattoo")
        fever_check = request.POST.get("fever")
        hiv_check = request.POST.get("disease")

        is_eligible = (
            age_check == "yes" and weight_check == "yes" and
            health_condition == "yes" and tattoo_check == "no" and
            fever_check == "no" and hiv_check == "no"
        )

        if is_eligible:
            messages.success(
                request,
                "🎉 Thank you! You have successfully registered as a donor."
            )
            return redirect("/") 
        else:
            messages.error(
                request,
                "❌ Sorry, you are not eligible to donate blood based on your answers."
            )
            return redirect("eligibility") 

    return render(request, "eligibility_form.html")

def blood_bank(request):
    return render(request, "blood_bank.html")   

def my_profile(request):
    return render(request, "profile.html")