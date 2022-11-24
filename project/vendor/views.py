from django.shortcuts import render
from .forms import VendorForm
from accounts.forms import *
# Create your views here.

def vprofile(request):
    profile_form = UserProfileForm()
    vendor_form = VendorForm()
    return render(request, "vprofile.html")