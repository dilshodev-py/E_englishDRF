from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from essential.models import Book, Unit


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class UniteModelSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class UserModelSerializer(ModelSerializer):
    point = IntegerField()
    class Meta:
        model = User
        fields = 'full_name', 'point',