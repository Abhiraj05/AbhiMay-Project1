from django.shortcuts import render,redirect
from django.contrib import messages
from adminpanel.models import *

# Create your views here.
def main(request):
    return render(request,"main.html")

def user_exist(username,password):
    return User_Registration.objects.filter(username=username,password=password).first()

def sign_up(request):
    error=None
    message=None
    if request.method  == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")
        
        if not username:
            error="please the enter the username."
            
        elif not password:
            error="please the enter the password."
            
        elif len(password)>=6:
            error="Password length should be a minimum of 6 characters."
            
        elif password!=confirm_password:
             error="password is not matching"
             
             if error:
                 return render(request,"sign_up.html",{"error":error})

        if not user_exist(username,password):
            User_Registration.objects.create(username=username,email=email,password=password)
            message="user register successfully."
            if message:
                 return render(request,"sign_up.html",{"message":message})
        else:
            message="user already exist."
            if message:
                 return render(request,"sign_up.html",{"message":message})
    return render(request,"sign_up.html")


def login(request): 
    message=None
    if request.method  == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        if not username:
            error="please the enter the username."
            
        elif not password:
            error="please the enter the password."
            
        elif len(password)>=6:
            error="Password length should be a minimum of 6 characters."
            
        if user_exist(username,password):
            message="user not register."
            if message:
                return redirect(request,"login.html",{"message":message})
        else:
            message="login successful."
            if message:
                return redirect(request,"login.html",{"message":message})
    return render(request,"login.html")