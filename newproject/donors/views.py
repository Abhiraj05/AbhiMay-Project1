from django.shortcuts import render, redirect
from donors.models import Donor
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from adminpanel.models import Profile




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
        hospital_name= request.POST.get("hospital")
        last_donation_date = request.POST.get("last_donation_date")

        if not name:
            error = "Please enter your name."
        elif not age:
            error = "Please enter your age."
        elif int(age) < 18:
            error = "Sorry, you must be at least 18 years old to register."
        elif not phone_no:
            error = "Please enter your phone number."
        elif Donor.objects.filter(phone_number=phone_no).exists():
            error = "A donor with this phone number is already registered."
        elif not email:
            error = "Please enter your email."
        elif User.objects.filter(email=email).exists() or Donor.objects.filter(email=email).exists():
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
        
        
        donor = Donor.objects.create(
            user=user,
            name=name,
            age=age,
            blood_group=blood_group,
            gender=gender,
            phone_number=phone_no,
            email=email,
            address=address,
            hospital=hospital_name,
            last_donation_date=last_donation_date if last_donation_date else None
        )
        
        # Store the new donor's ID in the session to use in the next view
        request.session['donor_id_for_email'] = donor.id

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
            # Get the donor's ID from the session
            donor_id = request.session.get('donor_id_for_email')
            if donor_id:
                try:
                    donor = Donor.objects.get(id=donor_id)
                    hospital=Profile.objects.filter(hospital=donor.hospital).first()
                    hospital_email=hospital.email
                    hospital_name=hospital.hospital
                    mail_subject="Donor Registration Pending — Verification in Progress"
                    message=f"""
                    Hello {donor.name},

                    Thank you for registering as a blood donor!

                    Your registration request is currently pending verification.  
                    Once the verification process is completed, we will contact you with the next steps.

                    We appreciate your patience and your willingness to contribute to this noble cause.

                    Warm regards,
                    {hospital_name} Team
                    """
                    send_email(request, hospital_email, donor.email, message, mail_subject)
                    
                    # Clean up the session
                    del request.session['donor_id_for_email']

                except Donor.DoesNotExist:
                    # Handle the case where the donor might not be found
                    pass
            
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
            return redirect("/eligibility") 

    return render(request, "eligibility_form.html")

def blood_bank(request):
    return render(request, "blood_bank.html")   

def my_profile(request):
    if request.user.is_authenticated:
        error=None
        if request.method=="POST":
            user_id=request.user.id
            name=request.POST.get("name")
            age=request.POST.get("age")
            email=request.POST.get("email")
            phone_number=request.POST.get("phone_number")
            address=request.POST.get("address")
            last_donation_date=request.POST.get("last_donation_date")
            is_active=request.POST.get("is_active")
      
            if not name:
                messages.error(request,"Please enter your name.")
            elif not age:
                 messages.error(request,"Please enter your age.")
            elif int(age) < 18:
                 messages.error(request,"Sorry, your age should be more than 18 years old.")
            elif not phone_number:
                 messages.error(request,"Please enter your phone number.")
            elif not email:
                 messages.error(request,"Please enter your email.")
            elif not address:
                 messages.error(request,"Please enter your address.")

            
            donor=Donor.objects.get(id=user_id)
            
                
            donor.name=name
            donor.email=email
            donor.phone_number=phone_number
            donor.address=address
            donor.last_donation_date=last_donation_date
            if is_active=='on':
                donor.is_active=True
            else:
                donor.is_active=False
            messages.success(request,"profile details updated.")
            donor.save()
            return redirect("/profile")
    else:
        messages.error(request,"please login..")    
    return render(request, "profile.html")