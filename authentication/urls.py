from django.urls import path
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import ForgotPasswordAPIView, ForgotPasswordCheckAPIView, PasswordResetView, RegisterAPIView, \
    RegisterCheckAPIView

urlpatterns = [
    path('forgot-password', ForgotPasswordAPIView.as_view(),name='forgot-password'),
    path('verify-otp', ForgotPasswordCheckAPIView.as_view(),name='verify-otp'),
    path('auth/reset-password/', PasswordResetView.as_view(),name='reset-password'),
    path('api/token/', TokenObtainPairView.as_view(parser_classes = [MultiPartParser , JSONParser]), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view() , name='register'),
    path('register/check', RegisterCheckAPIView.as_view() , name='register-check'),
]
