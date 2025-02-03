
from django.urls import path

from essential.views import QuizView

urlpatterns = [
    path('random-quiz/',QuizView.as_view(), name='random-quiz')
]
