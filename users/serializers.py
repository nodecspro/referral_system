from rest_framework import serializers
from .models import User

class PhoneSerializer(serializers.Serializer):
    """
    Сериализатор для валидации номера телефона,
    приходящего в POST-запросе.
    """
    phone_number = serializers.CharField(max_length=15, required=True)

    class Meta:
        fields = ['phone_number']
        
class VerifyCodeSerializer(serializers.Serializer):
    """
    Сериализатор для валидации 4-значного кода авторизации.
    """
    code = serializers.CharField(max_length=4, required=True)

    class Meta:
        fields = ['code']
        
class ReferredUserSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для отображения номеров телефонов
    приглашенных пользователей.
    """
    class Meta:
        model = User
        fields = ['phone_number']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения полного профиля пользователя.
    """
    referred_users = ReferredUserSerializer(many=True, read_only=True)

    activated_invite_code = serializers.CharField(
        source='activated_invite_from.invite_code',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'phone_number',
            'invite_code',
            'activated_invite_code',
            'referred_users',
        ]
        
class ActivateInviteCodeSerializer(serializers.Serializer):
    """
    Сериализатор для валидации инвайт-кода, который
    пользователь вводит для активации.
    """
    invite_code = serializers.CharField(max_length=6, required=True)

    class Meta:
        fields = ['invite_code']