from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from ..users import models as users


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = users.User.objects.filter(phone=attrs['phone']).first()
        if not user:
            raise serializers.ValidationError({"phone": "Bunday foydalanuvchi topilmadi"})
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": 'Parol xato kiritildi'})
        return attrs


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = users.User
        fields = (
            'id',
            'phone',
            'password',
        )

