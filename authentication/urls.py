from django.urls import path
from authentication.views import ForgotPasswordAPIView, ForgotPasswordCheckAPIView

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('forgot-password', ForgotPasswordAPIView.as_view()),
    path('verify-otp', ForgotPasswordCheckAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

