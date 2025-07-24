from rest_framework import serializers

class PhoneSerializer(serializers.Serializer):
    """
    Сериализатор для валидации номера телефона,
    приходящего в POST-запросе.
    """
    phone_number = serializers.CharField(max_length=15, required=True)

    class Meta:
        fields = ['phone_number']