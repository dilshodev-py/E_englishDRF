

import pytest
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import User
from essential.models import Book, Unit, Word


@pytest.mark.django_db
class TestQuizViewSet:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def db(self):
        Book.objects.create(name="Essential",image="images/books/essential.png",number=Book.NumberType.ONE)
        Unit.objects.create(book_id=1,number=1,name="Introduction")
        Word.objects.create(uz="Salom",en="Hello",pronunciation="həˈloʊ",type="noun",definition="A greeting or expression of goodwill",sentence="Hello, how are you?",image="images/words/hello.jpg",unit_id=1)

    def test_random_quiz(self, client,db):
        url = reverse('random-quiz')
        data = {
            "book_id": 1,
            "unit_ids": [1],
            "question_count": 2,
        }
        response = client.post(url, data)
        assert response.status_code == 200, "random quiz Bad request"

