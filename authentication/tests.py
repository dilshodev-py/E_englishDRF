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
        User.objects.create(email='absaitovdev@gmail.com', password=make_password('12'), is_active=True)

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
            "email": "absaitovdev@gmail.com",
            "password": "12",
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert len(response.data) == 2

    def forgot_password_auth(self, client, db):
        url = reverse('forgot_password')
        data = {
            'email': 'absaitovdev@gmail.com'
        }

        response = client.post(url, data)
        assert response.status_code == 200
        # ---------------------------------------------------

        code = cache.get('absaitovdev@gmail.com')
        url = 'forgot_password-check'
        data = {
            'email': 'absaitovdev@gmail.com',
            'code': code
        }
        response = client.post(url, data)
        assert response.status_code == 200

        # ---------------------------------------------------

        data['code'] = 00000

        response = client.post(url, data)

        assert response.status_code == 400

        # ---------------------------------------------------

        url = reverse('reset_password')

        data = {
            'email': 'absaitovdev@gmail.com',
            'password': 'asdfghjk'
        }

        response = client.post(url, data)

        assert response.status_code == 200

        # ---------------------------------------------------

        data['email'] = 'sdfghj@gmail.com'

        response = client.post(url, data)

        assert response.status_code == 400

        # ---------------------------------------------------

        url = reverse('token_obtain_pair')
        data = {
            "email": "absaitovdev@gmail.com",
            "password": "asdfghjk",
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_forgot_password_auth(self, client,db):
        url = reverse('forgot-password')
        data = {
            "email": "absaitovdev@gmail.com",
        }
        response = client.post(url, data)
        assert response.status_code == 200, "forgot password point : Bad request "
        code = cache.get('absaitovdev@gmail.com')
        url = reverse('verify-otp')
        data = {
            "code": code,
            "email": "absaitovdev@gmail.com",
        }
        response = client.post(url , data)
        assert response.status_code == 200 , 'forgot password check code Bad request '

        url = reverse('reset-password')
        data = {
            "email": "absaitovdev@gmail.com",
            "password": "Test*123",
        }
        response = client.post(url, data)
        assert response.status_code == 200 , 'reset password Bad request '





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
