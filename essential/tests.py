
import pytest
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.middleware.csrf import get_token
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import User
from essential.models import Book, Unit


@pytest.mark.django_db
class TestEssentialViewSet:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def db(self):
        User.objects.create(email='t@gmail.com', password=make_password('1'), is_active=True)
        Book.objects.create(name='Book', number=1 )
        Unit.objects.create(name='Unit', book_id=1, number=1 )

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

