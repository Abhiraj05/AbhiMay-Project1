from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminpanel.models import User_Registration
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from donors.models import Donor
from home.models import Request_Blood
import datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
# Create your views here.
def main(request):
    return render(request,"main.html")

@login_required
def all_donors_view(request):
    if not request.user.is_staff:
        messages.error(request,"You do not have access to this page.")
        return redirect('/')
    donor_list=Donor.objects.all().order_by('-created_at')
    paginator=Paginator(donor_list,10)
    page_number=request.GET.get('page')
    display_page=paginator.get_page(page_number)
    context={'display_page':display_page}
    return render(request,"all_donors.html",context)


@login_required
def show_blood_requests_view(request):
    if not request.user.is_staff:
        messages.error(request,"You do not have access to this page.")
        return redirect("/")
    request_list=Request_Blood.objects.all().order_by('-created_at')
    paginator = Paginator(request_list, 10)
    page_number =request.GET.get('page')
    display_page=paginator.get_page(page_number)
    context={'display_page':display_page}
    return render(request,"show_blood_requests.html",context)


@login_required
def admin_dashboard_view(request, donor_id=None, action=None):
    # Check if the user is staff/hospital admin
    if not request.user.is_staff:
        messages.error(request, "You Do not have access to this page. Plz Contact Admin.")
        return redirect('/')
    
    # approve donor logic
    if donor_id and action == "approve":
        donor = get_object_or_404(Donor, id=donor_id)
        donor.is_verified=True
        donor.save()
        messages.success(request, f"Donor '{donor.name}' has been successfully approved.")
        return redirect('admin_dashboard')
    # decline donor logic
    if donor_id and action =="decline":
        donor = get_object_or_404(Donor, id=donor_id)
        donor_name=donor.name
        if hasattr(donor,'user') and donor.user is not None:
            donor.user.delete()
        else:
            donor.delete()
        messages.info(request, f"The application for '{donor_name}' has been declined and removed.")
        return redirect('admin_dashboard')
    # Data for stats showing cards
    pending_donors = Donor.objects.filter(is_verified=False)
    pending_donors_count = pending_donors.count()
    verified_donors_count = Donor.objects.filter(is_verified=True).count()
    #logic for request this month card
    day_30_days_ago = timezone.now()-datetime.timedelta(days=30)
    this_month_req_count = Request_Blood.objects.filter(created_at__gte=day_30_days_ago).count()



    context = {
        'pending_donors': pending_donors,
        'pending_donors_count': pending_donors_count,
        'verified_donors_count': verified_donors_count,
        'this_month_req_count': this_month_req_count,
    }
    return render(request, "hospital_admin.html" , context)


@login_required
def admin_settings_view(request):
    if not request.user.is_staff:
        return redirect('/')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # This is important to keep the user logged in after a password change.
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_settings')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'admin_settings.html', {'form': form})


def user_exist(username,password):
    user=User_Registration.objects.filter(username=username,password=password).first()
    return user

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        if not identifier or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "login.html", {"form": form})
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
                # getting name of that partcular email user bcz authenticate function only take username or email only one field
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return render(request, "login.html", {"form": form})
        else:
            username = identifier
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password1.")
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(request.META.get("HTTP_REFERER", "/"))
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
#     return User_Registration.objects.filter(username=username,password=password).first()

# def sign_up(request):
#     error=None
#     message=None
#     if request.method  == "POST":
#         username=request.POST.get("username")
#         email=request.POST.get("email")
#         password=request.POST.get("password")
#         confirm_password=request.POST.get("confirm_password")
        
#         if not username:
#             error="please the enter the username."
            
#         elif not password:
#             error="please the enter the password."
            
#         elif len(password)>=6:
#             error="Password length should be a minimum of 6 characters."
            
#         elif password!=confirm_password:
#              error="password is not matching"
             
#              if error:
#                  return render(request,"sign_up.html",{"error":error})

#         if not user_exist(username,password):
#             User_Registration.objects.create(username=username,email=email,password=password)
#             message="user register successfully."
#             if message:
#                  return render(request,"sign_up.html",{"message":message})
#         else:
#             message="user already exist."
#             if message:
#                  return render(request,"sign_up.html",{"message":message})
#     return render(request,"sign_up.html")


# def login(request): 
#     message=None
#     if request.method  == "POST":
#         username=request.POST.get("username")
#         password=request.POST.get("password")
        
#         if not username:
#             error="please the enter the username."
            
#         elif not password:
#             error="please the enter the password."
            
#         elif len(password)>=6:
#             error="Password length should be a minimum of 6 characters."
                   
#             if error:
#                  return render(request,"login.html",{"error":error})
            
#         if user_exist(username,password):
#             message="user not register."
#             if message:
#                 return redirect(request,"login.html",{"message":message})
#         else:
#             message="login successful."
#             if message:
#                 return redirect(request,"login.html",{"message":message})
#     return render(request,"login.html")
