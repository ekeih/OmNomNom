from backend.celery import app, cache, cache_interval
from celery.utils.log import get_task_logger

import backend.canteens.singh
import backend.canteens.personalkantine
import backend.canteens.studierendenwerk

logger = get_task_logger(__name__)


def update_canteens(canteens):
    for canteen in canteens:
        logger.info('[Update] %s' % canteen.name)
        menu = canteen.update(url=canteen.url)
        cache.set(canteen.id_, menu, ex=cache_interval*2)


@app.task
def update_personalkantine():
    update_canteens(backend.canteens.personalkantine.CANTEENS)
    return 'Personalkantine Done'


@app.task
def update_singh():
    update_canteens(backend.canteens.singh.CANTEENS)
    return 'Singh Done'


@app.task
def update_studierendenwerk():
    update_canteens(backend.canteens.studierendenwerk.CANTEENS)
    return 'Studierendenwerk Done'
