from rest_framework import serializers
from .models import Ride, Location
from users.models import Driver

# class RideSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ride
#         fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        # fields = ['id', 'user', 'start_location', 'end_location', 'created_at', 'status']
        fields = '__all__'

# class CreateRideSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ride
#         fields = [ 'user', 'start_location', 'end_location', 'start_name_location', 'end_name_location', 'driver']
#         #fields = '__all__'

class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['start_location', 'end_location', 'start_name_location', 'end_name_location', 'driver']
        extra_kwargs = {'driver': {'required': False}}
        # Здесь исключено поле 'user'

    # def create(self, validated_data):
    #     # Здесь мы предполагаем, что 'user' будет передан в качестве контекста сериализатора
    #     user = self.context['request'].user
    #     return Ride.objects.create(user=user, **validated_data)
    # def save(self, **kwargs):
    #     # Здесь kwargs['user'] будет передан из представления
    #     self.instance = Ride(**self.validated_data, **kwargs)
    #     self.instance.save()
    #     return self.instance
    def create(self, validated_data):
        # Получаем пользователя из контекста
        user = self.context['request'].user
        return Ride.objects.create(user=user, **validated_data)

class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['current_location', 'current_location_lat', 'current_location_long']

class DriverStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['is_active_driver']

class ActiveDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'username', 'current_location']

class ActiveRideUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'start_location', 'end_location', 'created_at', 'status', 'driver', 'start_name_location', 'end_name_location']
        # Добавьте дополнительные поля по необходимости

class ActiveRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'start_location', 'end_location', 'created_at', 'status']
        # Добавьте дополнительные поля по необходимости