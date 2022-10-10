from os import environ

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from redis import Redis

logger = get_task_logger(__name__)

redis_host = environ.get('OMNOMNOM_REDIS_HOST') or 'localhost'
redis_port = environ.get('OMNOMNOM_REDIS_PORT') or 6379

cache_ttl = environ.get('OMNOMNOM_CACHE_INTERVAL') or 60 * 60 * 24 * 7 * 52
cache_database = environ.get('OMNOMNOM_CACHE_DATABASE') or 0

celery_database = environ.get('OMNOMNOM_CELERY_DATABASE') or 1

cache = Redis(host=redis_host, port=redis_port, db=cache_database)
cache_date_format = '%Y-%m-%d'

app = Celery('backend',
             broker='redis://%s:%s/%s' % (redis_host, redis_port, celery_database),
             include=[
                 'canteens.cafenero',
                 'canteens.personalkantine',
                 'canteens.singh',
                 'canteens.studierendenwerk'
             ]
             )

app.conf.task_default_queue = 'canteens'

def worker():
    app.start(argv=['worker', '-l', 'info', '-Q', 'canteens'])
