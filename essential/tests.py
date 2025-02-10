import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from django.test import TestCase

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
