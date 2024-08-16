from django.urls import path
from .views import ActiveDriversList, DriverStatusUpdate, DriverLocationUpdate, DriverUpdate, UserRegistrationView, UserLoginView, ValidateTokenView, DriverRegistrationView, CustomUserRegistrationView, validate_token, DjDriverRegistrationView

urlpatterns = [
    # ... другие URL-маршруты ...
    path('api/active-drivers/', ActiveDriversList.as_view(), name='active-drivers'),
    path('api/driver/status-update/', DriverStatusUpdate.as_view(), name='driver-status-update'),
    path('api/driver/update-location/', DriverLocationUpdate.as_view(), name='driver-update-location'),
    path('api/driver/update-profile/', DriverUpdate.as_view(), name='driver-update-profile'),
    path('api/original_register/', UserRegistrationView.as_view(), name='register'),
    path('api/register/', CustomUserRegistrationView.as_view(), name='register-custom-user'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/token/validate', ValidateTokenView.as_view(), name='validate-token-2'),
    path('api/token/validate_2', validate_token, name='validate-token'),
    path('api/driver/register/', DriverRegistrationView.as_view(), name='register-driver'),
    path('register/driver/', DjDriverRegistrationView.as_view(), name='register-driver'),

]