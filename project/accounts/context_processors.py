from vendor.models import *

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