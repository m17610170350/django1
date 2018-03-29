from django_redis import get_redis_connection


cli = get_redis_connection()
cli.lpush('py5', 5)
RESULT = cli.lrange('py5')
print(RESULT)