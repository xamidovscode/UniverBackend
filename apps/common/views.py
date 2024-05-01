from ..common import models as common
from rest_framework import generics
from ..common import serializers


class FloorParentListAPIView(generics.ListCreateAPIView):
    queryset = common.Floor.objects.filter(parent__isnull=True)
    serializer_class = serializers.FloorListSerializer
    pagination_class = None


class FloorChildListAPIView(generics.ListAPIView):
    serializer_class = serializers.FloorListSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = common.Floor.objects.filter(parent__isnull=False, parent__id=self.kwargs.get('pk'))
        return queryset


class FloorUpdateAPIView(generics.UpdateAPIView):
    queryset = common.Floor.objects.all()
    serializer_class = serializers.FloorListSerializer
    lookup_field = 'pk'