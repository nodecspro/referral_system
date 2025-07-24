from rest_framework import serializers

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