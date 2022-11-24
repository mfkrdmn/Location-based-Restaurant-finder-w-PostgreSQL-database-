from vendor.models import *
from django.conf import settings

# def get_vendor(request):
#     vendor = Vendor.objects.get(user=request.user)
#     return dict(vendor=vendor)

#burada kod yukarıdakinde çalışır ancak logout olunca request.user olmadığı için
#hata verir. O yüzden aşağıdaki kodu yazdık


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor= None
    return dict(vendor=vendor)

#Google auto complete

def get_google_api(request):
    return {'GOOGLE_API_KEY' : settings.GOOGLE_API_KEY}