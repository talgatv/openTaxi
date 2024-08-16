from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Ride, Location, Message
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
# Другие необходимые импорты

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Ride, RideStatusChange


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from users.models import Driver, CustomUser
from .serializers import DriverLocationSerializer, DriverStatusSerializer, RideSerializer, ActiveDriverSerializer, CreateRideSerializer, ActiveRideUserSerializer , ActiveRideSerializer
from django.db.models import Q
from functools import wraps

import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import status
# from rest_framework.response import Response
# from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication


# def check_driver_user(view_func):
#     @wraps(view_func)
#     def _wrapped_view(view, request, *args, **kwargs):
#         user = request.user
#         if isinstance(user, Driver):
#             return view_func(view, request, *args, **kwargs)
#         else:
#             return Response({"error": "Access denied. Only drivers are allowed."}, status=403)
#     return _wrapped_view

# def check_custom_user(view_func):
#     @wraps(view_func)
#     def _wrapped_view(view, request, *args, **kwargs):
#         print('Пользователь кастомер')
#         user = request.user
#         print("Тип пользователя:", type(user))  # Отладочный вывод
#         if isinstance(user, CustomUser):
#             print('Пользователь кастомер прошел проверку')
#             return view_func(view, request, *args, **kwargs)
#         else:
#             return Response({"error": "Access denied. Only custom users are allowed."}, status=403)
#     return _wrapped_view


# def check_custom_user(view_func):
#     @wraps(view_func)
#     def _wrapped_view(view, request, *args, **kwargs):
#         user = request.user
#         try:
#             custom_user = CustomUser.objects.get(user=user)
#             return view_func(view, request, *args, **kwargs)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Access denied. Only custom users are allowed."}, status=403)
#     return _wrapped_view

# def check_custom_user(view_func):
#     print('проверка что это юзер')
#     print('проверка что это юзер')
#     print('проверка что это юзер')
#     print('проверка что это юзер')
#     @wraps(view_func)
#     def _wrapped_view(view, request, *args, **kwargs):
#         user = request.user
#         print(request.user)
#         print(request.user.__dict__)
#         # Проверяем, есть ли у пользователя атрибуты CustomUser
#         # if hasattr(user, 'profile_photo') or hasattr(user, 'date_joined'):
#         if hasattr(user, 'is_customuser') :
#             return view_func(view, request, *args, **kwargs)
#         else:
#             return Response({"error": "Access denied. Only custom users are allowed."}, status=403)
#     return _wrapped_view


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

class IsDriverPermission(permissions.BasePermission):
    """
    Проверяет, является ли пользователь водителем, на основе данных в JWT токене.
    """

    def has_permission(self, request, view):
        # Аутентификация пользователя через JWT
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request)
        raw_token = jwt_auth.get_raw_token(header)
        
        # Попытка декодирования токена и проверка на ошибки
        try:
            validated_token = jwt_auth.get_validated_token(raw_token)
        except Exception as e:  # Ловим все исключения для простоты, можно уточнить тип
            # Можно залогировать e для отладки
            return False
        
        # Извлечение данных о роли пользователя из Payload токена
        is_driver = validated_token.get('is_driver', False)
        
        # Возвращает True, если пользователь является водителем, иначе False
        return is_driver

@require_http_methods(["GET"])
def list_rides(request):
    rides = Ride.objects.all()
    rides_data = [{"id": ride.id, "start": ride.start_location, "end": ride.end_location} for ride in rides]
    return JsonResponse(rides_data, safe=False)

@require_http_methods(["POST"])
def add_ride(request):
    # Логика для обработки данных запроса и создания новой поездки
    return HttpResponse("New ride added")

@require_http_methods(["GET"])
def get_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        ride_data = {"id": ride.id, "start": ride.start_location, "end": ride.end_location}
        return JsonResponse(ride_data)
    except ObjectDoesNotExist:
        return HttpResponse("Ride not found", status=404)

@require_http_methods(["POST"])
def update_ride_status(request, ride_id):
    # Логика для обновления статуса поездки
    return HttpResponse("Ride status updated")

@require_http_methods(["GET"])
def list_messages(request, ride_id):
    try:
        messages = Message.objects.filter(ride_id=ride_id)
        messages_data = [{"sender": message.sender.id, "receiver": message.receiver.id, "content": message.content, "timestamp": message.timestamp} for message in messages]
        return JsonResponse(messages_data, safe=False)
    except ObjectDoesNotExist:
        return HttpResponse("Messages not found", status=404)

@require_http_methods(["POST"])
def add_message(request, ride_id):
    # Логика для обработки данных запроса и добавления нового сообщения
    return HttpResponse("Message added")


# class RequestRideView(APIView):
#     permission_classes = [IsAuthenticated]

#     # @check_custom_user
#     def post(self, request):
#         print('пришел запрос на создание поездки')
#         print('пришел запрос на создание поездки')
#         print('пришел запрос на создание поездки')
#         print('пришел запрос на создание поездки')
#         print('User:', request.user)
#         serializer = CreateRideSerializer(data=request.data)

#         if serializer.is_valid():
#             print("прошел проверку, а юзер:", request.user)
#             serializer.save(user=request.user, status='requested')  # Сохраняем заказ с привязкой к текущему пользователю
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def is_driver_token_matches(request_user, provided_token):
    try:
        # Проверяем, является ли пользователь водителем
        driver = Driver.objects.get(id=request_user.id)

        # Генерация нового токена для пользователя
        new_token = str(RefreshToken.for_user(driver).access_token)

        # Декодирование обоих токенов
        decoded_new_token = jwt.decode(new_token, settings.SECRET_KEY, algorithms=["HS256"])
        decoded_provided_token = jwt.decode(provided_token, settings.SECRET_KEY, algorithms=["HS256"])

        # Сравнение идентификаторов пользователя в токенах
        return decoded_new_token['user_id'] == decoded_provided_token['user_id']
    except Driver.DoesNotExist:
        # Пользователь не является водителем
        return False
    except jwt.PyJWTError:
        # Ошибка при декодировании токенов
        return False


class RequestRideView(APIView):
    """ Пассажиры создают запрос на поездку. Открытый запрос, который водитель может выбрать. """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('пришел запрос на создание поездки')
        print('пришел запрос на создание поездки')
        print('пришел запрос на создание поездки')
        print('пришел запрос на создание поездки')
        print('User:', request.user)
        serializer = CreateRideSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(status='requested')  # Сохраняем заказ с привязкой к текущему пользователю
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateCurrentRetrieveDriverLocationForRideView(APIView):
    """ Водители отправляют свои текущие координаты """
    permission_classes = [IsAuthenticated, IsDriverPermission]

   
    def patch(self, request):
        driver = request.user
        # if not isinstance(driver, Driver) or driver.id != pk:
        #     return Response({"error": "You can only update your own location"}, status=status.HTTP_403_FORBIDDEN)

        serializer = DriverLocationSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RetrieveDriverLocationForUserView(APIView):
    """ Пассажиры узнают координаты водителя для конкретной поездки """
    # for user
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_rides = Ride.objects.filter(user=request.user, status='active').first()
        if not user_rides:
            return Response({"error": "No active rides found"}, status=status.HTTP_404_NOT_FOUND)

        driver = user_rides.driver
        if not driver:
            return Response({"error": "No driver assigned to the ride"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DriverLocationSerializer(driver)
        return Response(serializer.data)


class UpdateDriverAvailabilityStatusView(APIView):
    """ Водители обновляют свой статус (занят, на перерыве и т.д.). """
    permission_classes = [IsAuthenticated, IsDriverPermission]

   
    def patch(self, request):
        driver = request.user
        if not isinstance(driver, Driver):
            return Response({"error": "Only drivers can change their status"}, status=status.HTTP_403_FORBIDDEN)

        serializer = DriverStatusSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListActiveDriversView(APIView):
    """ Список всех активных водителей в системе """
    def get(self, request):
        active_drivers = Driver.objects.filter(is_active_driver=True)
        serializer = ActiveDriverSerializer(active_drivers, many=True)
        return Response(serializer.data)


class ListListUserActiveRidesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # active_rides = Ride.objects.filter(user=request.user, status='requested')
        active_rides = Ride.objects.filter(
            Q(user=request.user) &
            (Q(status='requested') | Q(status='in_progress'))
        )
        serializer = ActiveRideUserSerializer(active_rides, many=True)
        return Response(serializer.data)


class RideDetailsView(APIView):
    """ Пассажиры могут узнать подробности об активной поездке. """
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        ride = Ride.objects.filter(id=ride_id, user=request.user, status='in_progress').first()
        if ride:
            serializer = ActiveRideSerializer(ride)
            return Response(serializer.data)
        return Response({"error": "No ride found or access denied"}, status=status.HTTP_404_NOT_FOUND)


class ListUserActiveRidesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        active_rides = Ride.objects.filter(user=request.user, status='in_progress')
        serializer = ActiveRideSerializer(active_rides, many=True)
        return Response(serializer.data)


class RetrieveDriverLocationForRideView(APIView):
    """ Пассажиры узнают координаты водителя для конкретной поездки id поездк """
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        ride = Ride.objects.filter(id=ride_id, user=request.user, status='in_progress').first()
        if not ride:
            return Response({"error": "No active ride found or access denied"}, status=status.HTTP_404_NOT_FOUND)

        driver = ride.driver
        if not driver:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DriverLocationSerializer(driver)
        return Response(serializer.data)

class ListAvailableRidesForDriverView(APIView):
    """ Водители просматривают список доступных для принятия поездок """
    permission_classes = [IsAuthenticated, IsDriverPermission]

    
    def get(self, request):
        rides = Ride.objects.filter(status='requested', driver__isnull=True)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)


class AcceptAvailableRideView(APIView):
    """ Водители могут принять доступную поездку, отправив запрос на конкретный ID поездки """
    permission_classes = [IsAuthenticated, IsDriverPermission]

    
    def post(self, request, ride_id):
        print('IIID поездки:', ride_id)
        ride = get_object_or_404(Ride, id=ride_id)

        # Проверяем, что поездка еще не принята другим водителем
        if ride.driver is not None:
            return Response({"error": "This ride has already been accepted by another driver."}, status=400)

        # Проверяем, что пользователь является водителем
        # if not hasattr(request.user, 'car_make'):  # Здесь 'driver_profile' должен быть вашим способом определения водителя
        #     print('request.user', request.user)
        request_token = request.headers.get('Authorization', '').split(' ')[-1]
        # request_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        if is_driver_token_matches(request.user, request_token):
            this_user = Driver.objects.get(id=request.user.id)
        else:
            raise PermissionDenied("You do not have permission to perform this action.")

        # Присваиваем текущего пользователя в качестве водителя поездки
        ride.driver = this_user
        ride.status='in_progress'
        ride.save()

        return Response({"message": "Ride accepted successfully."})


class DriverCurrentRideView(APIView):
    permission_classes = [IsAuthenticated, IsDriverPermission]

   
    def get(self, request):
        # Проверяем, является ли пользователь водителем
        # request_token = request.headers.get('Authorization', '').split(' ')[-1]
        # if is_driver_token_matches(request.user, request_token):
        this_user = Driver.objects.get(id=request.user.id)
        # else:
        #     raise PermissionDenied("You do not have permission to perform this action.")

        # if not hasattr(request.user, 'driver_profile'):  # Предполагается, что у водителя есть 'driver_profile'
        #     raise PermissionDenied("You are not a driver.")

        # Список активных статусов поездки
        active_statuses = ['accepted', 'arrived', 'waiting_for_passenger', 'in_progress', 'travelling']

        # Получаем активную поездку для водителя
        current_ride = Ride.objects.filter(driver=this_user, status__in=active_statuses).first()
        
        # Если у водителя нет активных поездок
        if not current_ride:
            return Response({"message": "No active rides."})

        # Обновление статуса других поездок водителя на 'completed'
        other_rides = Ride.objects.filter(driver=this_user).exclude(id=current_ride.id)
        other_rides.update(status='completed')

        # Возвращаем данные активной поездки
        data = {
            'ride_id': current_ride.id,
            'start_location': current_ride.start_location,
            'end_location': current_ride.end_location,
            'start_name_location': current_ride.start_name_location,
            'end_name_location': current_ride.end_name_location,
            'status': current_ride.status,
            # Добавьте другие необходимые поля
        }
        return Response(data)





class CancelRideView(APIView):
    """ НЕ используется, Позволяет пассажирам отменить запланированную поездку """
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        ride = get_object_or_404(Ride, id=ride_id, user=request.user)  # Убедитесь, что поездка принадлежит пользователю

        # Проверяем, не начата ли уже поездка
        if ride.status not in ['requested', 'pending']:
            return Response({"error": "Ride cannot be cancelled at this stage."}, status=400)

        # Обновляем статус поездки на 'cancelled'
        ride.status = 'cancelled'
        ride.save()

        return Response({"message": "Ride cancelled successfully."})


class DriverArrivedView(APIView):
    permission_classes = [IsAuthenticated, IsDriverPermission]
    
    
    def post(self, request, ride_id):
        ride = get_object_or_404(Ride, id=ride_id, driver=Driver.objects.get(id=request.user.id))

        # Обновляем статус поездки на 'waiting_for_passenger'
        ride.status = 'waiting_for_passenger'
        ride.save()

        # Здесь можно добавить логику для уведомления пассажира

        return Response({"message": "Status updated to 'waiting for passenger'."})

class StartRideView(APIView):
    permission_classes = [IsAuthenticated, IsDriverPermission]


    def post(self, request, ride_id):
        ride = get_object_or_404(Ride, id=ride_id, driver=Driver.objects.get(id=request.user.id))

        # Проверяем, что текущий статус позволяет начать поездку
        if ride.status not in ['waiting_for_passenger', 'accepted']:
            return Response({"error": "Ride cannot be started at this stage."}, status=400)

        # Обновляем статус поездки на 'travelling'
        ride.status = 'travelling'
        ride.save()

        return Response({"message": "Ride has started."})


class CompleteRideView(APIView):
    permission_classes = [IsAuthenticated, IsDriverPermission]


    def post(self, request, ride_id):
        ride = get_object_or_404(Ride, id=ride_id, driver=Driver.objects.get(id=request.user.id))

        # Проверяем, что текущий статус позволяет завершить поездку
        if ride.status not in ['travelling']:
            return Response({"error": "Ride cannot be completed at this stage."}, status=400)

        # Обновляем статус поездки на 'completed'
        ride.status = 'completed'
        ride.save()

        return Response({"message": "Ride has been completed."})

class LastRideSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Найти последнюю запись в RideStatusChange с статусом 'completed' для текущего водителя
        last_status_change = RideStatusChange.objects.filter(
            ride__driver=Driver.objects.get(id=request.user.id), 
            status='completed'
        ).order_by('-changed_at').first()

        if not last_status_change:
            return Response({"error": "No completed rides found."}, status=404)

        # Получить поездку, связанную с этим изменением статуса
        last_ride = last_status_change.ride

        # Использование существующей функции для получения суммарной информации о поездке
        ride_data = self._collect_ride_data(last_ride)
        return Response(ride_data)

    def _collect_ride_data(self, ride):
        # Здесь должна быть реализация логики сбора данных о поездке
        # Можно использовать уже существующий код для сбора информации о поездке
        pass  # Замените это соответствующей логикой

# 5. **Заказы Такси**:
#    - +Создание нового заказа такси.
#    - Получение списка доступных заказов для водителей.
#    - Принятие заказа водителем.
#    - Обновление статуса заказа (например, в пути, завершен и т.д.).

# 6. **Отзывы и Рейтинги**:
#    - Оставление отзывов о поездке.
#    - Получение отзывов о водителе или пассажире.

# 7. **История Поездок**:
#    - Получение истории поездок пользователями или водителями.

# 8. **Уведомления**:
#    - Эндпоинты для отправки и получения уведомлений (например, о принятии заказа).

# Эти эндпоинты покроют большинство основных функций, необходимых для приложения такси. В зависимости от специфических требований вашего проекта, список может быть расширен или модифицирован.

