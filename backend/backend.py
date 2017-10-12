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

refresh_minute = environ.get('OMNOMNOM_REFRESH_MINUTE') or 3
refresh_hour = environ.get('OMNOMNOM_REFRESH_HOUR') or '*/2'

cache = Redis(host=redis_host, port=redis_port, db=cache_database)
cache_date_format = '%Y-%m-%d'

app = Celery('backend',
             broker='redis://%s:%s/%s' % (redis_host, redis_port, celery_database),
             include=[
                 'canteens.cafenero',
                 'canteens.personalkantine',
                 'canteens.singh',
                 'canteens.studierendenwerk',
                 'omnomgram.tasks',
                 'stats.tasks'
             ]
             )

app.conf.task_default_queue = 'housekeeping'
app.conf.task_routes = {
    'canteens.*': {'queue': 'canteens'}
}

app.conf.beat_schedule = {
    'update cafenero': {
        'task': 'canteens.cafenero.update_cafenero',
        'schedule': crontab(hour=refresh_hour, minute=refresh_minute)
    },
    'update singh': {
        'task': 'canteens.singh.update_singh',
        'schedule': crontab(hour=refresh_hour, minute=refresh_minute)
    },
    'update personalkantine': {
        'task': 'canteens.personalkantine.update_personalkantine',
        'schedule': crontab(hour=refresh_hour, minute=refresh_minute)
    },
    'update en canteen': {
        'task': 'canteens.personalkantine.update_en_canteen',
        'schedule': crontab(hour=refresh_hour, minute=refresh_minute)
    },
    'update studierendenwerk': {
        'task': 'canteens.studierendenwerk.update_all_studierendenwerk_canteens',
        'schedule': crontab(hour=refresh_hour, minute=refresh_minute)
    }
}


def beat():
    app.start(argv=['celery', 'beat', '-l', 'info'])


def housekeeping():
    from canteens.cafenero import update_cafenero
    from canteens.personalkantine import update_personalkantine, update_en_canteen
    from canteens.singh import update_singh
    from canteens.studierendenwerk import update_all_studierendenwerk_canteens
    update_cafenero.delay()
    update_personalkantine.delay()
    update_en_canteen.delay()
    update_singh.delay()
    update_all_studierendenwerk_canteens.delay()
    app.start(argv=['celery', 'worker', '-l', 'info', '-Q', 'housekeeping'])


def worker():
    app.start(argv=['celery', 'worker', '-l', 'info', '-Q', 'canteens'])
