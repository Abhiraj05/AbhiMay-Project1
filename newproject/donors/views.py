from django.shortcuts import render

# Create your views here.
def user_data(request):
    return render(request,"form.html")