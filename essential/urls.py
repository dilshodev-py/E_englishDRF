from django.urls import path

from essential.views import LeaderBoardListAPIView

urlpatterns = [
    path('leaderboard/', LeaderBoardListAPIView.as_view())
]
