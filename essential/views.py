from django.db.models import Sum
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView

from authentication.models import User
from essential.serializers import UserModelSerializer
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from essential.models import Book, Unit
from essential.serializers import BookModelSerializer, UniteModelSerializer



@extend_schema(tags=['leaderboard'])
class LeaderBoardAPIView(APIView):
    def get(self, request):
        users = User.objects.annotate(point=Sum('points__point')).order_by('-point')
        top = users[:10]
        serialized_top = UserModelSerializer(instance=top, many=True).data
        user = None
        over_user = None
        under_user = None
        around_user = None
        if request.user.is_authenticated and not request.user in top:
            for i in range(len(users)):
                if users[i].id == request.user.id:
                    user = users[i]
                    over_user = users[i - 1]
                    try:
                        under_user = users[i + 1]
                    except:
                        under_user = None
            around_user = [over_user, user]
            if under_user:
                around_user.append(under_user)
            around_user = UserModelSerializer(instance=around_user, many=True).data
        return JsonResponse({"top": serialized_top, "around_user": around_user})

@extend_schema(tags=['essential'])
class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer


@extend_schema(tags=['essential'])
class UniteListAPIView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UniteModelSerializer