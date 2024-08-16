from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Driver, CustomUser

class DriverAdmin(UserAdmin):
    model = Driver
    list_display = ('username', 'full_name', 'phone_number', 'car_make', 'car_model', 'car_year', 'car_color', 'license_plate', 'is_active_driver', 'rating', 'current_location')
    list_filter = ('is_active_driver', 'car_make', 'car_model', 'car_year')
    search_fields = ('full_name', 'phone_number', 'license_plate')
    ordering = ('full_name',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'full_name', 'phone_number', 'email', 'is_active', 'rating', 'address', 'is_customuser')
    # list_filter = ('is_active', 'date_joined')
    search_fields = ('full_name', 'phone_number', 'email')
    # ordering = ('full_name', 'date_joined')
    # exclude = ('date_joined',)
    readonly_fields = ('date_joined',)


admin.site.register(Driver, DriverAdmin)
admin.site.register(CustomUser, CustomUserAdmin)