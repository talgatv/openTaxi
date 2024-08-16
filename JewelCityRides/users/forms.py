# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Driver

class DriverRegistrationForm(UserCreationForm):
    class Meta:
        model = Driver
        # fields = ['username', 'password1', 'password2', 'full_name', 'phone_number', 'car_make', 'car_model', 'car_year', 'car_color', 'license_plate', 'license_number', 'insurance_policy_number']
        fields = ['username', 'password1', 'password2', 'full_name', ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Сделать водителя неактивным
        if commit:
            user.save()
        return user