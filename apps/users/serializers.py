from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from ..users.models import User


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(phone=attrs['phone']).first()
        if not user:
            raise serializers.ValidationError({"phone": "Bunday foydalanuvchi topilmadi"})
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": 'Parol xato kiritildi'})
        return attrs

