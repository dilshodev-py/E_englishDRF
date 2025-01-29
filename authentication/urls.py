from django.urls import path

from authentication.views import SendRandomNumberAPIView

from django.urls import path

from authentication.views import ForgotPasswordAPIView, ForgotPasswordCheckAPIView

urlpatterns = [
    path('forgot-password', ForgotPasswordAPIView.as_view()),
    path('verify-otp', ForgotPasswordCheckAPIView.as_view()),
    path('send-random-number/', SendRandomNumberAPIView.as_view(), name='send_random_number'),

]

