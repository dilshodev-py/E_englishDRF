import re

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.fields import EmailField, IntegerField
from rest_framework.serializers import Serializer, ModelSerializer

from authentication.models import User


class PasswordResetSerializer(serializers.Serializer):
    email = EmailField(required=True)
    password = CharField(required=True)
    confirm_password = CharField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise ValidationError('Something went wrong!')
        return value

    def validate_confirm_password(self, value):
        if value != self.initial_data.get('password'):
            raise ValidationError("Passwords must match!")
        return value

    def save(self, **kwargs):
        email = self.initial_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Something went wrong!")
        user = User.objects.filter(email=email).first()
        user.password = make_password(self.initial_data.get('password'))
        user.save()
        return user


class RegisterSerializer(ModelSerializer):
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
        return make_password(value)


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
        if not check_password(str(value) , self.initial_data.get('verify_code').encode()):
            raise ValidationError("Incorrect code!")
        return value

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     send_verification_email.delay(user.email)
    #     return user
