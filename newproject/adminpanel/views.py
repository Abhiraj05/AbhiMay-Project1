from django.shortcuts import render,redirect
from django.contrib import messages
from adminpanel.models import *

# Create your views here.
def main(request):
    return render(request,"main.html")

def value_check(value):
    return value == "" or value is None

def user_exist(username,password):
    user=User_Registration.objects.filter(username=username,password=password).first()
    return user


def sign_up(request):
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

        if not user_exist(username,password):
            User_Registration.objects.create(username=username,password=password)
            messages.success(request, "user register successfully")
            return redirect("/")
        else:
            messages.success(request, "user already exist")
            return redirect("/")
    return render(request,"sign_up.html")


def login(request):
    
    if request.method  == "POST":
        username=username.POST.get("")
        password=password.POST.get("")
        confirm_password=confirm_password.POST.get("")
        
        if value_check(username):
            messages.warning("please the enter the username")
            
        if value_check(password):
            messages.warning("please the enter the password")
        
        if user_exist(username,password):
            messages.warning("user not register")
           
    return render(request,"login.html")