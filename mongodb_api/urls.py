from django.urls import path
from . import views

urlpatterns = [
    # MongoDB connection test
    path('test-connection/', views.test_mongodb_connection, name='test-mongodb-connection'),
    
    # CRUD operations
    path('documents/', views.get_documents, name='get-documents'),
    path('documents/create/', views.create_document, name='create-document'),
    path('documents/<str:document_id>/', views.get_document, name='get-document'),
    path('documents/<str:document_id>/update/', views.update_document, name='update-document'),
    path('documents/<str:document_id>/delete/', views.delete_document, name='delete-document'),
    
    # Collection statistics
    path('stats/', views.get_collection_stats, name='get-collection-stats'),
]
