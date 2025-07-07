import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User


class JWTService:
    @staticmethod
    def generate_token(user):
        """Generate JWT token for a user"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
            'iat': datetime.utcnow(),
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token, payload['exp']
    
    @staticmethod
    def decode_token(token):
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "Token has expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"
    
    @staticmethod
    def get_user_from_token(token):
        """Get user object from JWT token"""
        payload, error = JWTService.decode_token(token)
        if error:
            return None, error
        
        try:
            user = User.objects.get(id=payload['user_id'])
            return user, None
        except User.DoesNotExist:
            return None, "User not found"
