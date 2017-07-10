from celery import Celery
from celery.utils.log import get_task_logger
from os import environ
from redis import Redis

logger = get_task_logger(__name__)

redis_host = environ.get('OMNOMNOM_REDIS_HOST') or 'localhost'
redis_port = environ.get('OMNOMNOM_REDIS_PORT') or 6379

cache_interval = environ.get('OMNOMNOM_CACHE_INTERVAL') or 60 * 60
cache_database = environ.get('OMNOMNOM_CACHE_DATABASE') or 0

celery_database = environ.get('OMNOMNOM_CELERY_DATABASE') or 1

cache = Redis(host=redis_host, port=redis_port, db=cache_database)

app = Celery('backend',
             broker='redis://%s:%s/%s' % (redis_host, redis_port, celery_database),
             include=[
                 'canteens.tasks',
                 'omnomgram.tasks'
             ]
             )
app.conf.timezone = 'Europe/Berlin'
app.conf.beat_schedule = {
    'update singh': {
        'task': 'canteens.tasks.update_singh',
        'schedule': cache_interval
    },
    'update personalkantine': {
        'task': 'canteens.tasks.update_personalkantine',
        'schedule': cache_interval
    },
    'update studierendenwerk': {
        'task': 'canteens.tasks.update_studierendenwerk',
        'schedule': cache_interval
    }
}


if __name__ == '__main__':
    app.start()
