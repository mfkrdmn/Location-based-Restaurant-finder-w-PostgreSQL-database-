from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display = ('category_name', 'vendor') 
    search_fields = ('category_name', 'vendor__vendor_name') #since vendor is foreign key, 
                                                        #to search in admin panel we reach it this way


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'updated_at') 
    search_fields = ('food_title', 'category__category_name','price')

admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem,FoodItemAdmin)