# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Django REST Framework imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.views import TokenObtainPairView

# Standard library imports
import jwt
from functools import wraps

# App-specific imports
from .forms import DriverRegistrationForm
from .models import Driver, CustomUser
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomUserRegistrationSerializer,
    DriverRegistrationSerializer,
    DriverSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    ValidateTokenSerializer,
)

def is_driver(view_func):
    @wraps(view_func)
    def _wrapped_view(instance, request, *args, **kwargs):
        # Аутентификация пользователя через JWT
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request)
        raw_token = jwt_auth.get_raw_token(header)
        validated_token = jwt_auth.get_validated_token(raw_token)
        
        # Извлечение данных о роли пользователя из Payload токена
        is_driver = validated_token.get('is_driver', False)
        
        if not is_driver:
            # Если пользователь не водитель, возвращаем ошибку
            return Response({"error": "Only drivers can perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        # Если пользователь водитель, выполняем оригинальную функцию
        return view_func(instance, request, *args, **kwargs)
    
    return _wrapped_view


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ActiveDriversList(APIView):
    def get(self, request, format=None):
        active_drivers = Driver.objects.filter(is_active_driver=True)
        serializer = DriverSerializer(active_drivers, many=True)
        return Response(serializer.data)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_serializer = CustomTokenObtainPairSerializer(data={
                'username': request.data['username'], 
                'password': request.data['password']
            })

            # Проверка валидности данных пользователя для создания токенов
            if token_serializer.is_valid():
                refresh = token_serializer.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    # Добавьте любые другие данные, которые хотите вернуть после регистрации
                }
                return Response(data)
            else:
                return Response(token_serializer.errors, status=400)
        
        return Response(serializer.errors, status=400)

class CustomUserRegistrationView_old(APIView):
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_driver': False
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Вместо прямого создания токенов используем CustomTokenObtainPairSerializer
            # Это предполагает, что CustomTokenObtainPairSerializer уже настроен для работы с вашей логикой
            token_serializer = CustomTokenObtainPairSerializer.get_token(user)
            
            # Добавляем 'is_driver' вручную, если ваш CustomTokenObtainPairSerializer этого не делает
            # token['is_driver'] = user.is_driver  # Пример, как это может быть реализовано внутри CustomTokenObtainPairSerializer

            return Response({
                'refresh': str(token_serializer),
                'access': str(token_serializer.access_token),
                # 'is_driver': user.is_driver  # Это если вы хотите добавить флаг вручную
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)



class DriverStatusUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, *args, **kwargs):
        # Применяем декоратор к обработчику запроса
        return is_driver(super(DriverLocationUpdate, self).dispatch)(*args, **kwargs)

    def patch(self, request, format=None):
        driver = request.user
        if not isinstance(driver, Driver):
            return Response({"error": "Only drivers can change their status"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DriverSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # class Meta:
    #     model = Driver
    #     fields = ['is_active_driver']  # Ограничение только статусом активности

    def update(self, instance, validated_data):
        instance.is_active_driver = validated_data.get('is_active_driver', instance.is_active_driver)
        instance.save()
        return instance




class DriverLocationUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, *args, **kwargs):
        # Применяем декоратор к обработчику запроса
        return is_driver(super(DriverLocationUpdate, self).dispatch)(*args, **kwargs)

    def patch(self, request, format=None):
        driver = request.user
        if not isinstance(driver, Driver):
            return Response({"error": "Only drivers can update their location"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DriverLocationUpdateSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, *args, **kwargs):
        # Применяем декоратор к обработчику запроса
        return is_driver(super(DriverLocationUpdate, self).dispatch)(*args, **kwargs)

    def patch(self, request, format=None):
        driver = request.user
        if not isinstance(driver, Driver):
            return Response({"error": "Only drivers can update their information"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = DriverUpdateSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ValidateTokenView(APIView):
#     permission_classes = [AllowAny]

    # def post(self, request):
    #     token = request.data.get('token')
    #     try:
    #         UntypedToken(token)
    #         return Response({'valid': True})
    #     except (InvalidToken, TokenError) as e:
    #         return Response({'valid': False, 'error': str(e)})

class ValidateTokenView(APIView):
    # permission_classes = [AllowAny]
    print('ValidateTokenView ')

    def post(self, request):
        print('Проверка токена пользователя')
        serializer = ValidateTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({
        #         'refresh': '2222hhh',
        #         'access': 'ksds'
        #     })




# @csrf_exempt
# @require_http_methods(["POST"])
# def validate_token(request):
#     token = request.headers.get('Authorization', '').split(' ')[-1]
#     print('request:', request)
#     print('request.__dict__:', request.__dict__)
#     # token = request.data.get('token')
#     try:
#         # Декодирование токена
#         decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         user_id = decoded_data.get('user_id')
#         user_model = get_user_model()
#         print('== user_id:',user_id)

#         # Проверка, является ли пользователь водителем или customUser
#         try:
#             user = user_model.objects.get(id=user_id)
#             is_driver = hasattr(user, 'driver_profile')  # Предположим, у вас есть профиль водителя
#             is_customuser = not is_driver  # Если это не водитель, предполагаем, что это customUser
#             return JsonResponse({'valid': True, 'is_driver': is_driver, 'is_customuser': is_customuser})
#         except user_model.DoesNotExist:
#             return JsonResponse({'valid': False, 'error': 'User does not exist'}, status=400)

#     except jwt.ExpiredSignatureError:
#         return JsonResponse({'valid': False, 'error': 'Signature has expired'}, status=400)
#     except jwt.DecodeError:
#         return JsonResponse({'valid': False, 'error': 'Error decoding signature'}, status=400)







User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def validate_token(request):
    provided_token = request.headers.get('Authorization', '').split(' ')[-1]

    try:
        # Декодирование JWT токена
        decoded_data = jwt.decode(provided_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data['user_id']

        # Проверка наличия CustomUser с таким user_id
        try:
            custom_user = CustomUser.objects.get(id=user_id)
            # return JsonResponse({'valid': True, 'user_type': 'customuser'})

            # Генерация нового токена для пользователя
            new_token = str(RefreshToken.for_user(custom_user).access_token)

            # Декодирование обоих токенов
            decoded_new_token = jwt.decode(new_token, settings.SECRET_KEY, algorithms=["HS256"])
            decoded_provided_token = jwt.decode(provided_token, settings.SECRET_KEY, algorithms=["HS256"])

            # Сравнение идентификаторов пользователя в токенах
            if decoded_new_token['user_id'] == decoded_provided_token['user_id'] :
                return JsonResponse({'valid': True, 'user_type': 'customuser'})


        except Driver.DoesNotExist:
            pass  # Продолжаем проверку для Driver

        except jwt.PyJWTError:
            # Ошибка при декодировании токенов
            return JsonResponse({'valid': False, 'error': 'Signature has expired'}, status=400)

        # Проверка наличия Driver с таким user_id
        # try:
        #     driver = Driver.objects.get(id=user_id)
        #     return JsonResponse({'valid': True, 'user_type': 'driver'})


        # Проверка наличия CustomUser с таким user_id
        try:
            # custom_user = CustomUser.objects.get(id=user_id)
            # return JsonResponse({'valid': True, 'user_type': 'customuser'})
            driver = Driver.objects.get(id=user_id)

            # Генерация нового токена для пользователя
            new_token = str(RefreshToken.for_user(driver).access_token)

            # Декодирование обоих токенов
            decoded_new_token = jwt.decode(new_token, settings.SECRET_KEY, algorithms=["HS256"])
            decoded_provided_token = jwt.decode(provided_token, settings.SECRET_KEY, algorithms=["HS256"])

            # Сравнение идентификаторов пользователя в токенах
            if decoded_new_token['user_id'] == decoded_provided_token['user_id'] :
                return JsonResponse({'valid': True, 'user_type': 'driver'})


        except Driver.DoesNotExist:
            pass  # Продолжаем проверку для Driver

        except Driver.DoesNotExist:
            pass  # Пользователь не найден

        # Если ни один из пользователей не найден
        return JsonResponse({'valid': False, 'error': 'User not found'}, status=404)

    except jwt.ExpiredSignatureError:
        return JsonResponse({'valid': False, 'error': 'Signature has expired'}, status=400)
    except jwt.DecodeError:
        return JsonResponse({'valid': False, 'error': 'Error decoding signature'}, status=400)

        

class DriverRegistrationView(APIView):
    def post(self, request):
        serializer = DriverRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Driver registered successfully. Pending approval."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DjDriverRegistrationView(generic.CreateView):
    form_class = DriverRegistrationForm
    success_url = reverse_lazy('login')  # Или другой URL для перенаправления после регистрации
    template_name = 'driver_register.html'

# -Аутентификация и Регистрация:

# Регистрация новых пользователей/водителей.
# Вход в систему (получение токена JWT).


# -Профиль Пользователя/Водителя:

# Получение информации о профиле.
# Обновление профиля пользователя/водителя.


# -Управление Статусом Водителя:

# Обновление статуса активности водителя (активный/неактивный).


# -Управление Геолокацией:

# Обновление текущего местоположения водителя.