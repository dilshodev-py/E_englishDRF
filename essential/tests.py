
import pytest
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.middleware.csrf import get_token
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
        Book.objects.create(name="Essential", image="images/books/essential.png", number=Book.NumberType.ONE)
        Unit.objects.create(book_id=1, number=1, name="Introduction")
        Word.objects.create(uz="Salom", en="Hello", pronunciation="həˈloʊ", type="noun",
                            definition="A greeting or expression of goodwill", sentence="Hello, how are you?",
                            image="images/words/hello.jpg", unit_id=1)

        User.objects.create(email='t@gmail.com', password=make_password('1'), is_active=True)
        Book.objects.create(name='Book', number=1 )
        Unit.objects.create(name='Unit', book_id=1, number=1 )
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from django.test import TestCase

    def test_quiz_result_api(self, client, db):

        url = reverse('token_obtain_pair')
        data = {
            "email": "t@gmail.com",
            "password": "1"
        }
        response = client.post(url, data)
        access = response.data.get('access')

        url = reverse('quiz_result')
        data = {
            "correct": 15,
            "unit": 1,
            "user":1
        }

        response = client.post(url, data, headers={"Authorization" : "Bearer " + access })
        assert response.status_code == 201

    def test_random_quiz(self, client,db):
        url = reverse('random-quiz')
        data = {
            "book_id": 1,
            "unit_ids": [1],
            "question_count": 2,
        }
        response = client.post(url, data)
        assert response.status_code == 200, "random quiz Bad request"
from essential.models import Book, Unit


# Create your tests here.
@pytest.mark.django_db
class TestEssential:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def db(self):
        Book.objects.create(name="name", image = "image", number = 1)
        Book.objects.create(name="name", image = "image", number = 2)

    def test_book_list(self, client, db):
        url = reverse("books")
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2
