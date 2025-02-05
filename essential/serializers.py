from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from essential.models import Book, Unit, Word
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

class WordModelSerializer(ModelSerializer):
    already_try=serializers.SerializerMethodField()
    class Meta:
        model = Word
        fields = '__all__'
        extra_fields = ['already_try']

    def get_already_try(self, obj):
        return self.context.get('already_try', False)