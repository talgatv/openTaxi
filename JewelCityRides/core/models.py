from django.db import models
from django.conf import settings
import datetime
from users.models import Driver, CustomUser


class Location(models.Model):
    # Общие поля для всех пользователей
    user_type = models.CharField(max_length=50)  # 'driver' или 'customuser'
    user_id = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_type:
            if isinstance(self.user, Driver):
                self.user_type = 'driver'
            elif isinstance(self.user, CustomUser):
                self.user_type = 'customuser'
        super().save(*args, **kwargs)

    def __str__(self):
        user_type = 'Driver' if self.user_type == 'Driver' else 'Customer'
        return f"{user_type} Location - Latitude: {self.latitude}, Longitude: {self.longitude}, Updated: {self.updated_at}"

# class Ride(models.Model):
#     STATUS_CHOICES = [
#         ('requested', 'Requested'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#         ('unavailable', 'Unavailable')
#     ]

#     customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_rides', on_delete=models.CASCADE)
#     driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='driver_rides', null=True, blank=True, on_delete=models.SET_NULL)
#     start_location = models.ForeignKey(Location, related_name='ride_starts', on_delete=models.CASCADE)
#     end_location = models.ForeignKey(Location, related_name='ride_ends', on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
#     response_time = models.DurationField(default=datetime.timedelta(minutes=30))  # Длительность до начала поездки
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Ride from {self.start_location} to {self.end_location} by {self.customer}"



# class Ride(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     start_location = models.CharField(max_length=255)
#     end_location = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50, default='pending')
#     # Дополнительные поля по необходимости

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),   # Заказано
        ('accepted', 'Accepted'),     # Принято водителем
        ('arrived', 'Arrived'),       # Водитель прибыл
        ('waiting_for_passenger', 'Waiting for Passenger'),  # В ожидании пассажираы
        ('in_progress', 'In Progress'), # Водитель едет до пассажира
        ('travelling', 'Travelling'), # В пути с пассажиром
        ('completed', 'Completed'),   # Завершено
        ('cancelled', 'Cancelled'),   # Отменено
        ('unavailable', 'Unavailable')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Общее поле для пользователя
    start_location = models.CharField(max_length=255)  # Общее поле для начальной локации
    end_location = models.CharField(max_length=255)  # Общее поле для конечной локации
    start_name_location = models.CharField(max_length=255)  # Общее поле для начальной локации
    end_name_location = models.CharField(max_length=255)  # Общее поле для конечной локации
    created_at = models.DateTimeField(auto_now_add=True)  # Общее поле для даты создания
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='requested')  # Общее поле для статуса
    response_time = models.DurationField(default=datetime.timedelta(minutes=30))  # Длительность до начала поездки
    driver = models.ForeignKey(Driver, related_name='driver_rides', null=True, blank=True, on_delete=models.SET_NULL)

    
    # Дополнительные поля по необходимости
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride from {self.start_location} to {self.end_location} by {self.user}"


class DriverSchedule(models.Model):
    # driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    available_days = models.JSONField()  # Пример: {'friday': True, 'saturday': False, ...}
    available_hours = models.JSONField()  # Пример: {'friday': {'start': '20:00', 'end': '22:00'}}

    def __str__(self):
        return f"Schedule for {self.driver.username}"



class Message(models.Model):
    ride = models.ForeignKey('Ride', related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} for ride {self.ride.id} at {self.timestamp}"



class RideStatusChange(models.Model):
    ride = models.ForeignKey('Ride', on_delete=models.CASCADE, related_name='status_changes')
    status = models.CharField(max_length=21, choices=Ride.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='status_changes')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Ride {self.ride.id} changed to {self.status} by {self.changed_by} at {self.changed_at}"