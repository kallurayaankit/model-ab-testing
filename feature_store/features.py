import redis
import random

# Connect to Redis (docker-compose service name 'redis')
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_user_features(user_id: int):
    """Get user features from Redis. If not present, generate random and store."""
    key = f"user:{user_id}"
    data = r.hgetall(key)
    if not data:
        # Simulate fresh features
        data = {
            'user_age': random.randint(18, 70),
            'user_genre_action': round(random.random(), 2),
            'user_genre_comedy': round(random.random(), 2),
        }
        r.hmset(key, data)
    # Also add a dummy 'item_popularity' feature
    data['item_popularity'] = round(random.random(), 2)
    return data