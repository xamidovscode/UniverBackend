from rest_framework import generics, views, viewsets
from rest_framework.response import Response
from . import serializers, models


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        user = models.User.objects.get(phone=phone)
        return Response(user.tokens())

