from django.shortcuts import render, redirect
from donors.models import Donor
from newproject import urls
from django.contrib import messages


def donor_data(request):
    error = None  
    if request.method == "POST":
        name = request.POST.get("donor-name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood-group")
        address = request.POST.get("address")
        phone_no = request.POST.get("phone-no")
        email = request.POST.get("email")
        location = request.POST.get("location")
        last_donation_date = request.POST.get("last_donation_date")


        if not name:
            error = "Please enter your name."
        elif not age:
            error = "Please enter your age."
        elif int(age) < 18:
            error = "You cannot donate blood."
        elif not address:
            error = "Please enter your address."
        elif not phone_no:
            error = "Please enter your phone number."
        elif not email:
            error = "Please enter your email."
        elif not last_donation_date:
            error = "Please enter the last donation date."

       
        if error:
            return render(request, "form.html", {"error": error})

        
        Donor.objects.create(
            name=name,
            age=age,
            blood_group=blood_group,
            gender=gender,
            phone_number=phone_no,
            email=email,
            address=address,
            last_donation_date=last_donation_date
        )

        return redirect("/eligibility")

    return render(request, "form.html")


def donor_eligibility(request):
    if request.method == "POST":
        age = request.POST.get("age")
        weight = request.POST.get("weight")
        health_conditon = request.POST.get("health")
        tattoo = request.POST.get("tattoo")
        fever = request.POST.get("fever")
        hiv = request.POST.get("disease")

        is_eligible = (
            age == "yes" and weight == "yes" and
            health_conditon == "yes" and tattoo == "no" and
            fever == "no" and hiv == "no"
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
                "❌ Sorry, you are not eligible to donate blood right now."
            )
            return redirect("eligibility")

    return render(request, "eligibility_form.html")
