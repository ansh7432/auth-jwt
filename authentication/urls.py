from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('verify/', views.verify_token_view, name='verify_token'),
    path('validate/', views.validate_token_view, name='validate_token'),
]
