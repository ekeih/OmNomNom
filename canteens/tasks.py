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
        cache.set(canteen.id_, menu, ex=cache_interval*2)
        time.sleep(3)


@app.task
def update_cafenero():
    update_canteens(canteens.cafenero.CANTEENS)
    return 'Cafenero Done'


@app.task
def update_personalkantine():
    update_canteens(canteens.personalkantine.CANTEENS)
    return 'Personalkantine Done'


@app.task
def update_singh():
    update_canteens(canteens.singh.CANTEENS)
    return 'Singh Done'


@app.task
def update_studierendenwerk():
    update_canteens(canteens.studierendenwerk.CANTEENS)
    return 'Studierendenwerk Done'
