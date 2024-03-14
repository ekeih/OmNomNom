from telegram.ext import CallbackContext, JobQueue

from canteens.cafenero import update_cafenero
from canteens.personalkantine import update_en_canteen, update_personalkantine
from canteens.singh import update_singh
from canteens.studierendenwerk import update_all_studierendenwerk_canteens


def schedule(job_queue: JobQueue) -> None:
    job_queue.run_repeating(update_cafenero_timer, interval=60 * 60 * 2, first=5)
    job_queue.run_repeating(update_personalkantine_timer, interval=60 * 60 * 2, first=5)
    job_queue.run_repeating(update_en_canteen_timer, interval=60 * 60 * 2, first=5)
    job_queue.run_repeating(update_singh_timer, interval=60 * 60 * 2, first=5)
    job_queue.run_repeating(update_all_studierendenwerk_canteens_timer, interval=60 * 60 * 2, first=5)

async def update_cafenero_timer(context: CallbackContext) -> None:
    update_cafenero.delay()
async def update_personalkantine_timer(context: CallbackContext) -> None:
    update_personalkantine.delay()
async def update_en_canteen_timer(context: CallbackContext) -> None:
    update_en_canteen.delay()
async def update_singh_timer(context: CallbackContext) -> None:
    update_singh.delay()
async def update_all_studierendenwerk_canteens_timer(context: CallbackContext) -> None:
    update_all_studierendenwerk_canteens.delay()
