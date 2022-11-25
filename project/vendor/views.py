from django.shortcuts import render, get_object_or_404,redirect
from .forms import VendorForm
from accounts.forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import *
from menu.forms import *
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

############

@login_required(login_url = "login")

@user_passes_test(check_role_vendor)
def vprofile(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings updates')
            return redirect('vprofile')
        
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    
    else:

        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile' :profile,
        'vendor' :vendor
    }
    return render(request, "vprofile.html", context)


############

def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')

    context = {
        'categories' : categories,
    }
    return render(request, 'menu-builder.html', context)


############


def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)

    context = {
        'fooditems' : fooditems,
        'category' : category,
    }

    return render(request, 'fooditems_by_category.html', context)


############ Category CRUD - Add

def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('menu_builder')
 

    else:
        form = CategoryForm()

    context = {
        'form' : form
    }


    return render(request, 'add_category.html', context)


############ Category - Edit

def edit_category(request, pk=None):

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('menu_builder')


    else:
        form = CategoryForm(instance=category) #instance=category demezsek edit page e edit olacak veriler gelmez

    context = {
        'form' : form,
        'category' :category,
    }


    return render(request, 'edit_category.html', context)


############ Category - Delete


def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('menu_builder')
