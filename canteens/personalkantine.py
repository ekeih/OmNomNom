import datetime

from backend.backend import app, cache, cache_date_format, cache_ttl
from celery.utils.log import get_task_logger

from canteens.canteen import get_current_week, get_next_week

logger = get_task_logger(__name__)

def get_date_range():
    today = datetime.date.today()
    if today.weekday() > 4:
        return get_next_week()
    else:
        return get_current_week()


@app.task(bind=True, default_retry_delay=30)
def update_personalkantine(self):
    try:
        logger.info('[Update] TU Personalkantine')
        for day in get_date_range():
            if menu:
                menu = 'Die Personalkantine hat leider bis auf weiteres geschlossen. (https://personalkantine.personalabteilung.tu-berlin.de)'
                cache.hset(day.strftime(cache_date_format), 'tu_personalkantine', menu)
                cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)


@app.task(bind=True, default_retry_delay=30)
def update_en_canteen(self):
    try:
        logger.info('[Update] TU EN Canteen')
        for day in get_date_range():
            if menu:
                menu = 'Die EN-Kantine hat ihren Speiseplan leider nicht mehr online. (https://personalkantine.personalabteilung.tu-berlin.de)'
                cache.hset(day.strftime(cache_date_format), 'tu_en_kantine', menu)
                cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)
