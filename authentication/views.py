from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .jwt_service import JWTService
from .serializers import (
    LoginSerializer, 
    TokenVerifySerializer, 
    TokenResponseSerializer,
    ValidateResponseSerializer,
    VerifyResponseSerializer,
    UserRegistrationSerializer,
    UserRegistrationResponseSerializer
)


@swagger_auto_schema(
    method='post',
    operation_description='Register a new user account',
    request_body=UserRegistrationSerializer,
    responses={
        201: UserRegistrationResponseSerializer,
        400: 'Bad request - validation errors'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    POST /api/auth/register/
    Register a new user account
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': 'Validation failed', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        with transaction.atomic():
            user = serializer.save()
            
            # Generate JWT token for the new user
            token, expires = JWTService.generate_token(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'date_joined': user.date_joined.isoformat() + 'Z'
                },
                'token': token,
                'expires': expires.isoformat() + 'Z'
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response(
            {'error': 'Registration failed', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(
    method='post',
    operation_description='Authenticate user and get JWT token',
    request_body=LoginSerializer,
    responses={
        200: TokenResponseSerializer,
        401: 'Unauthorized - invalid credentials'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST /api/auth/login/
    Takes {"username": "user", "password": "pass"}
    Returns JWT token
    """
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid input', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, expires = JWTService.generate_token(user)
    
    return Response({
        'token': token,
        'expires': expires.isoformat() + 'Z'
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description='Verify if a JWT token is valid',
    request_body=TokenVerifySerializer,
    responses={
        200: VerifyResponseSerializer
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token_view(request):
    """
    POST /api/auth/verify/
    Takes {"token": "jwt_token"}
    Returns token validation status
    """
    serializer = TokenVerifySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid input', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token = serializer.validated_data['token']
    payload, error = JWTService.decode_token(token)
    
    if error:
        return Response({
            'valid': False,
            'message': error
        }, status=status.HTTP_200_OK)
    
    return Response({
        'valid': True,
        'message': 'Token is valid'
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description='Validate JWT token and get user information',
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="JWT token (format: 'Bearer <token>')",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: ValidateResponseSerializer,
        401: 'Unauthorized - invalid or missing token'
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def validate_token_view(request):
    """
    GET /api/auth/validate/
    Requires JWT in Authorization header
    Returns {"valid": true, "user": "username", "expires": "timestamp"}
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response(
            {'error': 'Authorization header required'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        token = auth_header.split(' ')[1]  # Remove 'Bearer ' prefix
    except IndexError:
        return Response(
            {'error': 'Invalid authorization header format'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user, error = JWTService.get_user_from_token(token)
    if error:
        return Response(
            {'error': error},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    payload, _ = JWTService.decode_token(token)
    expires = datetime.fromtimestamp(payload['exp'])
    
    return Response({
        'valid': True,
        'user': user.username,
        'expires': expires.isoformat() + 'Z'
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description='Health check endpoint',
    responses={
        200: openapi.Response(
            description='Health check response',
            examples={
                'application/json': {
                    'status': 'healthy',
                    'service': 'JWT Authentication API',
                    'version': '1.0.0',
                    'timestamp': '2025-07-08T10:30:00Z'
                }
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    GET /api/auth/health/
    Simple health check endpoint
    """
    return Response({
        'status': 'healthy',
        'service': 'JWT Authentication API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat() + 'Z'
    }, status=status.HTTP_200_OK)
