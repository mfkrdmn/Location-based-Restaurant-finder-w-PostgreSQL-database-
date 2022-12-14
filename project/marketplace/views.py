from django.shortcuts import render, get_object_or_404
from vendor.models import *
from menu.models import *
from django.db.models import Prefetch
# Create your views here.

def marketplace(request):

    vendors = Vendor.objects.all()
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors,
        'vendor_count' : vendor_count
    }

    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):

    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.all()
        )
    )

    context = {
        'vendor' : vendor,
        'categories' :categories,
    }

    return render(request, 'marketplace/vendor_detail.html', context)


def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']

    vendors = Vendor.objects.filter(vendor_name__icontains=keyword)

    context = {
        'vendors' : vendors
    }

    
    return render(request, "marketplace/listings.html", context)


