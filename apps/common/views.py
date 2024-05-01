from django.shortcuts import render
from ..common import models as common
from rest_framework import generics
from ..common import serializers


class FloorListAPIView(generics.ListAPIView):
    queryset = common.Floor.objects.filter(parent__isnull=True)
    serializer_class = serializers.FloorListSerializer

