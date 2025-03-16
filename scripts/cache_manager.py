from app.core.redis_client import redis_client
import json

# Cache keys
HDFS_SAMPLES_KEY = "hdfs_samples"
HIVE_METADATA_KEY = "hive_metadata"
CACHE_EXPIRATION = 3600

def cache_hdfs_samples(samples: dict):
    """Stores HDFS samples in Redis."""
    redis_client.setex(HDFS_SAMPLES_KEY, CACHE_EXPIRATION, json.dumps(samples))

def get_cached_hdfs_samples():
    """Retrieves cached HDFS samples from Redis."""
    cached_data = redis_client.get(HDFS_SAMPLES_KEY)
    return json.loads(cached_data) if cached_data else None

def cache_hive_metadata(metadata: list):
    """Stores Hive metadata in Redis."""
    redis_client.setex(HIVE_METADATA_KEY, CACHE_EXPIRATION, json.dumps(metadata))

def get_cached_hive_metadata():
    """Retrieves cached Hive metadata from Redis."""
    cached_data = redis_client.get(HIVE_METADATA_KEY)
    return json.loads(cached_data) if cached_data else None