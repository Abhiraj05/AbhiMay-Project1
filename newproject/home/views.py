from django.shortcuts import render

# Create your views here.


def blood_request(request):
    error = None
    if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        blood_group = request.POST.get("blood_group")
        contact_number = request.POST.get("contact_number")
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

    return render(request, "request_blood.html")
