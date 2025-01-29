from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, IntegerField
from rest_framework.serializers import Serializer

from authentication.models import User


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
