from django.db.models import Sum
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from authentication.models import User
from essential.serializers import UserModelSerializer


@extend_schema(tags=['leaderboard'])
class LeaderBoardListAPIView(ListAPIView):
    queryset = User.objects.annotate(point=Sum('points__point')).order_by('point')[:10]
    serializer_class = UserModelSerializer
