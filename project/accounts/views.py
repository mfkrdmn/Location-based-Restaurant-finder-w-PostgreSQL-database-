from django.shortcuts import render, redirect
from .utils import detectUser
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied #will show error if the user is not permitted


# Restric vendor from accessing customer dashboard page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restric customer from accessing vendor dashboard page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


#############

 
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("dashboard")

    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            # return redirect('registerUser')

            # ustteki kisim asaginin diger yolu

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('login')
        
        else:
            print('Invalid Form')
            print(form.errors)
            
    else:
        form = UserForm()


    context = {
        'form' : form
    }
    return render(request, 'registerUser.html', context)


#############


def registerVendor(request):

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("dashboard")

    elif request.method == 'POST':
        #store the data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('registerVendor')


            # burada yaptığımız şey eğer kullanıcı bir vendor olarak kayıt yapacaksa aynı zamanda bir
            #user da olacağı için hem user hem vendor form dan veri çekip vendor ve user olarak kaydını yapıyoruz


        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form  = VendorForm()

    context = {
        'form' : form,
        'v_form' : v_form,
    }

    return render(request, "registerVendor.html", context)


#############


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("myAccount")

    elif request.method == "POST": #user is not logged in yet
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user) 
            messages.success(request, "You are now logged in")
            return redirect("myAccount")

        else:
            messages.error(request, "Invalid login informations")
            return redirect("login")


    return render(request, "login.html")


#############


def logout(request):
    auth.logout(request)
    messages.error(request, "You are logged out")
    return redirect("login")


#############


def dashboard(request):
    return render(request, "dashboard.html")


#############


@login_required(login_url = "login")
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url = "login")

@user_passes_test(check_role_customer)

def custDashboard(request):
    return render(request, "custDashboard.html")


@login_required(login_url = "login")

@user_passes_test(check_role_vendor)

def vendorAccount(request):
    return render(request, "vendorAccount.html")