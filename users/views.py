import random
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PhoneSerializer

class RequestAuthCodeView(APIView):
    """
    Представление для запроса 4-значного кода авторизации.
    Принимает POST-запрос с номером телефона.
    """
    def post(self, request, *args, **kwargs):
        # 1. Используем наш сериализатор для валидации данных из запроса
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Если валидация прошла, получаем номер телефона
        phone_number = serializer.validated_data['phone_number']

        # 3. Генерируем случайный 4-значный код
        auth_code = random.randint(1000, 9999)

        # 4. Временно сохраняем код и номер в сессии пользователя
        #    Это самый простой способ хранить временные данные без Redis/Celery
        request.session['phone_number'] = phone_number
        request.session['auth_code'] = auth_code
        # Устанавливаем время жизни сессии, например, 5 минут (300 секунд)
        request.session.set_expiry(300)

        # 5. Имитируем отправку кода с задержкой в 1-2 секунды
        time.sleep(2)

        # 6. Выводим код в консоль сервера (имитация отправки SMS)
        print(f"--- Код авторизации для {phone_number}: {auth_code} ---")

        # 7. Возвращаем успешный ответ
        return Response(
            {'message': 'Код авторизации отправлен.'},
            status=status.HTTP_200_OK
        )