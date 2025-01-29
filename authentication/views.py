from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_202_ACCEPTED
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import ForgotPasswordSerializer, ForgotPasswordCheckSerializer


# from authentication.tasks import send_email


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

