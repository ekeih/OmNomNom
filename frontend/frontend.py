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
from backend.backend import cache_date_format
from stats.tasks import log_error, log_to_influxdb
from telegram import Bot, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)

from frontend.schedule import schedule
from frontend.strings import about_text, goodbye, help_text

logging.getLogger('JobQueue').setLevel(logging.INFO)
logging.getLogger('telegram').setLevel(logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

logging_format = '[%(asctime)s: %(levelname)s/%(name)s] %(message)s'
formatter = logging.Formatter(logging_format)
logging.basicConfig(level=logging.INFO, format=logging_format)

frontend_logger = logging.getLogger('frontend')
frontend_fh = None
message_logger = logging.getLogger('frontend.messages')
message_fh = None
cache = None

async def send_message_to_admin(bot: Bot, message: str) -> None:
    admin = os.environ.get('OMNOMNOM_ADMIN')
    await bot.send_message(chat_id=admin, text=message, parse_mode=ParseMode.MARKDOWN)


def get_canteen_and_date(message):
    """
    Extract canteen and date from a message.

    Args:
        message (str): The message from the user. It should have the format '/mensa date' (without @BotName).

    Returns:
        (tuple): Tuple containing:

            canteen(str): The requested canteen.

            date(str): The date in the format '2017-10-16'.
    """

    def parse_date(date_string):
        """Try to extract the date with dateparser."""
        def try_dateparser(d):
            settings = {'PREFER_DATES_FROM': 'future', 'DATE_ORDER': 'DMY'}
            return dateparser.parse(d, settings=settings)

        def try_parsedatetime(d):
            """Try to extract the date with parsedatetime."""
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

    s = message.split()
    canteen = s.pop(0)[1:]
    if len(s) > 0:
        date = parse_date(' '.join(s))
        if date:
            return canteen, date.strftime(cache_date_format)
        else:
            return canteen, False
    else:
        return canteen, datetime.date.today().strftime(cache_date_format)


async def log_incoming_messages(update: Update, _: CallbackContext) -> None:
    """Log incoming messages to a log file and influxdb."""
    frontend_logger.debug('incoming messages: %s' % update)
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
    log_to_influxdb('messages', fields, tags)


async def send_typing_action(update: Update, context: CallbackContext) -> None:
    """Send 'typing...' message to chat as long as it is not a reply message."""
    if not update.message.reply_to_message:
        frontend_logger.debug("Send typing")
        await context.bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)


async def about(update: Update, _: CallbackContext) -> None:
    """Send the 'About' text about the bot."""
    message_logger.info('Out: Sending <about> message')
    await update.message.reply_text(text=about_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


async def help_message(update: Update, _: CallbackContext) -> None:
    """Send a help message with usage instructions."""
    message_logger.info('Send <help> message')
    await update.message.reply_text(text=help_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


async def menu(update: Update, context: CallbackContext) -> None:
    """
    Process the message and reply with the menu or error messages.

    Todo:
        Reduce complexity!
    """
    frontend_logger.debug('menu called')
    if update.message.text:
        message = update.message.text.lower().replace('@%s' % context.bot.username.lower(), '')
        requested_canteen, requested_date = get_canteen_and_date(message)
        frontend_logger.info('Requested Canteen: %s (%s)' % (requested_canteen, requested_date))
        if requested_date:
            reply = cache.hget(requested_date, requested_canteen)
            if not reply or reply.strip() == '':
                possible_canteens = []
                for canteen, canteen_menu in cache.hscan_iter(requested_date, '*%s*' % requested_canteen):
                    possible_canteens.append((canteen, canteen_menu))
                if len(possible_canteens) == 1:
                    reply = possible_canteens.pop()[1]
                    await update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                    message_logger.debug('Out: %s' % reply)
                    await update.message.reply_text(text=goodbye, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                elif len(possible_canteens) > 1:
                    reply = 'Meintest du vielleicht:\n'
                    for canteen in possible_canteens:
                        reply += '\n /%s' % canteen[0]
                    await update.message.reply_text(text=reply)
                    message_logger.debug('Out: %s' % reply)
                else:
                    error_message = "\n*Chat*\n```\n%s\n```\n*Message*\n```\n%s\n```\n*User*\n```\n%s\n```" % \
                                    (update.effective_chat, update.effective_message, update.effective_user)
                    await send_message_to_admin(context.bot, error_message)
                    reply = 'Leider kenne ich keinen passenden Speiseplan.'
                    await update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN)
                    message_logger.debug('Out: %s' % reply)
            else:
                await update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                message_logger.debug('Out: %s' % reply)
                await update.message.reply_text(text=goodbye, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        else:
            reply = 'Sorry, leider habe ich das Datum nicht verstanden. Probier es doch einmal mit `/%s morgen`, ' \
                    '`/%s dienstag`, `/%s yesterday` oder `/%s next friday`.' % (requested_canteen, requested_canteen,
                                                                                 requested_canteen, requested_canteen)
            await update.message.reply_text(text=reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            message_logger.debug('Out: %s' % reply)


async def group_message_handler(update: Update, context: CallbackContext) -> None:
    """
    Handle events that are specific for groups. Currently it only sends a help message when the bot is invited to a new
    group.
    """
    frontend_logger.info('Group members changed')
    frontend_logger.debug(update)
    my_id = context.bot.get_me().id
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.id == my_id:
                frontend_logger.info('I was invited to a group :)')
                await help_message(context.bot, update)


async def error_handler(update: Update, context: CallbackContext) -> None:
    """
    Handle errors in the dispatcher and decide which errors are just logged and which errors are important enough to
    trigger a message to the admin.
    """
    # noinspection PyBroadException
    try:
        raise context.error
    except telegram.error.BadRequest:
        frontend_logger.error(context.error)
        log_error(str(context.error), 'frontend', 'badrequest')
    except telegram.error.TimedOut:
        frontend_logger.error(context.error)
        log_error(str(context.error), 'frontend', 'timeout')
    except:
        error_message = '*Some Frontend Error*\n\n*Update*\n```\n%s\n```\n*Error*\n```\n%s\n```' % (update, context.error)
        await send_message_to_admin(context.bot, error_message)
        frontend_logger.error(context.error)

async def post_init(application: Application) -> None:
    await send_message_to_admin(application.bot, '*Bot Started*\n\nID: %s\nFirstname: %s\nLastname: %s\nUsername: %s\nName: %s' %
                                (application.bot.id, application.bot.first_name, application.bot.last_name,
                                application.bot.username, application.bot.name))

def main() -> None:
    """
    The entrypoint for omnbot-frontend. The main function adds all handlers to the telegram dispatcher, informs the
    admin about the startup and runs the dispatcher forever.
    """
    global frontend_fh
    global message_fh
    global cache

    frontend_fh = logging.StreamHandler(sys.stdout)
    frontend_fh.setLevel(logging.DEBUG)
    frontend_fh.setFormatter(formatter)
    frontend_logger.addHandler(frontend_fh)

    message_fh = logging.StreamHandler(sys.stdout)
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

    admin = os.environ.get('OMNOMNOM_ADMIN')
    if not admin:
        frontend_logger.error('You have to specify an Admin account.')
        sys.exit()
    frontend_logger.debug('Admin ID: %s' % admin)

    application = Application.builder().token(token).post_init(post_init).build()

    # Add an error handler to log and report errors
    application.add_error_handler(error_handler)

    # React to /start, /about and /help messages
    application.add_handler(CommandHandler('start', help_message), 2)
    application.add_handler(CommandHandler('about', about), 2)
    application.add_handler(CommandHandler('help', help_message), 2)

    # Send typing action and log incoming messages
    application.add_handler(MessageHandler(filters.Regex('.*'), send_typing_action), 0)
    application.add_handler(MessageHandler(filters.Regex('.*'), log_incoming_messages), 1)

    # Handle all messages beginning with a '/'
    application.add_handler(MessageHandler(filters.Regex('/.*'), menu), 2)

    # Handle normal text messages that are no reply and answer with a help_message
    application.add_handler(MessageHandler(filters.TEXT & (~ filters.REPLY), help_message), 2)

    # Handle group member changes
    application.add_handler(MessageHandler(filters.ChatType.GROUPS & (~ filters.REPLY), group_message_handler), 3)

    # Schedule canteen updates
    schedule(application.job_queue)

    frontend_logger.info('Start polling')
    application.run_polling()
