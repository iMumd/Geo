# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Redis Cache Manager
# ═══════════════════════════════════════════════════════════════

import asyncio
import json
import redis.asyncio as redis
from typing import Optional, Any, Dict, List
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Async Redis cache manager"""
    
    def __init__(
        self,
        url: str = "redis://localhost:6379/0",
        password: Optional[str] = None,
        ssl: bool = False,
        decode_responses: bool = True,
        max_connections: int = 50
    ):
        self.url = url
        self.password = password
        self.ssl = ssl
        self.decode_responses = decode_responses
        self.max_connections = max_connections
        self._pool: Optional[redis.ConnectionPool] = None
        self._client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self._pool = redis.ConnectionPool.from_url(
                self.url,
                password=self.password,
                ssl=self.ssl,
                decode_responses=self.decode_responses,
                max_connections=self.max_connections,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            self._client = redis.Redis(connection_pool=self._pool)
            await self._client.ping()
            logger.info("Redis cache connected successfully")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, running without cache")
            self._client = None
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self._client:
            await self._client.aclose()
        if self._pool:
            await self._pool.disconnect()
        logger.info("Redis cache disconnected")
    
    def _ensure_connected(self):
        """Check if Redis is connected"""
        if not self._client:
            raise ConnectionError("Redis is not connected")
    
    # Basic Operations
    async def set(self, key: str, value: Any, ex: int = None) -> bool:
        """Set a key-value pair"""
        if not self._client:
            return False
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            await self._client.set(key, value, ex=ex)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value by key"""
        if not self._client:
            return None
        
        try:
            value = await self._client.get(key)
            if value:
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """Delete a key"""
        if not self._client:
            return False
        
        try:
            await self._client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self._client:
            return False
        
        try:
            return await self._client.exists(key) > 0
        except Exception as e:
            logger.error(f"Cache exists error: {e}")
            return False
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for key"""
        if not self._client:
            return False
        
        try:
            await self._client.expire(key, seconds)
            return True
        except Exception as e:
            logger.error(f"Cache expire error: {e}")
            return False
    
    async def ttl(self, key: str) -> int:
        """Get TTL for key"""
        if not self._client:
            return -1
        
        try:
            return await self._client.ttl(key)
        except Exception as e:
            logger.error(f"Cache TTL error: {e}")
            return -1
    
    # Hash Operations
    async def hset(self, key: str, field: str, value: Any) -> bool:
        """Set hash field"""
        if not self._client:
            return False
        
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            await self._client.hset(key, field, value)
            return True
        except Exception as e:
            logger.error(f"Cache hset error: {e}")
            return False
    
    async def hget(self, key: str, field: str) -> Optional[Any]:
        """Get hash field"""
        if not self._client:
            return None
        
        try:
            value = await self._client.hget(key, field)
            if value:
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return None
        except Exception as e:
            logger.error(f"Cache hget error: {e}")
            return None
    
    async def hgetall(self, key: str) -> Dict[str, Any]:
        """Get all hash fields"""
        if not self._client:
            return {}
        
        try:
            data = await self._client.hgetall(key)
            result = {}
            for k, v in data.items():
                try:
                    result[k] = json.loads(v)
                except (json.JSONDecodeError, TypeError):
                    result[k] = v
            return result
        except Exception as e:
            logger.error(f"Cache hgetall error: {e}")
            return {}
    
    async def hdel(self, key: str, *fields) -> bool:
        """Delete hash fields"""
        if not self._client:
            return False
        
        try:
            await self._client.hdel(key, *fields)
            return True
        except Exception as e:
            logger.error(f"Cache hdel error: {e}")
            return False
    
    # List Operations
    async def lpush(self, key: str, *values) -> bool:
        """Push to list"""
        if not self._client:
            return False
        
        try:
            serialized = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            await self._client.lpush(key, *serialized)
            return True
        except Exception as e:
            logger.error(f"Cache lpush error: {e}")
            return False
    
    async def rpush(self, key: str, *values) -> bool:
        """Push to list from right"""
        if not self._client:
            return False
        
        try:
            serialized = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            await self._client.rpush(key, *serialized)
            return True
        except Exception as e:
            logger.error(f"Cache rpush error: {e}")
            return False
    
    async def lrange(self, key: str, start: int = 0, end: int = -1) -> List:
        """Get list range"""
        if not self._client:
            return []
        
        try:
            data = await self._client.lrange(key, start, end)
            result = []
            for item in data:
                try:
                    result.append(json.loads(item))
                except (json.JSONDecodeError, TypeError):
                    result.append(item)
            return result
        except Exception as e:
            logger.error(f"Cache lrange error: {e}")
            return []
    
    # Set Operations
    async def sadd(self, key: str, *values) -> bool:
        """Add to set"""
        if not self._client:
            return False
        
        try:
            serialized = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            await self._client.sadd(key, *serialized)
            return True
        except Exception as e:
            logger.error(f"Cache sadd error: {e}")
            return False
    
    async def smembers(self, key: str) -> set:
        """Get all set members"""
        if not self._client:
            return set()
        
        try:
            data = await self._client.smembers(key)
            result = set()
            for item in data:
                try:
                    result.add(json.loads(item))
                except (json.JSONDecodeError, TypeError):
                    result.add(item)
            return result
        except Exception as e:
            logger.error(f"Cache smembers error: {e}")
            return set()
    
    async def srem(self, key: str, *values) -> bool:
        """Remove from set"""
        if not self._client:
            return False
        
        try:
            serialized = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            await self._client.srem(key, *serialized)
            return True
        except Exception as e:
            logger.error(f"Cache srem error: {e}")
            return False
    
    # Counter Operations
    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        if not self._client:
            return 0
        
        try:
            return await self._client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Cache incr error: {e}")
            return 0
    
    async def decr(self, key: str, amount: int = 1) -> int:
        """Decrement counter"""
        if not self._client:
            return 0
        
        try:
            return await self._client.decrby(key, amount)
        except Exception as e:
            logger.error(f"Cache decr error: {e}")
            return 0
    
    # Rate Limiting
    async def rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check rate limit"""
        if not self._client:
            return True
        
        try:
            current = await self._client.get(key)
            if current is None:
                await self._client.setex(key, window, 1)
                return True
            
            if int(current) >= limit:
                return False
            
            await self._client.incr(key)
            return True
        except Exception as e:
            logger.error(f"Cache rate limit error: {e}")
            return True
    
    # Flood Control
    async def check_flood(self, user_id: int, chat_id: int, limit: int = 5, 
                         window: int = 5) -> bool:
        """Check if user is flooding"""
        key = f"flood:{chat_id}:{user_id}"
        return await self.rate_limit(key, limit, window)
    
    # Cleanup
    async def flush_pattern(self, pattern: str):
        """Flush keys matching pattern"""
        if not self._client:
            return
        
        try:
            cursor = 0
            while True:
                cursor, keys = await self._client.scan(cursor, match=pattern, count=100)
                if keys:
                    await self._client.delete(*keys)
                if cursor == 0:
                    break
        except Exception as e:
            logger.error(f"Cache flush pattern error: {e}")


# Global cache instance
cache = CacheManager()