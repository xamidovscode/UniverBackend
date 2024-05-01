from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from ..common import models
from rest_framework import serializers


class FloorListSerializer(ModelSerializer):
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = models.Floor
        fields = (
            "id",
            "name",
            "rooms",
        )

    def get_rooms(self, obj):
        queryset = models.Floor.objects.filter(parent=obj)
        serializer = FloorListSerializer(queryset, many=True)
        for i in serializer.data:
            i.pop('rooms')
        return serializer.data


