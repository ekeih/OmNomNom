from os import environ

from celery.utils.log import get_task_logger
from telegram import Bot, ParseMode

from backend.backend import app

logger = get_task_logger(__name__)

token = environ.get('OMNOMNOM_AUTH_TOKEN')
ADMIN = environ.get('OMNOMNOM_ADMIN')
bot = Bot(token)


@app.task
def send_message_to_admin(message):
    bot.send_message(chat_id=ADMIN, text=message, parse_mode=ParseMode.MARKDOWN)
    logger.info('Send to Admin: %s' % message)
