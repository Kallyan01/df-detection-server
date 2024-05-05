from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        namespace='CELERY',
        CELERY_WORKER_POOL = 'eventlet'
    )
    celery.conf.update(app.config)
    return celery
