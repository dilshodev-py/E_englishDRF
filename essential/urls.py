from django.urls import path

from essential.views import BookListAPIView, UniteListAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view()),
    path('units/', UniteListAPIView.as_view()),
]