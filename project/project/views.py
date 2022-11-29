from django.shortcuts import render
from vendor.models import *

def home(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors' : vendors
    }
    
    return render(request, 'home.html', context)