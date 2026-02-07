from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.config import settings
import logging
import time

logger = logging.getLogger(__name__)

# MongoDB client with connection pooling
client = None
db = None
job_collection = None
user_collection = None


def connect_to_database(max_retries: int = 3, retry_delay: int = 2):
    """
    Connect to MongoDB with retry logic and error handling.
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Delay in seconds between retries
    """
    global client, db, job_collection, user_collection
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to MongoDB (attempt {attempt + 1}/{max_retries})...")
            
            # Create client with connection pooling settings
            client = MongoClient(
                settings.mongo_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                maxPoolSize=50,
                minPoolSize=10,
                tls=True,
                tlsAllowInvalidCertificates=True,  # Fix for SSL handshake issues on some platforms
            )
            
            # Test the connection
            client.admin.command('ping')
            
            # Initialize database and collections
            db = client["carevia"]
            job_collection = db["jobs"]
            user_collection = db["users"]
            
            # Create indexes for better performance
            job_collection.create_index("url", unique=True)
            job_collection.create_index("source")
            job_collection.create_index("category")
            
            logger.info("Successfully connected to MongoDB")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.critical("Max retries reached. Could not connect to MongoDB.")
                raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise
    
    return False


def close_database_connection():
    """Close the MongoDB connection gracefully."""
    global client
    
    if client:
        try:
            client.close()
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")


def check_database_health() -> bool:
    """
    Check if database connection is healthy.
    
    Returns:
        bool: True if database is accessible, False otherwise
    """
    try:
        if client is None:
            return False
        
        # Ping the database
        client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# Initialize connection on module import
try:
    connect_to_database()
except Exception as e:
    logger.warning(f"Initial database connection failed: {e}")

