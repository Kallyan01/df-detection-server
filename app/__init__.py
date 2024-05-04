from flask import Flask
from .config import make_celery
from flask_cors import CORS
import os
from dotenv import load_dotenv
ENV ={
    'dev' : '.env.dev',
    'prod' : '.env.prod',
}

flask_env = os.getenv('FLASK_ENV')
if flask_env is None:
    flask_env = 'dev'  # Set a default value if FLASK_ENV is not set
load_dotenv(ENV[flask_env])
print(os.getenv('ENV_TYPE'))
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')
CORS(app)
celery = make_celery(app)

