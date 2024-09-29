import uuid
from datetime import datetime
from rest_framework.exceptions import ValidationError

from utils.custom_filter import FloorFilter
from .models import Application
from ..common import models as common
from rest_framework import generics, filters, viewsets
from ..common import serializers
from django_filters.rest_framework import DjangoFilterBackend
from ..users.permissions import IsStudent
from rest_framework.response import Response
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.http import HttpResponse


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
        date_str = self.request.query_params.get("date")
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValidationError({"date": "unsupported format"})
            else:
                queryset = common.Attendance.objects.filter(date__year=date.year, date__month=date.month)
        else:
            date = datetime.today().date()
            queryset = common.Attendance.objects.filter(date__year=date.year, date__month=date.month)
        return queryset


class StudentAttendanceListAPIView(generics.ListAPIView):
    serializer_class = serializers.AttendanceUpdateSerializer
    pagination_class = None
    queryset = common.Attendance.objects.filter()
    permission_classes = [IsStudent]

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




class GenerateApplicationAPIView(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = serializers.ApplicationCreateSerializer
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Application.objects.filter(pk=pk, status='approved').first()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return Response({'msg': 'Application not found or not approved'}, status=404)

        context = {
            'pk': obj.pk,
            'first_name': obj.user_apartment.student.first_name,
            'reason': obj.reason,
            'created_at': obj.created_at.date(),
            'responsible': obj.admin.first_name,
            'status': 'TASDIQLANDI'
        }

        html_string = render_to_string('test.html', context)
        html = HTML(string=html_string)
        result = html.write_pdf(base_url=request.build_absolute_uri())

        filename = f'{uuid.uuid4()}-application.pdf'

        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Transfer-Encoding'] = 'binary'

        return response

class StudentApplicationListAPIView(generics.ListAPIView):
    serializer_class = serializers.StudentApplicationsSerializer
    queryset = common.Application.objects.all()
    permission_classes = [IsStudent]

    def get_queryset(self):
        return self.queryset.filter(user_apartment__student=self.request.user).order_by("-id")


class ApplicationsListAPIView(generics.ListAPIView):
    serializer_class = serializers.StudentApplicationsSerializer
    queryset = common.Application.objects.all()


class ApplicationUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.ApplicationUpdateSerializer
    queryset = common.Application.objects.all().exclude(status='approved')
    lookup_field = 'pk'
    http_method_names = ("patch",)


class StudentPaymentViewSets(viewsets.ModelViewSet):
    queryset = common.StudentPayments.objects.all()
    serializer_class = serializers.StudentPaymentsSerializer

