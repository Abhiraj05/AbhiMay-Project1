from django.shortcuts import render


def value_check(value):
    return value is None or value == ""


# Create your views here.
def donor_data(request):
    if request.method == "POST":
        name = request.POST.get("")
        age = request.POST.get("")
        dob = request.POST.get("")
        gender = request.POST.get("")
        blood_group = request.POST.get("")
        address = request.POST.get("")
        phone_no = request.POST.get("")
        email = request.POST.get("")
        last_donation_date=request.POST.get("")

        if age < 18:
            return "you cannot donate the the blood"

        if value_check(name):
            return "please enter your  name"
        
        if value_check(dob):
            return "please enter  your  date of birth"

        if value_check(address):
            return "please enter your  address"

        if value_check(phone_no):
            return "please enter your phone no."
        
        
        if value_check(email):
            return "please enter your email"
        
        if value_check(last_donation_date):
            return "please enter the last donation date"

    return render(request, "form.html")
