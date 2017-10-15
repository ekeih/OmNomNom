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

import datetime
import logging
import os
import sys

import dateparser
import parsedatetime
import redis
import telegram.error
from telegram import Bot, ChatAction, ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, RegexHandler, Updater

from backend.backend import cache_date_format
from frontend.strings import about_text, help_text
from omnomgram.tasks import send_message_to_admin
from stats.tasks import log_error, log_to_influxdb

logging.getLogger('JobQueue').setLevel(logging.INFO)
logging.getLogger('telegram').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)

logging_format = '[%(asctime)s: %(levelname)s/%(name)s] %(message)s'
formatter = logging.Formatter(logging_format)
logging.basicConfig(level=logging.INFO, format=logging_format)

frontend_logger = logging.getLogger('frontend')
frontend_fh = logging.handlers.TimedRotatingFileHandler('logs/frontend.log', when='midnight', backupCount=60)
frontend_fh.setLevel(logging.DEBUG)
frontend_fh.setFormatter(formatter)
frontend_logger.addHandler(frontend_fh)

message_logger = logging.getLogger('frontend.messages')
message_fh = logging.handlers.TimedRotatingFileHandler('logs/messages.log', when='midnight', backupCount=60)
message_fh.setLevel(logging.DEBUG)
message_fh.setFormatter(formatter)
message_logger.addHandler(message_fh)

redis_host = os.environ.get('OMNOMNOM_REDIS_HOST') or 'localhost'
frontend_logger.debug('Redis host: %s' % redis_host)

cache = redis.Redis(host=redis_host, decode_responses=True)

token = os.environ.get('OMNOMNOM_AUTH_TOKEN')
if not token:
    frontend_logger.error('You have to set your auth token as environment variable in OMNOMNOM_AUTH_TOKEN')
    sys.exit()

ADMIN = os.environ.get('OMNOMNOM_ADMIN')
if not ADMIN:
    frontend_logger.error('You have to specify an Admin account.')
    sys.exit()
frontend_logger.debug('Admin ID: %s' % ADMIN)

updater = Updater(token=token)
bot_instance = Bot(token)
dispatcher = updater.dispatcher

START_TEXT = """*Bot Started*

ID: %s
Firstname: %s
Lastname: %s
Username: %s
Name: %s
""" % (bot_instance.id, bot_instance.first_name, bot_instance.last_name, bot_instance.username, bot_instance.name)


def get_canteen_and_date(message):
    def parse_date(date_string):
        def try_dateparser(d):
            settings = {'PREFER_DATES_FROM': 'future', 'DATE_ORDER': 'DMY'}
            return dateparser.parse(d, settings=settings)

        def try_parsedatetime(d):
            cal = parsedatetime.Calendar()
            time_struct, parse_status = cal.parse(d)
            if parse_status > 0:
                return datetime.datetime(*time_struct[:6])
            else:
                return False

        try_date = try_dateparser(date_string)
        if try_date:
            return try_date
        else:
            try_date = try_parsedatetime(date_string)
            if try_date:
                return try_date
            else:
                return False

    s = message.replace(bot_instance.name.lower(), '').split()
    canteen = s.pop(0)[1:]
    if len(s) > 0:
        date = parse_date(' '.join(s))
        if date:
            return canteen, date.strftime(cache_date_format)
        else:
            return canteen, False
    else:
        return canteen, datetime.date.today().strftime(cache_date_format)


def log_incoming_messages(_, update):
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
    message_logger.info('In: %s: %s' % (target_chat, update.message.text))
    fields = {'message': update.message.text}
    tags = {'chat': target_chat}
    log_to_influxdb.delay('messages', fields, tags)


def send_typing_action(bot, update):
    if not update.message.reply_to_message:
        frontend_logger.debug("Send typing")
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)


def about(_, update):
    message_logger.info('Out: Sending <about> message')
    update.message.reply_text(text=about_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def help_message(_, update):
    message_logger.info('Send <help> message')
    update.message.reply_text(text=help_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def menu(_, update):
    """
    Todo:
        Reduce complexity!
    """
    if update.message.text:
        requested_canteen, requested_date = get_canteen_and_date(update.message.text.lower())
        frontend_logger.info('Requested Canteen: %s (%s)' % (requested_canteen, requested_date))
        if requested_date:
            reply = cache.hget(requested_date, requested_canteen)
            if not reply or reply.strip() == '':
                possible_canteens = []
                for canteen, canteen_menu in cache.hscan_iter(requested_date, '*%s*' % requested_canteen):
                    possible_canteens.append((canteen, canteen_menu))
                if len(possible_canteens) == 1:
                    reply = possible_canteens.pop()[1]
                    update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                    message_logger.debug('Out: %s' % reply)
                elif len(possible_canteens) > 1:
                    reply = 'Meintest du vielleicht:\n'
                    for canteen in possible_canteens:
                        reply += '\n /%s' % canteen[0]
                    update.message.reply_text(text=reply)
                    message_logger.debug('Out: %s' % reply)
                else:
                    error_message = "\n*Chat*\n```\n%s\n```\n*Message*\n```\n%s\n```\n*User*\n```\n%s\n```" % \
                                    (update.effective_chat, update.effective_message, update.effective_user)
                    send_message_to_admin.delay(error_message)
                    reply = 'Leider kenne ich keinen passenden Speiseplan. ' \
                            'Wenn das ein Fehler ist, wende dich an @ekeih.'
                    update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN)
                    message_logger.debug('Out: %s' % reply)
            else:
                update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                message_logger.debug('Out: %s' % reply)
        else:
            reply = 'Sorry, leider habe ich das Datum nicht verstanden. Probier es doch einmal mit `/%s morgen`, ' \
                    '`/%s dienstag`, `/%s yesterday` oder `/%s next friday`.' % (requested_canteen, requested_canteen,
                                                                                 requested_canteen, requested_canteen)
            update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            message_logger.debug('Out: %s' % reply)


def group_message_handler(bot, update):
    """
    Handle events that are specific for groups. Currently it only sends a help message when the bot is invited to a new
    group.
    """
    frontend_logger.info('Group members changed')
    frontend_logger.debug(update)
    my_id = bot.get_me().id
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.id == my_id:
                frontend_logger.info('I was invited to a group :)')
                help_message(bot, update)


def error_handler(_, update, error):
    """
    Handle errors in the dispatcher and decide which errors are just logged and which errors are important enough to
    trigger a message to the admin.
    """
    # noinspection PyBroadException
    try:
        raise error
    except telegram.error.BadRequest:
        frontend_logger.error(error)
        log_error.delay(str(error), 'frontend', 'badrequest')
    except telegram.error.TimedOut:
        frontend_logger.error(error)
        log_error.delay(str(error), 'frontend', 'timeout')
    except:
        error_message = '*Some Frontend Error*\n\n*Update*\n```\n%s\n```\n*Error*\n```\n%s\n```' % (update, error)
        send_message_to_admin.delay(error_message)
        frontend_logger.error(error)


def main():
    """
    The entrypoint for omnbot-frontend. The main function adds all handlers to the telegram dispatcher, informs the
    admin about the startup and runs the dispatcher forever.
    """

    # Add an error handler to log and report errors
    dispatcher.add_error_handler(error_handler)

    # React to /start, /about and /help messages
    dispatcher.add_handler(CommandHandler('start', help_message), 2)
    dispatcher.add_handler(CommandHandler('about', about), 2)
    dispatcher.add_handler(CommandHandler('help', help_message), 2)

    # Send typing action and log incoming messages
    dispatcher.add_handler(RegexHandler('.*', send_typing_action), 0)
    dispatcher.add_handler(RegexHandler('.*', log_incoming_messages), 1)

    # Handle all messages beginning with a '/'
    dispatcher.add_handler(RegexHandler('/.*', menu), 2)

    # Handle normal text messages that are no reply and answer with a help_message
    dispatcher.add_handler(MessageHandler(Filters.text & (~ Filters.reply), help_message), 2)

    # Handle group member changes
    dispatcher.add_handler(MessageHandler(Filters.group & (~ Filters.reply), group_message_handler), 3)

    send_message_to_admin.delay(START_TEXT)

    frontend_logger.info('Start polling')
    updater.start_polling()
    updater.idle()
