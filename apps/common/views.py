from datetime import datetime
from ..common import models as common
from rest_framework import generics, filters
from ..common import serializers
from django_filters.rest_framework import DjangoFilterBackend

from ..users.permissions import IsStudent


class FloorParentListAPIView(generics.ListCreateAPIView):
    queryset = common.Floor.objects.filter(parent__isnull=True, is_active=True)
    serializer_class = serializers.FloorListSerializer
    pagination_class = None


class FloorChildListAPIView(generics.ListAPIView):
    serializer_class = serializers.FloorListSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = common.Floor.objects.filter(
            parent__isnull=False,
            parent__id=self.kwargs.get('pk'),
            is_active=True
        )
        return queryset


class FloorUpdateAPIView(generics.UpdateAPIView):
    queryset = common.Floor.objects.all()
    serializer_class = serializers.FloorListSerializer
    lookup_field = 'pk'


class FloorDestroyAPIView(generics.DestroyAPIView):
    queryset = common.Floor.objects.all()
    serializer_class = serializers.FloorListSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


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
    permission_classes = [IsStudent]


class StudentApplicationListAPIView(generics.ListAPIView):
    serializer_class = serializers.StudentApplicationsSerializer
    queryset = common.Application.objects.all()
    permission_classes = [IsStudent]

    def get_queryset(self):
        return self.queryset.filter(user_apartment__student=self.request.user)
