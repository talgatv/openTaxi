from django.urls import path
from . import views
# from .views import RequestRideView, UpdateCurrentRetrieveDriverLocationForRideView, UpdateDriverAvailabilityStatusView, RetrieveDriverLocationForRideView, ListActiveDriversView, ListListUserActiveRidesView, RideDetailsView, ListUserActiveRidesView,RetrieveDriverLocationForUserView, ListAvailableRidesForDriverView, AcceptAvailableRideView
from .views import (
    RequestRideView,
    # UpdateCurrentDriverLocationView,
    UpdateCurrentRetrieveDriverLocationForRideView,
    RetrieveDriverLocationForUserView,
    UpdateDriverAvailabilityStatusView,
    ListActiveDriversView,
    ListUserActiveRidesView,
    RideDetailsView,
    RetrieveDriverLocationForRideView,
    ListAvailableRidesForDriverView,
    AcceptAvailableRideView,
    DriverCurrentRideView,
    DriverArrivedView,
    StartRideView,
    CompleteRideView,
    LastRideSummaryView



    # CancelRideView,
    # DriverRideHistoryView,
    # UserRideHistoryView,
    # RateRideView,
    # DriverEarningsView
)


urlpatterns = [
    # Пользовательские запросы на поездку
    path('api/rides/request/', RequestRideView.as_view(), name='request-ride'),
    path('api/rides/create/', RequestRideView.as_view(), name='create-ride'),

    # Водитель обновляет своё местоположение
    path('api/driver/update-location/', UpdateCurrentRetrieveDriverLocationForRideView.as_view(), name='update-driver-location'),

    # Пользователь узнаёт местоположение водителя
    path('api/ride/driver-location/<int:ride_id>/', RetrieveDriverLocationForUserView.as_view(), name='get-driver-location'),
    path('api/ride/active/driver-location/', RetrieveDriverLocationForUserView.as_view(), name='get-driver-location'),

    # Водитель обновляет свой статус
    path('api/driver/status-update/', UpdateDriverAvailabilityStatusView.as_view(), name='driver-status-update'),
    # path('api/driver/status-update/', UpdateDriverAvailabilityStatusView.as_view(), name='driver-status-update'),

    # Список активных водителей
    path('api/drivers/active/', ListActiveDriversView.as_view(), name='active-drivers-list'),
    # path('api/drivers/active/', ListActiveDriversView.as_view(), name='active-drivers-list'),

    # Список активных поездок пользователя
    path('api/user/rides/active/', ListUserActiveRidesView.as_view(), name='user-active-rides'),
    # path('api/user/rides/active/', ListUserActiveRidesView.as_view(), name='user-active-rides'),

    # Детали поездки
    path('api/rides/detail/<int:ride_id>/', RideDetailsView.as_view(), name='ride-detail'),
    path('api/rides/<int:ride_id>/', RideDetailsView.as_view(), name='ride-detail'),

    # Водитель получает местоположение другого водителя по ID поездки
    path('api/rides/driver-location/<int:ride_id>/', RetrieveDriverLocationForRideView.as_view(), name='driver-location-for-ride'),
    path('api/rides/<int:ride_id>/driver-location/', RetrieveDriverLocationForRideView.as_view(), name='driver-location'),

    # Список доступных поездок для водителей
    path('api/drivers/rides/available/', ListAvailableRidesForDriverView.as_view(), name='available-rides-for-drivers'),
    # path('api/drivers/rides/available/', ListAvailableRidesForDriverView.as_view(), name='available-rides-for-drivers'),

    # Водитель принимает поездку
    path('api/rides/accept/<int:ride_id>/', AcceptAvailableRideView.as_view(), name='accept-ride'),

    # URL для получения текущей активной поездки водителем
    path('api/driver/current-ride/', DriverCurrentRideView.as_view(), name='driver-current-ride'),

    path('api/rides/<int:ride_id>/arrived/', DriverArrivedView.as_view(), name='driver-arrived'),
    path('api/rides/<int:ride_id>/start/', StartRideView.as_view(), name='start-ride'),
    path('api/rides/<int:ride_id>/complete/', CompleteRideView.as_view(), name='complete-ride'),
    path('api/driver/rides/last-summary/', LastRideSummaryView.as_view(), name='last-ride-summary'),

    # # Отмена поездки пассажиром
    # path('api/rides/cancel/<int:ride_id>/', CancelRideView.as_view(), name='cancel-ride'),

    # # История поездок водителя
    # path('api/driver/rides/history/', DriverRideHistoryView.as_view(), name='driver-ride-history'),

    # # История поездок пользователя
    # path('api/user/rides/history/', UserRideHistoryView.as_view(), name='user-ride-history'),

    # # Оценка поездки пассажиром
    # path('api/rides/rate/<int:ride_id>/', RateRideView.as_view(), name='rate-ride'),

    # # Показ заработка водителя
    # path('api/driver/earnings/', DriverEarningsView.as_view(), name='driver-earnings'),
]


# urlpatterns = [
#     path('rides/', views.list_rides, name='list_rides'),
#     path('rides/add/', views.add_ride, name='add_ride'),
#     path('rides/<int:ride_id>/', views.get_ride, name='get_ride'),
#     path('rides/<int:ride_id>/update/', views.update_ride_status, name='update_ride_status'),
#     path('rides/<int:ride_id>/messages/', views.list_messages, name='list_messages'),
#     path('rides/<int:ride_id>/messages/add/', views.add_message, name='add_message'),
#     path('api/rides/create/', RequestRideView.as_view(), name='create-ride'),
#     path('api/driver/<int:pk>/update-location/', UpdateCurrentRetrieveDriverLocationForRideView.as_view(), name='update-driver-location'),
#     path('api/ride/active/driver-location/', RetrieveDriverLocationForUserView.as_view(), name='get-driver-location'),
#     path('api/driver/status-update/', UpdateDriverAvailabilityStatusView.as_view(), name='driver-status-update'),
#     path('api/drivers/active/', ListActiveDriversView.as_view(), name='active-drivers-list'),
#     path('api/rides/active/', ListListUserActiveRidesView.as_view(), name='active-rides-list'),
#     path('api/user/rides/active/', ListUserActiveRidesView.as_view(), name='user-active-rides'),
#     path('api/rides/<int:ride_id>/', RideDetailsView.as_view(), name='ride-detail'),
#     path('api/rides/<int:ride_id>/driver-location/', RetrieveDriverLocationForRideView.as_view(), name='driver-location'),
#     path('api/drivers/rides/available/', ListAvailableRidesForDriverView.as_view(), name='available-rides-for-drivers'),
#     path('api/rides/accept/<int:ride_id>/', AcceptAvailableRideView.as_view(), name='accept-ride'),

# ]

