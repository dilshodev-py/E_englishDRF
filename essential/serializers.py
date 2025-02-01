from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserModelSerializer(ModelSerializer):
    point = IntegerField()
    class Meta:
        model = User
        fields = 'full_name', 'point',