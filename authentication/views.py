import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
# from authentication.tasks import send_email
from authentication.serializers import RegisterSerializer

from drf_spectacular.utils import extend_schema
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_202_ACCEPTED
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import ForgotPasswordSerializer, ForgotPasswordCheckSerializer


# from authentication.tasks import send_email
import random
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from authentication.serializers import EmailSerializer

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


class SendRandomNumberAPIView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            random_number = random.randint(1000, 9999)

            subject = "Sizning tasdiqlash kodingiz"
            message = f"Sizning tasdiqlash kodingiz: {random_number}"
            from_email = settings.EMAIL_HOST_USER

            try:
                send_mail(subject, message, from_email, [email])
                return Response({"message": "Email muvaffaqiyatli yuborildi!", "code": random_number},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['auth'], request=ForgotPasswordSerializer)
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        s = ForgotPasswordSerializer(data=data)
        if s.is_valid():
            email = s.validated_data.get('email')
            code = randint(10000, 99999)
            # send_email.delay(email=email, code=code)
            response = JsonResponse({"message": "Code send to your email!", "email": email}, status=HTTP_200_OK)
            response.set_cookie("code", str(code), max_age=300)
            return response
        return JsonResponse(s.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], request=ForgotPasswordCheckSerializer)
class ForgotPasswordCheckAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        verify_code = request.COOKIES.get('code')
        if not verify_code:
            return JsonResponse({"error": "Code expired!"})
        data['verify_code'] = int(verify_code)
        s = ForgotPasswordCheckSerializer(data=data)
        if s.is_valid():
            return JsonResponse({"message": "Correct code!"}, status=HTTP_200_OK)
        return JsonResponse(s.errors, status=HTTP_400_BAD_REQUEST)



