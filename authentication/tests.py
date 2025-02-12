

import pytest
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import User


@pytest.mark.django_db
class TestUserViewSet:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def db(self):
        User.objects.create(email='absaitovdev@gmail.com' , password=make_password('12') , is_active=True)


    def test_register_auth(self, client):
        url = reverse('register')
        data = {
            "fullname": "Dilshod Absaitov",
            "email": "absaitovdev@gmail.com",
            "password": "AbsaitovDilshod3234*",
        }
        response = client.post(url, data)
        assert response.status_code == 200
        code = cache.get('absaitovdev@gmail.com')
        url = reverse('register-check')
        data = {
            "code": code,
            "email": "absaitovdev@gmail.com",
        }
        response = client.post(url, data)
        assert response.status_code == 200, 'register point : Bad request '

    def test_login_auth(self, client, db):
        url = reverse('token_obtain_pair')
        data = {
            "email": "ozodbekg800@gmail.com",
            "password": "12",
        }
        response = client.post(url , data)
        assert response.status_code == 200
        assert len(response.data) == 2

    # def test_retrieve_book(self, client, db):
    #     url = reverse('category-detail', args=[1])
    #     response = client.get(url)
    #     assert response.status_code == 200
    #     assert response.data['name'] == "Sport"
    #
    # def test_update_book(self, client, db):
    #     url = reverse('category-update', args=[2])
    #     data = {
    #         "name": "Car"
    #     }
    #     response = client.put(url, data)
    #     assert response.status_code == 200
    #     assert response.data['name'] == "Car"
    # #
    # def test_delete_category(self, client, db):
    #     url = reverse('category-destroy', args=[1])
    #     response = client.delete(url)
    #     assert response.status_code == 204
    #     assert not Category.objects.filter(id=1).exists()
