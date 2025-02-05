from django.test import TestCase

from authentication.models import User


class RegisterTestCase(TestCase):
    def setUp(self):
        User.objects.create(email='test@gmail.com', password='test1234')

    def test_user(self):
        user =  User.objects.filter(email='test@gmail.com').first()
        self.assertIsNotNone(user, "Problem with creating user!")
        self.assertNotEqual(user.password, 'test1234', "Problem with hashing user password!")


