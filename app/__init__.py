from flask import Flask
from .config import make_celery
from flask_cors import CORS
import os
from dotenv import load_dotenv
import redis 
ENV ={
    'dev' : '.env.dev',
    'prod' : '.env.prod',
}
load_dotenv(ENV[os.getenv('FLASK_ENV')])
redis_result_cache_db = redis.Redis.from_url(os.getenv('RESULT_CACHE_DB'))
redis_uuid_map_db = redis.Redis.from_url(os.getenv('UUID_MAP_DB'))

print("------------------------------------------------")
print(os.getenv('ENV_TYPE'))
print("------------------------------------------------")

flask_env = os.getenv('FLASK_ENV')
if flask_env is None:
    flask_env = 'dev'  # Set a default value if FLASK_ENV is not set
load_dotenv(ENV[flask_env])
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')
CORS(app)
celery = make_celery(app)

from app import routes
