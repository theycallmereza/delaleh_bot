import redis

from src import config

# Connect to Redis (change host and port if needed)
REDIS_HOST = config.REDIS_HOST
REDIS_PORT = config.REDIS_PORT
REDIS_DB = config.REDIS_DB
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


# Example of setting a key-value pair
def set_token(telegram_id, access_token, refresh_token):
    redis_client.set(f"{telegram_id}:access_token", access_token)
    redis_client.set(f"{telegram_id}:refresh_token", refresh_token)


# Example of getting a token
def get_token(telegram_id):
    access_token = redis_client.get(f"{telegram_id}:access_token")
    refresh_token = redis_client.get(f"{telegram_id}:refresh_token")
    return access_token, refresh_token
