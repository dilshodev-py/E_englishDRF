from django.urls import path

from essential.views import LeaderBoardAPIView
from essential.views import BookListAPIView, UniteListAPIView

urlpatterns = [
    path('leaderboard/', LeaderBoardAPIView.as_view()),
    path('books/', BookListAPIView.as_view()),
    path('units/', UniteListAPIView.as_view()),
]