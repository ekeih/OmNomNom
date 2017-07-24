#!/usr/bin/env python3

# Copyright (C) 2017  Max Rosin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import redis
import sys
import textwrap

from telegram import Bot, ChatAction, ParseMode
from telegram.ext import CommandHandler, RegexHandler, Updater
from omnomgram.tasks import send_message_to_admin

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logging.getLogger('JobQueue').setLevel(logging.INFO)
logging.getLogger('telegram').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)

redis_host = os.environ.get('OMNOMNOM_REDIS_HOST') or 'localhost'
cache = redis.Redis(host=redis_host, decode_responses=True)

token = os.environ.get('OMNOMNOM_AUTH_TOKEN')
if not token:
    logging.error('You have to set your auth token as environment variable in OMNOMNOM_AUTH_TOKEN')
    sys.exit()

ADMIN = os.environ.get('OMNOMNOM_ADMIN')
if not ADMIN:
    logger.error('You have to specify an Admin account.')
    sys.exit()

ABOUT_TEXT = """*OmNomNom*

OmNomNom is a Telegram bot to get canteen information. Currently it supports only canteens in Berlin (Germany) \
and most of its answers are in German.
The "official" version of this bot is available as [@OmnBot](https://telegram.me/OmnBot). Feel free to talk to it and \
invite it to your groups.
Find out more about it on [Github](https://github.com/ekeih/OmNomNom). Pull requests and issues are always welcome. If \
you have questions you can talk to me via [Telegram](https://telegram.me/ekeih).

OmNomNom is licensed under the [GNU AGPL v3](https://github.com/ekeih/OmNomNom#license).
"""

logger.debug('Initialize API')
updater = Updater(token=token)
bot = Bot(token)
dispatcher = updater.dispatcher


def __log_incoming_messages(bot, update):
    chat = update.message.chat
    target_chat = ''
    if chat.type == 'group':
        target_chat = chat.title
    elif chat.type == 'private':
        if chat.first_name:
            target_chat += chat.first_name
        if chat.last_name:
            target_chat += ' %s' % chat.last_name
        if chat.username:
            target_chat += ' (%s)' % chat.username
    logger.info('In:  %s: %s' % (target_chat, update.message.text))


def __send_typing_action(bot, update):
    logger.debug("Send typing")
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)


def __about(bot, update):
    update.message.reply_text(text=ABOUT_TEXT, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def __error_handler(bot, update, error):
    error_message = """\
                    *Some Frontend Error*
                    *Update*
                    ```
                    %s
                    ```
                    *Error*
                    ```
                    %s
                    ```
                    """ % (update, error)
    send_message_to_admin.delay(textwrap.dedent(error_message))
    logger.info(error)


def __menu(bot, update):
    if update.message.text:
        requested_canteen = update.message.text[1:].replace(bot.name, '')
        logger.debug('Requested Canteen: %s' % requested_canteen)
        reply = cache.get(requested_canteen)
        if not reply or reply.strip() == '':
            error_message = """\
                            *Chat*
                            ```
                            %s
                            ```
                            *Message*
                            ```
                            %s
                            ```
                            *User*
                            ```
                            %s
                            ```
                            """ % (update.effective_chat, update.effective_message, update.effective_user)
            send_message_to_admin.delay(textwrap.dedent(error_message))
            reply = 'Leider kenne ich keinen passenden Speiseplan. Wenn das ein Fehler ist, wende dich an @ekeih.'
        logger.debug(reply)
        update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

logger.debug('Adding API callbacks')
dispatcher.add_error_handler(__error_handler)
dispatcher.add_handler(CommandHandler('start', __about), 2)
dispatcher.add_handler(CommandHandler('about', __about), 2)
dispatcher.add_handler(CommandHandler('help', __about), 2)
dispatcher.add_handler(RegexHandler('.*', __send_typing_action), 0)
dispatcher.add_handler(RegexHandler('.*', __log_incoming_messages), 1)
dispatcher.add_handler(RegexHandler('/.*', __menu), 2)

start_message = """*Bot Started*

ID: %s
Firstname: %s
Lastname: %s
Username: %s
Name: %s
""" % (bot.id, bot.first_name, bot.last_name, bot.username, bot.name)

send_message_to_admin.delay(start_message)

logger.info('Start polling')
updater.start_polling()
