from django.shortcuts import render
from django.contrib import messages
from adminpanel.models import *

# Create your views here.
def main(request):
    return render(request,"main.html")

def value_check(value):
    return value == "" or value is None

def user_exist(username,password):
    user=User_Registration(username=username,password=password).first()
    return user

def login(request):
    if request.method  == "POST":
        username=username.POST.get("")
        password=password.POST.get("")
        confirm_password=confirm_password.POST.get("")
        
        if value_check(username):
            messages.warning("please the enter the username")
            
        if value_check(password):
            messages.warning("please the enter the password")
            
        if password!=confirm_password:
            messages.warning("password is not matching")
        
        if user_exist(username,password):
            messages.warning("user not register")
        
        
    return render(request,"login.html")