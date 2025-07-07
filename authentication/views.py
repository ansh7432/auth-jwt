from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from datetime import datetime
from .jwt_service import JWTService
from .serializers import (
    LoginSerializer, 
    TokenVerifySerializer, 
    TokenResponseSerializer,
    ValidateResponseSerializer,
    VerifyResponseSerializer
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
