from django.db import models
from accounts.models import *
# Create your models here.

class Vendor(models.Model):

    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    vendor_slug = models.SlugField(max_length=100, unique=True) #to show vendor pages

    def __str__(self):
        return self.vendor_name
