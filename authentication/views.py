from random import randint

from django.core.cache import cache
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import ForgotPasswordSerializer, ForgotPasswordCheckSerializer, RegisterCheckSerializer
from authentication.serializers import PasswordResetSerializer
from authentication.serializers import RegisterSerializer
from authentication.tasks import send_email


@extend_schema(tags=['auth'], request=PasswordResetSerializer)
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "message": "Parol yangilandi!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], request=ForgotPasswordSerializer)
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        data = request.data
        s = ForgotPasswordSerializer(data=data)
        if s.is_valid():
            email = s.validated_data.get('email')
            code = randint(10000, 99999)
            print(code)
            send_email.delay(to_send=email, code=code)
            response = JsonResponse({"status": 200, "message": "Code send to your email!", "email": email}, status=HTTP_200_OK)
            cache.set(email, code, timeout=300)
            return response
        return JsonResponse(s.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], request=ForgotPasswordCheckSerializer)
class ForgotPasswordCheckAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        email = data.get('email')
        verify_code = cache.get(email)
        if not verify_code:
            return JsonResponse({"error": "Code expired!"}, status=HTTP_400_BAD_REQUEST)
        data['verify_code'] = verify_code
        s = ForgotPasswordCheckSerializer(data=data)
        if s.is_valid():
            return JsonResponse({"status": 200, "message": "Correct code!", "email": email}, status=HTTP_200_OK)
        return JsonResponse(s.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], request=RegisterSerializer)
class RegisterAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        user = User.objects.filter(email=request.data.get("email")).first()
        if serializer.is_valid() or (user and not user.is_active):
            if not user:
                u = serializer.save()
                u.is_active = False
                u.save()
            random_code = randint(10000, 99999)
            email = request.data.get("email")
            send_email.delay(email, random_code)
            response = JsonResponse({
                "status": 200,
                "message": "Tasdiqlash kodi jo'natildi!",
                "data": None
            }, status=HTTP_200_OK)
            cache.set(email, str(random_code), timeout=300)
            return response
        elif user and user.is_active:
            return JsonResponse({"status": 400, "message": "Email oldin ro'yxatdan o'tgan !"}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], request=RegisterCheckSerializer)
class RegisterCheckAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        verify_code = cache.get(data.get('email'))
        print(verify_code)
        print(data.get('code'))
        if not verify_code:
            return JsonResponse({"error": "Code expired!"}, status=HTTP_400_BAD_REQUEST)
        data['verify_code'] = verify_code
        s = RegisterCheckSerializer(data=data)
        if s.is_valid():
            User.objects.filter(email=data.get('email')).update(is_active=True)
            return JsonResponse({"status": 200, "message": "Registered!"}, status=HTTP_200_OK)
        return JsonResponse(s.errors, status=HTTP_400_BAD_REQUEST)
