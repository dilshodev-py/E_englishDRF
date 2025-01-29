from django.urls import path


from authentication.views import PasswordResetView

from django.urls import path

from django.urls import path

from authentication.views import ForgotPasswordAPIView, ForgotPasswordCheckAPIView

urlpatterns = [
    path('forgot-password', ForgotPasswordAPIView.as_view()),
    path('verify-otp', ForgotPasswordCheckAPIView.as_view()),
    path('auth/reset-password/', PasswordResetView.as_view()),

]

