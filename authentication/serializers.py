from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    expires = serializers.DateTimeField()


class ValidateResponseSerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    user = serializers.CharField()
    expires = serializers.DateTimeField()


class VerifyResponseSerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    message = serializers.CharField()
