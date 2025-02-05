import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from essential.models import Word, Book, Unit


# Create your tests here.
@pytest.mark.django_db
class TestWordViewSet:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def db(self):
        book = Book.objects.create(name='Sample Book', image='images/books/', number=1)
        unit = Unit.objects.create(book=book, number=1, name='Sample Unit')

        Word.objects.create(
            uz='salom', en='hello', pronunciation='kdsdk', type='noun',
            definition='sjdbjas jask', sentence='sa', image='images/words/', unit=unit
        )

    def test_word_list(self, client, db):
        unit_id=1
        url = reverse('words', kwargs={'unit_id': unit_id})
        response=client.get(url)
        assert response.status_code == 200, 'Error!'


