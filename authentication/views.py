from django.shortcuts import render
import random
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from authentication.serializers import EmailSerializer


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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


