from django.shortcuts import render

# Create your views here.

def find_donor(request):
    return render(request, "finddonors.html")
