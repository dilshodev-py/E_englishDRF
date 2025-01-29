import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
# from authentication.tasks import send_email
from authentication.serializers import RegisterSerializer


# Create your views here.
class RegisterAPIView(CreateView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        user = User.objects.filter(email=request.data.get("email")).first()
        if serializer.is_valid() or (user and not user.is_active):
            if not user:
                serializer.save()
            data = serializer.validated_data
            random_code = random.randrange(10 ** 5, 10 ** 6)
            email = data.get("email")
            # send_email.delay(email, random_code)
            response = Response("Tasdiqlash kodi jo'natildi !", status=HTTP_200_OK)
            response.set_cookie("verify", make_password(str(random_code)))
            return response
        elif user and user.is_active:
            return Response("Email oldin ro'yxatdan o'tgan !", status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

