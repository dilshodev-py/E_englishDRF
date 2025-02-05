from django.urls import path

from essential import views
from essential.views import LeaderBoardAPIView
from essential.views import BookListAPIView, UniteListAPIView
from essential.views import QuizView

urlpatterns = [
    path('leaderboard/', LeaderBoardAPIView.as_view()),
    path('books/', BookListAPIView.as_view()),
    path('random-quiz/',QuizView.as_view(), name='random-quiz'),
    path('books/<int:book_id>/units/', UniteListAPIView.as_view()),
    path('random-quiz/',QuizView.as_view(), name='random-quiz'),
    path('words/<unit_id>', views.get_words_apiview),
]
