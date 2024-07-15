from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from ..users import models as users
from ..common import models as common


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
    apartment = serializers.PrimaryKeyRelatedField(
        queryset=common.Floor.objects.filter(parent__isnull=False),
        required=True, write_only=True
    )

    class Meta:
        model = users.User
        fields = (
            'id',
            'phone',
            'password',
            'first_name',
            'apartment',
            'group',
        )

    def validate(self, attrs):
        apartment_id = attrs['apartment']
        group = attrs.get('group')
        if not group:
            raise serializers.ValidationError({"group": "Guruh tanlash shart"})
        apartment = common.UserApartment.objects.filter(status='active', apartment__id=apartment_id.id).count()
        if apartment >= 6:
            raise serializers.ValidationError({"apartment": "Bu xonada oquvchilar soni 6 ta"})
        return attrs

    def create(self, validated_data):
        apartment = validated_data.pop("apartment")
        validated_data['status'] = 'active'
        instance = super().create(validated_data)
        common.UserApartment.objects.create(
            student=instance, apartment=apartment
        )
        return instance


class EmployeeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = users.User
        fields = (
            'id',
            'first_name',
            'phone',
            'first_name'
        )
