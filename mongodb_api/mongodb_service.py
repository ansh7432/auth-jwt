from pymongo import MongoClient
from django.conf import settings
import logging
import ssl

logger = logging.getLogger(__name__)

class MongoDBService:
    _client = None
    _db = None
    
    @classmethod
    def get_client(cls):
        """Get MongoDB client singleton"""
        if cls._client is None:
            try:
                cls._client = MongoClient(
                    settings.MONGODB_CONFIG['host'],
                    tls=True,
                    tlsAllowInvalidCertificates=True,
                    authSource='admin',
                    authMechanism='SCRAM-SHA-1'
                )
                # Test connection
                cls._client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
        return cls._client
    
    @classmethod
    def get_database(cls):
        """Get MongoDB database"""
        if cls._db is None:
            client = cls.get_client()
            cls._db = client[settings.MONGODB_CONFIG['database']]
        return cls._db
    
    @classmethod
    def get_collection(cls, collection_name):
        """Get MongoDB collection"""
        db = cls.get_database()
        return db[collection_name]
    
    @classmethod
    def close_connection(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")
