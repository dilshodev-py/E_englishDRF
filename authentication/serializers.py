import re

from django.contrib.auth.models import User
from django.db.models.fields import CharField, EmailField
from rest_framework.serializers import Serializer, ValidationError


class RegisterSerializer(Serializer):
    full_name = CharField(max_length=255)
    email = EmailField(unique=True)
    password = CharField(max_length=8)
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[*/!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError("Password must contain at least one special character.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one number.")
from rest_framework import serializers


from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, IntegerField
from rest_framework.serializers import Serializer

from authentication.models import User

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgotPasswordSerializer(Serializer):
    email = EmailField(required=True)

    def validate_email(self, value):
        if not value:
            raise ValidationError("Email must not be empty!")
        if not User.objects.filter(email=value).exists():
            raise ValidationError("Email not found!")
        return value


class ForgotPasswordCheckSerializer(Serializer):
    code = IntegerField(required=True)
    verify_code = IntegerField(read_only=True)
    email = EmailField(required=True)

    def validate_email(self, value):
        if not value or not User.objects.filter(email=value).exists():
            raise ValidationError("Something went wrong!")
        return value

    def validate_code(self, value):
        if not value == self.initial_data.get('verify_code'):
            raise ValidationError("Incorrect code!")
        return value

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     send_verification_email.delay(user.email)
    #     return user
