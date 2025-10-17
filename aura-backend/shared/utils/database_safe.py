"""
Database utilities and connection management for Aura Backend Services
Python 3.13 Compatible Version with fallback for asyncpg
"""

import asyncio
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Try to import asyncpg, but handle gracefully if not available
try:
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False
    print("⚠️  AsyncPG not available - PostgreSQL async features will be limited")

logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()


class DatabaseManager:
    """Database connection manager for PostgreSQL, MongoDB, and Redis"""
    
    def __init__(self):
        self.postgres_engine = None
        self.postgres_session = None
        self.postgres_sync_engine = None  # Fallback sync engine
        self.postgres_sync_session = None  # Fallback sync session
        self.mongo_client = None
        self.mongo_db = None
        self.redis_client = None
        self.use_async_postgres = ASYNCPG_AVAILABLE
    
    async def init_postgres(self, database_url: str) -> None:
        """Initialize PostgreSQL connection (async if available, sync as fallback)"""
        try:
            if self.use_async_postgres:
                # Try async connection
                async_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
                
                self.postgres_engine = create_async_engine(
                    async_url,
                    echo=False,
                    poolclass=StaticPool
                )
                
                self.postgres_session = sessionmaker(
                    self.postgres_engine,
                    class_=AsyncSession,
                    expire_on_commit=False
                )
                
                logger.info("PostgreSQL async connection initialized")
            else:
                # Fallback to sync connection
                self.postgres_sync_engine = create_engine(
                    database_url,
                    echo=False,
                    poolclass=StaticPool
                )
                
                self.postgres_sync_session = sessionmaker(
                    self.postgres_sync_engine,
                    expire_on_commit=False
                )
                
                logger.info("PostgreSQL sync connection initialized (asyncpg not available)")
            
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
            # If async fails, try sync fallback
            if self.use_async_postgres:
                logger.info("Falling back to sync PostgreSQL connection...")
                self.use_async_postgres = False
                await self.init_postgres(database_url)
            else:
                raise
    
    async def init_mongodb(self, mongodb_url: str, database_name: str) -> None:
        """Initialize MongoDB connection"""
        try:
            self.mongo_client = AsyncIOMotorClient(mongodb_url)
            self.mongo_db = self.mongo_client[database_name]
            
            # Test connection
            await self.mongo_client.admin.command('ping')
            logger.info(f"MongoDB connection initialized for database: {database_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB: {e}")
            raise
    
    async def init_redis(self, redis_url: str) -> None:
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info("Redis connection initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise
    
    async def get_postgres_session(self):
        """Get PostgreSQL session (async or sync depending on availability)"""
        if self.use_async_postgres:
            if not self.postgres_session:
                raise RuntimeError("PostgreSQL async not initialized")
            return self.postgres_session()
        else:
            if not self.postgres_sync_session:
                raise RuntimeError("PostgreSQL sync not initialized")
            return self.postgres_sync_session()
    
    def get_postgres_sync_session(self):
        """Get synchronous PostgreSQL session"""
        if not self.postgres_sync_session:
            raise RuntimeError("PostgreSQL sync not initialized")
        return self.postgres_sync_session()
    
    def get_mongo_db(self):
        """Get MongoDB database"""
        if self.mongo_db is None:
            raise RuntimeError("MongoDB not initialized")
        return self.mongo_db
    
    def get_redis_client(self):
        """Get Redis client"""
        if not self.redis_client:
            raise RuntimeError("Redis not initialized")
        return self.redis_client
    
    async def close_connections(self) -> None:
        """Close all database connections"""
        try:
            if self.use_async_postgres and self.postgres_engine:
                await self.postgres_engine.dispose()
                logger.info("PostgreSQL async connection closed")
            elif self.postgres_sync_engine:
                self.postgres_sync_engine.dispose()
                logger.info("PostgreSQL sync connection closed")
            
            if self.mongo_client:
                self.mongo_client.close()
                logger.info("MongoDB connection closed")
            
            if self.redis_client:
                await self.redis_client.close()
                logger.info("Redis connection closed")
                
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")


# Global database manager instance
db_manager = DatabaseManager()


class RedisCache:
    """Redis cache utility class"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        try:
            return await self.redis.setex(key, ttl, value)
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(await self.redis.delete(key))
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            return bool(await self.redis.exists(key))
        except Exception as e:
            logger.error(f"Redis EXISTS error for key {key}: {e}")
            return False
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter in cache"""
        try:
            return await self.redis.incr(key, amount)
        except Exception as e:
            logger.error(f"Redis INCR error for key {key}: {e}")
            return 0
    
    async def get_hash(self, key: str, field: str) -> Optional[str]:
        """Get hash field value"""
        try:
            return await self.redis.hget(key, field)
        except Exception as e:
            logger.error(f"Redis HGET error for key {key}, field {field}: {e}")
            return None
    
    async def set_hash(self, key: str, field: str, value: str) -> bool:
        """Set hash field value"""
        try:
            return await self.redis.hset(key, field, value)
        except Exception as e:
            logger.error(f"Redis HSET error for key {key}, field {field}: {e}")
            return False


class MongoRepository:
    """MongoDB repository base class"""
    
    def __init__(self, collection_name: str, mongo_db):
        self.collection = mongo_db[collection_name]
    
    async def create(self, document: Dict[str, Any]) -> str:
        """Create a new document"""
        try:
            result = await self.collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"MongoDB CREATE error: {e}")
            raise
    
    async def find_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Find document by ID"""
        try:
            from bson import ObjectId
            document = await self.collection.find_one({"_id": ObjectId(doc_id)})
            if document:
                document["_id"] = str(document["_id"])
            return document
        except Exception as e:
            logger.error(f"MongoDB FIND_BY_ID error: {e}")
            return None
    
    async def find_many(self, filter_dict: Dict[str, Any], limit: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        try:
            cursor = self.collection.find(filter_dict).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            for doc in documents:
                doc["_id"] = str(doc["_id"])
            return documents
        except Exception as e:
            logger.error(f"MongoDB FIND_MANY error: {e}")
            return []
    
    async def update_by_id(self, doc_id: str, update_dict: Dict[str, Any]) -> bool:
        """Update document by ID"""
        try:
            from bson import ObjectId
            result = await self.collection.update_one(
                {"_id": ObjectId(doc_id)},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"MongoDB UPDATE error: {e}")
            return False
    
    async def delete_by_id(self, doc_id: str) -> bool:
        """Delete docume by ID"""
        try:
            from bson import ObjectId
            result = await self.collection.delete_one({"_id": ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"MongoDB DELETE error: {e}")
            return False
    
    async def count(self, filter_dict: Dict[str, Any] = None) -> int:
        """Count documents"""
        try:
            if filter_dict is None:
                filter_dict = {}
            return await self.collection.count_documents(filter_dict)
        except Exception as e:
            logger.error(f"MongoDB COUNT error: {e}")
            return 0


async def init_database_connections(
    postgres_url: str,
    mongodb_url: str,
    mongodb_name: str,
    redis_url: str
) -> DatabaseManager:
    """Initialize all database connections"""
    try:
        await db_manager.init_postgres(postgres_url)
        await db_manager.init_mongodb(mongodb_url, mongodb_name)
        await db_manager.init_redis(redis_url)
        
        logger.info("All database connections initialized successfully")
        return db_manager
        
    except Exception as e:
        logger.error(f"Failed to initialize database connections: {e}")
        await db_manager.close_connections()
        raise


async def check_database_health() -> Dict[str, str]:
    """Check health of all database connections"""
    health_status = {
        "postgres": "unhealthy",
        "mongodb": "unhealthy", 
        "redis": "unhealthy"
    }
    
    # Check PostgreSQL
    try:
        if db_manager.use_async_postgres and db_manager.postgres_engine:
            async with db_manager.postgres_engine.begin() as conn:
                await conn.execute("SELECT 1")
            health_status["postgres"] = "healthy"
        elif db_manager.postgres_sync_engine:
            with db_manager.postgres_sync_engine.begin() as conn:
                conn.execute("SELECT 1")
            health_status["postgres"] = "healthy (sync)"
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")
    
    # Check MongoDB
    try:
        if db_manager.mongo_client:
            await db_manager.mongo_client.admin.command('ping')
            health_status["mongodb"] = "healthy"
    except Exception as e:
        logger.error(f"MongoDB health check failed: {e}")
    
    # Check Redis
    try:
        if db_manager.redis_client:
            await db_manager.redis_client.ping()
            health_status["redis"] = "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
    
    return health_status
