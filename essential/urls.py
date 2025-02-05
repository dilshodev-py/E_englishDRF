from django.urls import path

from essential.views import LeaderBoardAPIView
from essential.views import BookListAPIView, UniteListAPIView
from essential.views import QuizView

urlpatterns = [
    path('leaderboard/', LeaderBoardAPIView.as_view()),
    path('books/', BookListAPIView.as_view()),
    path('books/<int:book_id>/units/', UniteListAPIView.as_view()),
    path('units/', UniteListAPIView.as_view()),
    path('random-quiz/',QuizView.as_view(), name='random-quiz')
]