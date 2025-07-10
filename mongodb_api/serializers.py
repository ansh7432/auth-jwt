from rest_framework import serializers
from datetime import datetime
from bson import ObjectId

class MongoDataSerializer(serializers.Serializer):
    """Serializer for MongoDB document operations"""
    
    # Common fields
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    age = serializers.IntegerField(required=False, min_value=0)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Dynamic fields for flexible data
    data = serializers.DictField(required=False)
    
    def create(self, validated_data):
        """Create a new document in MongoDB"""
        from .mongodb_service import MongoDBService
        
        # Add timestamps
        validated_data['created_at'] = datetime.utcnow()
        validated_data['updated_at'] = datetime.utcnow()
        
        # Get collection
        collection = MongoDBService.get_collection('user_data')
        
        # Insert document
        result = collection.insert_one(validated_data)
        
        # Return the created document
        created_document = collection.find_one({'_id': result.inserted_id})
        if created_document:
            created_document['id'] = str(created_document['_id'])
            del created_document['_id']
        
        return created_document
    
    def update(self, instance, validated_data):
        """Update an existing document in MongoDB"""
        from .mongodb_service import MongoDBService
        
        # Add update timestamp
        validated_data['updated_at'] = datetime.utcnow()
        
        # Get collection
        collection = MongoDBService.get_collection('user_data')
        
        # Update document
        collection.update_one(
            {'_id': ObjectId(instance['id'])},
            {'$set': validated_data}
        )
        
        # Return the updated document
        updated_document = collection.find_one({'_id': ObjectId(instance['id'])})
        if updated_document:
            updated_document['id'] = str(updated_document['_id'])
            del updated_document['_id']
        
        return updated_document

class MongoQuerySerializer(serializers.Serializer):
    """Serializer for MongoDB query parameters"""
    
    collection = serializers.CharField(max_length=100, required=False, default='user_data')
    limit = serializers.IntegerField(required=False, default=10, min_value=1, max_value=100)
    skip = serializers.IntegerField(required=False, default=0, min_value=0)
    sort_by = serializers.CharField(max_length=50, required=False, default='created_at')
    sort_order = serializers.ChoiceField(choices=[('asc', 'Ascending'), ('desc', 'Descending')], 
                                        required=False, default='desc')
    
    # Filter fields
    name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    age_min = serializers.IntegerField(required=False, min_value=0)
    age_max = serializers.IntegerField(required=False, min_value=0)
