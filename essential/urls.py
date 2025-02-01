from django.urls import path

from essential.views import LeaderBoardAPIView

urlpatterns = [
    path('leaderboard/', LeaderBoardAPIView.as_view())
]
