from datetime import datetime

from rest_framework.permissions import IsAuthenticated

from ..common import models as common
from rest_framework import generics, filters
from ..common import serializers
from django_filters.rest_framework import DjangoFilterBackend


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


class AttendanceUpdateAPIView(generics.UpdateAPIView):
    queryset = common.Attendance.objects.all()
    serializer_class = serializers.AttendanceUpdateSerializer
    lookup_field = 'pk'
    http_method_names = ('patch', )


class AttendanceFloorListAPIView(generics.ListAPIView):
    serializer_class = serializers.AttendanceUpdateSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ("apartment", 'date')
    queryset = common.Attendance.objects.filter()

    def get_queryset(self):
        date = datetime.today().date()
        queryset = common.Attendance.objects.filter(date=str(date))
        return queryset


class GroupCreateAPIView(generics.ListCreateAPIView):
    queryset = common.Group.objects.all()
    serializer_class = serializers.GroupSerializer


class ApplicationCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.ApplicationCreateSerializer
    permission_classes = [IsAuthenticated]

