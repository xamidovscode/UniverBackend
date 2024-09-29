from rest_framework import generics, views, viewsets, status
from rest_framework.response import Response
from . import serializers, models
from ..common import models as common
from rest_framework import permissions

class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        user = models.User.objects.get(phone=phone)
        data = {
            'tokens': user.tokens(),
            'roles': user.roles,
            'status': user.status,
            'phone': str(user.phone)
        }
        return Response(data, status=status.HTTP_200_OK)


class CreateStudentWithApartmentAPIView(generics.CreateAPIView):
    serializer_class = serializers.StudentSerializer


class StudentsListAPIView(generics.ListAPIView):
    queryset = models.User.objects.filter(role='student')
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        pk = self.request.query_params.get('pk')
        queryset = self.queryset
        if pk:
            users_pk = common.UserApartment.objects.filter(
                status="active", apartment_id=pk).values_list('student__id', flat=True)
            queryset = queryset.filter(id__in=users_pk)
        return queryset


class EmployeeListAPIView(generics.ListAPIView):
    queryset = models.User.objects.filter(role='employee')
    serializer_class = serializers.EmployeeListSerializer
