from datetime import datetime
from rest_framework.exceptions import ValidationError
from utils.custom_filter import FloorFilter
from ..common import models as common
from rest_framework import generics, filters, viewsets
from ..common import serializers
from django_filters.rest_framework import DjangoFilterBackend
from ..users.permissions import IsStudent


class FloorViewSets(viewsets.ModelViewSet):
    queryset = common.Floor.objects.filter(parent__isnull=True, is_active=True)
    serializer_class = serializers.FloorListSerializer
    pagination_class = None
    filterset_class = FloorFilter

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()



class RoomsListAPIView(generics.ListAPIView):
    serializer_class = serializers.FloorListSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = common.Floor.objects.filter(
            parent__isnull=False,
            parent__id=self.kwargs.get('pk'),
            is_active=True
        )
        return queryset


class RoomDestroyAPIView(generics.DestroyAPIView):
    serializer_class = serializers.FloorListSerializer
    queryset = common.Floor.objects.filter(
        parent__isnull=False,
        is_active=True
    )
    pagination_class = None

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
        queryset = common.Attendance.objects.filter(date__year=date.year, date__month=date.month)
        return queryset


class StudentAttendanceListAPIView(generics.ListAPIView):
    serializer_class = serializers.AttendanceUpdateSerializer
    pagination_class = None
    queryset = common.Attendance.objects.filter()

    def get_queryset(self):
        date_str = self.request.query_params.get("date")
        user = self.request.user
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValidationError({"date": "unsupported format"})
            else:
                queryset = common.Attendance.objects.filter(date__year=date.year, date__month=date.month, student=user)
        else:
            date = datetime.today().date()
            queryset = common.Attendance.objects.filter(date__year=date.year, date__month=date.month, student=user)
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


class StudentPaymentViewSets(viewsets.ModelViewSet):
    queryset = common.StudentPayments.objects.all()
    serializer_class = serializers.StudentPaymentsSerializer

