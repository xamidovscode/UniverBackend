from rest_framework import generics, views, viewsets, status
from rest_framework.response import Response
from . import serializers, models
from ..common import models as common


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        user = models.User.objects.get(phone=phone)
        data = {
            'tokens': user.tokens(),
            'role': user.role,
            'status': user.status
        }
        return Response(data, status=status.HTTP_200_OK)


class CreateStudentWithApartmentAPIView(generics.CreateAPIView):
    serializer_class = serializers.StudentSerializer


class StudentsListAPIView(generics.ListAPIView):
    queryset = models.User.objects.filter(role='student')
    serializer_class = serializers.EmployeeListSerializer


class EmployeeListAPIView(generics.ListAPIView):
    queryset = models.User.objects.filter(role='employee')
    serializer_class = serializers.EmployeeListSerializer
