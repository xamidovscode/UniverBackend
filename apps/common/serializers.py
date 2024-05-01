from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from ..common import models
from rest_framework import serializers


class FloorListSerializer(ModelSerializer):

    class Meta:
        model = models.Floor
        fields = (
            "id",
            "name",
        )



