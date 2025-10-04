from django.shortcuts import render,redirect
from django.contrib import messages
from adminpanel.models import User_Registration
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def main(request):
    return render(request,"main.html")

def value_check(value):
    return value == "" or value is None

def user_exist(username,password):
    user=User_Registration.objects.filter(username=username,password=password).first()
    return user

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password1.")
        else:
            messages.error(request, "Invalid username or password2.")
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")
# def sign_up(request):
#     if request.method  == "POST":
#         username=request.POST.get("username")
#         email=request.POST.get("email")
#         password=request.POST.get("password")
#         confirm_password=request.POST.get("confirm_password")
        
#         if value_check(username):
#             messages.warning("please the enter the username")
            
#         if value_check(password):
#             messages.warning("please the enter the password")
            
#         if password!=confirm_password:
#             messages.warning("password is not matching")

#         if not user_exist(username,password):
#             User_Registration.objects.create(username=username,email=email,password=password)
#             messages.success(request, "user register successfully")
#             return redirect("login/")
#         else:
#             messages.success(request, "user already exist")
#             return redirect("signup/")
#     return render(request,"sign_up.html")


# def login(request): 
#     if request.method  == "POST":
#         username=request.POST.get("username")
#         password=request.POST.get("password")
        
#         if value_check(username):
#             messages.warning("please the enter the username")
            
#         if value_check(password):
#             messages.warning("please the enter the password")
        
#         if user_exist(username,password):
#             messages.warning("user not register")
#             return redirect("login/")
#         else:
#             messages.warning("login successful")
#             return redirect("finddonors/")
    
            
           
#     return render(request,"login.html")