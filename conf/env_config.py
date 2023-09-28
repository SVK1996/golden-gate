import logging
import redis
import psycopg2


db_pg = psycopg2.connect("host=localhost port=5432 dbname=britannica user=postgres password=password")
db_schema = 'public'

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)s %(message)s', level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S')


# Redis configuration
r_host = 'localhost'  # Replace with your Redis server host
r_port = 6379  # Default Redis port
r_db = 0  # Redis database index (usually 0)

# Create a Redis connection pool
redis_pool = redis.ConnectionPool(host=r_host, port=r_port, db=r_db)

# Function to get a Redis connection from the pool
def get_redis_connection():
    return redis.Redis(connection_pool=redis_pool)

SECRET_KEY = 'your-secret-key'