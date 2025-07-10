from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from bson import ObjectId
from datetime import datetime
import logging

from .mongodb_service import MongoDBService
from .serializers import MongoDataSerializer, MongoQuerySerializer

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow anonymous access
def test_mongodb_connection(request):
    """Test MongoDB connection"""
    try:
        client = MongoDBService.get_client()
        db = MongoDBService.get_database()
        
        # Test connection
        client.admin.command('ping')
        
        # Get database stats
        stats = db.command('dbstats')
        
        return JsonResponse({
            'status': 'success',
            'message': 'MongoDB connection successful',
            'database': stats.get('db', 'N/A'),
            'collections': stats.get('collections', 0),
            'dataSize': stats.get('dataSize', 0),
            'storageSize': stats.get('storageSize', 0)
        })
    except Exception as e:
        logger.error(f"MongoDB connection test failed: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'MongoDB connection failed: {str(e)}'
        }, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_document(request):
    """Create a new document in MongoDB"""
    try:
        serializer = MongoDataSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.create(serializer.validated_data)
            return Response({
                'status': 'success',
                'message': 'Document created successfully',
                'data': document
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error creating document: {e}")
        return Response({
            'status': 'error',
            'message': f'Error creating document: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_documents(request):
    """Get documents from MongoDB with filtering and pagination"""
    try:
        # Parse query parameters
        query_serializer = MongoQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Invalid query parameters',
                'errors': query_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        query_data = query_serializer.validated_data
        collection = MongoDBService.get_collection(query_data['collection'])
        
        # Build filter query
        filter_query = {}
        if query_data.get('name'):
            filter_query['name'] = {'$regex': query_data['name'], '$options': 'i'}
        if query_data.get('email'):
            filter_query['email'] = query_data['email']
        if query_data.get('age_min') or query_data.get('age_max'):
            age_filter = {}
            if query_data.get('age_min'):
                age_filter['$gte'] = query_data['age_min']
            if query_data.get('age_max'):
                age_filter['$lte'] = query_data['age_max']
            filter_query['age'] = age_filter
        
        # Build sort
        sort_direction = 1 if query_data['sort_order'] == 'asc' else -1
        sort_criteria = [(query_data['sort_by'], sort_direction)]
        
        # Execute query
        cursor = collection.find(filter_query).sort(sort_criteria).skip(query_data['skip']).limit(query_data['limit'])
        
        # Convert documents to JSON serializable format
        documents = []
        for doc in cursor:
            doc['id'] = str(doc['_id'])
            del doc['_id']
            # Convert datetime objects to strings
            if 'created_at' in doc:
                doc['created_at'] = doc['created_at'].isoformat()
            if 'updated_at' in doc:
                doc['updated_at'] = doc['updated_at'].isoformat()
            documents.append(doc)
        
        # Get total count
        total_count = collection.count_documents(filter_query)
        
        return Response({
            'status': 'success',
            'message': 'Documents retrieved successfully',
            'data': {
                'documents': documents,
                'total_count': total_count,
                'page_size': query_data['limit'],
                'page': (query_data['skip'] // query_data['limit']) + 1
            }
        })
        
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return Response({
            'status': 'error',
            'message': f'Error retrieving documents: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document(request, document_id):
    """Get a specific document by ID"""
    try:
        collection = MongoDBService.get_collection('user_data')
        document = collection.find_one({'_id': ObjectId(document_id)})
        
        if document:
            document['id'] = str(document['_id'])
            del document['_id']
            # Convert datetime objects to strings
            if 'created_at' in document:
                document['created_at'] = document['created_at'].isoformat()
            if 'updated_at' in document:
                document['updated_at'] = document['updated_at'].isoformat()
            
            return Response({
                'status': 'success',
                'message': 'Document retrieved successfully',
                'data': document
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        return Response({
            'status': 'error',
            'message': f'Error retrieving document: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_document(request, document_id):
    """Update a specific document by ID"""
    try:
        collection = MongoDBService.get_collection('user_data')
        
        # Check if document exists
        existing_doc = collection.find_one({'_id': ObjectId(document_id)})
        if not existing_doc:
            return Response({
                'status': 'error',
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validate and update
        serializer = MongoDataSerializer(data=request.data)
        if serializer.is_valid():
            # Add update timestamp
            update_data = serializer.validated_data
            update_data['updated_at'] = datetime.utcnow()
            
            # Update document
            collection.update_one(
                {'_id': ObjectId(document_id)},
                {'$set': update_data}
            )
            
            # Return updated document
            updated_doc = collection.find_one({'_id': ObjectId(document_id)})
            updated_doc['id'] = str(updated_doc['_id'])
            del updated_doc['_id']
            
            return Response({
                'status': 'success',
                'message': 'Document updated successfully',
                'data': updated_doc
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        return Response({
            'status': 'error',
            'message': f'Error updating document: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_document(request, document_id):
    """Delete a specific document by ID"""
    try:
        collection = MongoDBService.get_collection('user_data')
        
        # Check if document exists
        existing_doc = collection.find_one({'_id': ObjectId(document_id)})
        if not existing_doc:
            return Response({
                'status': 'error',
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Delete document
        result = collection.delete_one({'_id': ObjectId(document_id)})
        
        if result.deleted_count > 0:
            return Response({
                'status': 'success',
                'message': 'Document deleted successfully'
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Failed to delete document'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return Response({
            'status': 'error',
            'message': f'Error deleting document: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_collection_stats(request):
    """Get statistics about the MongoDB collection"""
    try:
        collection = MongoDBService.get_collection('user_data')
        
        # Get collection stats
        total_docs = collection.count_documents({})
        
        # Get recent documents
        recent_docs = list(collection.find().sort('created_at', -1).limit(5))
        for doc in recent_docs:
            doc['id'] = str(doc['_id'])
            del doc['_id']
        
        return Response({
            'status': 'success',
            'message': 'Collection statistics retrieved successfully',
            'data': {
                'total_documents': total_docs,
                'recent_documents': recent_docs,
                'collection_name': 'user_data'
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting collection stats: {e}")
        return Response({
            'status': 'error',
            'message': f'Error getting collection stats: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
