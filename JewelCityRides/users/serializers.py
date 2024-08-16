from rest_framework import serializers
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import Driver, CustomUser
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

import jwt
from django.conf import settings



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавить кастомные данные в payload
        # Проверяем, существует ли связанный объект Driver для пользователя
        token['is_driver'] = hasattr(user, 'is_active_driver')
        # Проверяем, существует ли связанный объект CustomUser для пользователя
        # Предполагая, что у вас есть способ различать CustomUser как пассажира
        token['is_customuser'] = hasattr(user, 'is_customuser')  # Замените 'customuser_attribute' на реальный атрибут модели, если он есть

        return token


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # fields = ('username', 'password', 'full_name', 'phone_number', 'email', 'profile_photo')
        fields = ('username', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            # full_name=validated_data.get('full_name'),
            # phone_number=validated_data.get('phone_number'),
            # email=validated_data.get('email'),
            # Удалите или обновите следующую строку в зависимости от того, как вы храните фотографии
            # profile_photo=validated_data.get('profile_photo')
        )
        return user


class UserLoginSerializer_old(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            # is_driver = Driver.objects.filter(id=user.id).exists() if user.id else False
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'is_driver': False
            }
        raise serializers.ValidationError("Invalid credentials")


class UserLoginSerializer_old(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Проверяем, является ли пользователь водителем
        try:
            user = Driver.objects.get(username=username)
            if user.check_password(password):
                is_driver = True
                user_id = 0
                driver_id = user.id
            else:
                raise serializers.ValidationError("Invalid credentials")
        except Driver.DoesNotExist:
            # Проверяем, является ли пользователь обычным пользователем
            try:
                user = CustomUser.objects.get(username=username)

                if user.check_password(password):
                    is_driver = False
                    user_id = user.id
                    driver_id = 0
                else:
                    raise serializers.ValidationError("Invalid credentials")
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")

        # Если пользователь найден и активен
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            print('Отправляем данные логина')
            print('USER:', user)
            print(user.__dict__)
            print('refresh.access_token :', refresh.access_token)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user_id,
                'is_driver': is_driver,
                'driver_id': driver_id
            }

        # Если пользователь не найден или не активен
        raise serializers.ValidationError("Invalid credentials")


def create_custom_jwt(user, is_driver, user_id, driver_id):
    # Создаем refresh токен для пользователя
    refresh = RefreshToken.for_user(user)
    
    # Добавляем кастомные данные в payload токена
    refresh['is_driver'] = is_driver
    refresh['custom_user_id'] = user_id
    refresh['driver_id'] = driver_id
    refresh['is_customuser'] = not is_driver
    
    # Возвращаем refresh и access токены
    return str(refresh), str(refresh.access_token)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        user = None
        is_driver = False
        user_id = 0
        driver_id = 0

        # Попытка найти пользователя сначала в модели Driver, затем в CustomUser
        try:
            user = Driver.objects.get(username=username)
            is_driver = True
            driver_id = user.id
        except Driver.DoesNotExist:
            try:
                user = CustomUser.objects.get(username=username)
                user_id = user.id
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")

        if user and user.check_password(password):
            # Используем функцию для создания кастомного JWT
            refresh, access = create_custom_jwt(user, is_driver, user_id, driver_id)
            
            return {
                'refresh': refresh,
                'access': access,
                'is_driver': is_driver,
                'user_id': user_id,
                'driver_id': driver_id
            }
        
        raise serializers.ValidationError("Invalid credentials")

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'full_name', 'phone_number', 'car_make', 'car_model', 'car_year', 'car_color', 'license_plate', 'rating', 'current_location', 'is_active_driver']
        # Выберите поля, которые хотите включить в сериализацию




class DriverLocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['current_location']  # Ограничение только геолокацией

    def update(self, instance, validated_data):
        instance.current_location = validated_data.get('current_location', instance.current_location)
        instance.save()
        return instance


class DriverUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['full_name', 'phone_number', 'car_make', 'car_model', 'car_year', 'car_color', 'license_plate', 'rating', 'current_location', 'is_active_driver']
        # Укажите все поля, которые водитель может обновить

    def update(self, instance, validated_data):
        # Обновите все поля из validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# class ValidateTokenSerializer(serializers.Serializer):
#     token = serializers.CharField()

    # def validate_token(self, data):
    #     try:
    #         UntypedToken(data['token'])
    #     except (InvalidToken, TokenError):
    #         raise serializers.ValidationError("Invalid token")

    #     return data

# class ValidateTokenSerializer(serializers.Serializer):
#     token = serializers.CharField()

#     def validate(self, data):
#         token = data.get('token')
#         try:
#             decoded_data = UntypedToken(token)
#             is_valid = True
#         except (InvalidToken, TokenError):
#             is_valid = False
#             decoded_data = None

#         user_id = decoded_data['user_id'] if decoded_data else None
#         is_driver = Driver.objects.filter(id=user_id).exists() if user_id else False

#         return {'valid': is_valid, 'is_driver': is_driver}


User_model = get_user_model()

class ValidateTokenSerializer_old2(serializers.Serializer):
    token = serializers.CharField()
    # print('==== Проверка Валидация токена')

    def validate(self, data):
        print('ДАТА:',data)
        token = data.get('token')
        print('Токен: ', token)
        try:
            print('Проверка, юзер есть или нет')
            decoded_data = UntypedToken(token)
            is_valid = True
            user_id = decoded_data['user_id']
        except (InvalidToken, TokenError):
            is_valid = False
            user_id = None

        if user_id:
            try:

                user = User_model.objects.get(id=user_id)
                is_driver = hasattr(user, 'is_driver') and user.is_driver
                is_customuser = hasattr(user, 'is_customuser') and user.is_customuser
            except User_model.DoesNotExist:
                is_driver = False
                is_customuser = False
        else:
            is_driver = False
            is_customuser = False

        return {'valid': is_valid, 'is_driver': is_driver, 'is_customuser': is_customuser}

# class ValidateTokenSerializer(serializers.Serializer):
#     token = serializers.CharField()

#     def validate(self, data):
#         token = data.get('token')
#         print('ДАТА:',data)
#         print('Токен: ', token)


#         try:
#             # Декодирование токена
#             decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#             user_id = decoded_data['user_id']
#             is_valid = True
#         except jwt.ExpiredSignatureError:
#             # Обработка истекшего токена
#             return {'valid': False, 'error': 'Token expired'}
#         except jwt.InvalidTokenError:
#             # Обработка невалидного токена
#             return {'valid': False, 'error': 'Invalid token'}

#         try:
#             user = User.objects.get(id=user_id)
#             is_driver = hasattr(user, 'is_driver') and user.is_driver
#             is_customuser = hasattr(user, 'is_customuser') and user.is_customuser
#         except User.DoesNotExist:
#             is_driver = False
#             is_customuser = False

#         return {'valid': is_valid, 'is_driver': is_driver, 'is_customuser': is_customuser}


class ValidateTokenSerializer_old3(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data.get('token')
        try:
            # Декодирование токена
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_data['user_id']
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Invalid token'}

        # Проверяем сущестование и роль пользователя
        return self._check_user_role(user_id, token, decoded_data)

    def _check_user_role(self, user_id, token, decoded_data):
        # Проверка для CustomUser
        if self._compare_token_with_model(CustomUser, user_id, token, decoded_data):
            #todo: решить эту проблему, дело в том что я пока не разобрался как по токену отделить пользователя и водителя
            user_id = decoded_data['user_id']
            # username = decoded_data['username']
            print('=====decoded_data',decoded_data)
            return {'valid': True, 'is_driver': True, 'is_customuser': True}
        
        # Проверка для Driver
        elif self._compare_token_with_model(Driver, user_id, token, decoded_data):
            return {'valid': True, 'is_driver': True, 'is_customuser': False}
        
        return {'valid': False, 'error': 'Invalid user or token'}

    def _compare_token_with_model(self, model, user_id, token, decoded_data):
        try:
            user = model.objects.get(id=user_id)
            new_token = str(RefreshToken.for_user(user).access_token)
            decoded_new_token = jwt.decode(new_token, settings.SECRET_KEY, algorithms=["HS256"])
            # return jwt.decode(new_token, settings.SECRET_KEY, algorithms=["HS256"])['user_id'] == user_id
            return decoded_new_token['user_id'] == decoded_data['user_id'] 
        except model.DoesNotExist:
            return False
        except jwt.PyJWTError:
            return False

        # # Декодирование обоих токенов
        # decoded_new_token = jwt.decode(new_token, settings.SECRET_KEY, algorithms=["HS256"])
        # decoded_provided_token = jwt.decode(provided_token, settings.SECRET_KEY, algorithms=["HS256"])

        # # Сравнение идентификаторов пользователя в токенах
        # return decoded_new_token['user_id'] == decoded_provided_token['user_id']

class ValidateTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data.get('token')
        is_valid = False
        is_driver = False
        is_customuser = False

        try:
            # Декодирование токена без верификации подписи (для примера)
            # Важно: в продакшене рекомендуется проверять подпись токена!
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], )

            is_valid = True
            # Проверяем, содержит ли декодированный payload информацию о роли пользователя
            is_driver = decoded_data.get('is_driver', False)
            is_customuser = decoded_data.get('is_customuser', False)
            # is_driver = decoded_data['is_driver']
            # is_customuser = decoded_data['is_customuser']
        except jwt.ExpiredSignatureError:
            # Обработка истекшего токена
            raise serializers.ValidationError("Token expired")
        except jwt.InvalidTokenError:
            # Обработка невалидного токена
            raise serializers.ValidationError("Invalid token")

        return {'valid': is_valid, 'is_driver': is_driver, 'is_customuser': is_customuser, 'new' : 'yes'}

class DriverRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Driver
        fields = ['username', 'password', 'full_name', 'phone_number', 'car_make', 'car_model', 'car_year', 'car_color', 'license_plate', 'license_number', 'insurance_policy_number']
    
    def create(self, validated_data):
        user = Driver.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            car_make=validated_data['car_make'],
            car_model=validated_data['car_model'],
            car_year=validated_data['car_year'],
            car_color=validated_data['car_color'],
            license_plate=validated_data['license_plate'],
            license_number=validated_data['license_number'],
            insurance_policy_number=validated_data['insurance_policy_number'],
            is_active=False  # Создать водителя как неактивного
        )
        return user