from django.contrib import admin

# Register your models here.
from .models import Ride, DriverSchedule, Message, Location

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_location', 'end_location', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['start_location', 'end_location', 'user__username']

@admin.register(DriverSchedule)
class DriverScheduleAdmin(admin.ModelAdmin):
    list_display = ['driver', 'available_days', 'available_hours']
    search_fields = ['driver__username']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'ride', 'timestamp']
    search_fields = ['sender__username', 'receiver__username', 'ride__id']
    list_filter = ['timestamp']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['user_type', 'latitude', 'longitude', 'created_at', 'user_id']
    list_filter = ['user_id', 'created_at']
    search_fields = ['user_id']