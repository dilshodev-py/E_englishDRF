from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView

from essential.models import Book, Unit
from essential.serializers import BookModelSerializer, UniteModelSerializer


# Create your views here.

@extend_schema(tags=['essential'])
class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer


@extend_schema(tags=['essential'])
class UniteListAPIView(ListAPIView):
    serializer_class = UniteModelSerializer

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        return Unit.objects.filter(book_id=book_id)