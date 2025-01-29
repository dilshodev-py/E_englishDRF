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
        return value

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     send_verification_email.delay(user.email)
    #     return user
