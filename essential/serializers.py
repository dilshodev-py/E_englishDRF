from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from essential.models import Book, Unit, QuizResult
from rest_framework import serializers

class QuizRequestSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    unit_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    question_count = serializers.IntegerField(default=10, min_value=1, max_value=20)


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
        fields = 'fullname', 'point',


class QuizResultSerializer(ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ['id', 'correct', 'user', 'unit', 'created_at']