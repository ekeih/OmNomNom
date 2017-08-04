from backend.backend import app, cache, cache_interval
from celery.utils.log import get_task_logger

import canteens.cafenero
import canteens.singh
import canteens.personalkantine
import canteens.studierendenwerk
import time

logger = get_task_logger(__name__)


def update_canteens(canteens):
    for canteen in canteens:
        logger.info('[Update] %s' % canteen.name)
        menu = canteen.update(url=canteen.url)
        if menu:
            cache.set(canteen.id_, menu, ex=cache_interval*4)
        time.sleep(3)


@app.task(bind=True, default_retry_delay=30)
def update_cafenero(self):
    try:
        update_canteens(canteens.cafenero.CANTEENS)
        return 'Cafenero Done'
    except Exception as ex:
        raise self.retry(exc=ex)


@app.task(bind=True, default_retry_delay=30)
def update_personalkantine(self):
    try:
        update_canteens(canteens.personalkantine.CANTEENS)
        return 'Personalkantine Done'
    except Exception as ex:
        raise self.retry(exc=ex)


@app.task(bind=True, default_retry_delay=30)
def update_singh(self):
    try:
        update_canteens(canteens.singh.CANTEENS)
        return 'Singh Done'
    except Exception as ex:
        raise self.retry(exc=ex)


@app.task(bind=True, default_retry_delay=30)
def update_studierendenwerk(self):
    try:
        update_canteens(canteens.studierendenwerk.CANTEENS)
        return 'Studierendenwerk Done'
    except Exception as ex:
        raise self.retry(exc=ex)
