from django.urls import path

from authentication.views import SendRandomNumberAPIView

urlpatterns = [
    path('send-random-number/', SendRandomNumberAPIView.as_view(), name='send_random_number'),

]

