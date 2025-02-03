from django.urls import path

from essential.views import BookListAPIView, UniteListAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view()),
    path('books/<int:book_id>/units/', UniteListAPIView.as_view()),
]