from rest_framework.serializers import ModelSerializer

from essential.models import Book, Unit


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class UniteModelSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'