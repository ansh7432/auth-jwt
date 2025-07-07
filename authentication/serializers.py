from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
        help_text="Password must be at least 8 characters long"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Confirm your password"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'username': {'help_text': 'Required. 150 characters or fewer.'},
            'email': {'required': True, 'help_text': 'Required. Valid email address.'},
            'first_name': {'help_text': 'Optional. First name.'},
            'last_name': {'help_text': 'Optional. Last name.'},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields didn't match."}
            )
        return attrs

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # Remove password_confirm since it's not needed for user creation
        validated_data.pop('password_confirm', None)
        
        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class UserRegistrationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user = serializers.DictField()
    token = serializers.CharField()
    expires = serializers.DateTimeField()
