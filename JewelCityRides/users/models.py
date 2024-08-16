from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Driver(AbstractUser):
    # Личная информация
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='driver_photos/', null=True, blank=True)

    # Информация о транспортном средстве
    car_make = models.CharField(max_length=255, blank=True, null=True)
    car_model = models.CharField(max_length=255, blank=True, null=True)
    car_year = models.IntegerField(blank=True, null=True)
    car_color = models.CharField(max_length=50, blank=True, null=True)
    license_plate = models.CharField(max_length=50, blank=True, null=True)

    # Лицензия и страховка
    license_number = models.CharField(max_length=50, blank=True, null=True)
    insurance_policy_number = models.CharField(max_length=50, blank=True, null=True)

    # Статус активности
    is_active_driver = models.BooleanField(default=True)

    # Рейтинг и отзывы
    rating = models.FloatField(default=0.0)

    # Геолокация
    current_location = models.CharField(max_length=255, null=True, blank=True)
    current_location_lat = models.CharField(max_length=255, null=True, blank=True)
    current_location_long = models.CharField(max_length=255, null=True, blank=True)

    # Рабочий график
    # Можно использовать JSONField или связанные модели для более сложных сценариев
    work_schedule = models.JSONField(null=True, blank=True)


    groups = models.ManyToManyField(
        Group,
        related_name="driver_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="driver_permissions",
        blank=True
    )


    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
        return self.full_name


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    rating = models.FloatField(default=0.0, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_customuser = models.BooleanField(default=True)


    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )

    class Meta:
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"

    def __str__(self):
        return self.full_name or self.username

