import random
import string
import time
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    PhoneSerializer,
    VerifyCodeSerializer,
    UserProfileSerializer,
)

User = get_user_model()

def generate_invite_code():
    """Генерирует уникальный 6-значный инвайт-код."""
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not User.objects.filter(invite_code=code).exists():
            return code

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
    
class VerifyCodeView(APIView):
    """
    Представление для проверки кода и авторизации/регистрации пользователя.
    """
    def post(self, request, *args, **kwargs):
        # Проверяем, есть ли данные в сессии
        if 'phone_number' not in request.session or 'auth_code' not in request.session:
            return Response(
                {'error': 'Сессия истекла или не была начата.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сравниваем код из запроса с кодом из сессии
        if str(request.session['auth_code']) != serializer.validated_data['code']:
            return Response(
                {'error': 'Неверный код авторизации.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = request.session['phone_number']

        # Находим пользователя или создаем нового
        user, created = User.objects.get_or_create(phone_number=phone_number)

        # Если пользователь новый, генерируем и присваиваем ему инвайт-код
        if created:
            user.invite_code = generate_invite_code()
            user.save()

        # Генерируем JWT токены для пользователя
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # Очищаем сессию после успешного входа
        request.session.flush()

        return Response(tokens, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    """
    Представление для просмотра и частичного обновления профиля пользователя.
    Доступно только аутентифицированным пользователям.
    """
    # Требуем, чтобы пользователь был аутентифицирован (предоставил валидный токен)
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для получения данных профиля.
        """
        # request.user будет содержать экземпляр текущего пользователя
        # благодаря JWTAuthentication и IsAuthenticated.
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)