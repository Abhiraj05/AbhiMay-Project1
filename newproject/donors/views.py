from django.shortcuts import render, redirect
from donors.models import Donor


def value_check(value):
    return value is None or value == ""


# Create your views here.
def donor_data(request):
    if request.method == "POST":
        # name = request.POST.get("donor-name")
        # age = request.POST.get("age")
        # gender = request.POST.get("gender")
        # blood_group = request.POST.get("blood-group")
        # address = request.POST.get("address")
        # phone_no = request.POST.get("phone-no")
        # email = request.POST.get("email")
        # location = request.POST.get("location")
        # last_donation_date = request.POST.get("last-donation-date")

        # if int(age) < 18:
        #     return "you cannot donate the the blood"

        # if value_check(name):
        #     return "please enter your  name"

        # if value_check(address):
        #     return "please enter your  address"

        # if value_check(phone_no):
        #     return "please enter your phone no."

        # if value_check(email):
        #     return "please enter your email"

        # if value_check(last_donation_date):
        #     return "please enter the last donation date"

        # Donor.objects.create(name=name, age=age, blood_group=blood_group, gender=gender, phone_number=phone_no,
        #                      email=email, address=address, last_donation_date=last_donation_date)

        return redirect("/eligibility")

    return render(request, "form.html")


def donor_eligibility(request):
    if request.method == "POST":
        # age = request.POST.get("age")
        # weight = request.POST.get("weight")
        # health_conditon = request.POST.get("health")
        # tattoo = request.POST.get("tattoo")
        # fever = request.POST.get("fever")
        # hiv = request.POST.get("disease")
        # if age == "yes" and weight == "yes" and health_conditon == "yes" and tattoo == "no" and fever == "no" and hiv == "no":
        #     return redirect("")
        # elif age == "yes" and weight == "yes" and health_conditon == "yes" and tattoo == "yes" and fever == "yes" and hiv == "yes":
        #     return redirect("")
        # elif age == "no" and weight == "no" and health_conditon == "no" and tattoo == "no" and fever == "no" and hiv == "no":
        #     return redirect("")

        return redirect("/")
    return render(request, "eligibility_form.html")
