#!/usr/bin/env python3

# A simple Telegram bot to get canteen information.
# Copyright (C) 2016  Max Rosin
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
import sys

from canteens import cache
from telegram import ChatAction, ParseMode
from telegram.ext import CommandHandler, RegexHandler, Updater
from threading import Lock
from omnomnom import OmNomNom

# logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

token = os.environ.get('TELEGRAM_BOT_AUTH_TOKEN')
if not token:
	logging.error('You have to set your auth token as environment variable in TELEGRAM_BOT_AUTH_TOKEN')
	sys.exit()

ABOUT_TEXT = """*OmNomNom*

OmNomNom is a simple Telegram bot to get canteen information. Currently it supports only canteens in Berlin (Germany) and most of its answers are in German.

The "official" version of this bot is available as [@OmnBot](https://telegram.me/OmnBot). Feel free to talk to it and invite it to your groups.

Find out more about it on [Github](https://github.com/ekeih/OmNomNom). Pull requests and issues are always welcome. If you have questions you can talk to me via [Telegram](https://telegram.me/ekeih).

OmNomNom is licensed under the [GNU AGPL v3](https://github.com/ekeih/OmNomNom#license).
"""

logger.debug('Initialize API')
updater = Updater(token=token)
dispatcher = updater.dispatcher

def __log_incomming_messages(bot, update):
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
	bot.sendMessage(chat_id=update.message.chat_id, text=ABOUT_TEXT, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def __error_handler(bot, update, error):
  logger.info(error)

logger.debug('Adding API callbacks')
dispatcher.addErrorHandler(__error_handler)
dispatcher.addHandler(CommandHandler('start', __about))
dispatcher.addHandler(CommandHandler('about', __about))
dispatcher.addHandler(CommandHandler('help', __about))
dispatcher.addHandler(RegexHandler('.*', __send_typing_action), 0)
dispatcher.addHandler(RegexHandler('.*', __log_incomming_messages), 1)

global_cache = cache.Cache()
cache_refresh = cache.Refresh(global_cache)
cache_refresh.start()

omnomnom = OmNomNom(global_cache)

# TU Berlin
dispatcher.addHandler(CommandHandler('tu_personalkantine', omnomnom.menu_makantine), 2)
dispatcher.addHandler(CommandHandler('tu_mar', omnomnom.menu_marchstrasse), 2)
dispatcher.addHandler(CommandHandler('tu_architektur', omnomnom.menu_architektur), 2)
dispatcher.addHandler(CommandHandler('tu_acker', omnomnom.menu_acker), 2)
dispatcher.addHandler(CommandHandler('tu_mensa', omnomnom.menu_mensa), 2)
dispatcher.addHandler(CommandHandler('tu_tel', omnomnom.menu_tel), 2)
dispatcher.addHandler(CommandHandler('tu_singh', omnomnom.menu_tu_singh), 2)

# HU Berlin
dispatcher.addHandler(CommandHandler('hu_nord', omnomnom.menu_hu_nord), 2)
dispatcher.addHandler(CommandHandler('hu_sued', omnomnom.menu_hu_sued), 2)
dispatcher.addHandler(CommandHandler('hu_adlershof', omnomnom.menu_hu_adlershof), 2)
dispatcher.addHandler(CommandHandler('hu_spandauer', omnomnom.menu_hu_spandauer), 2)

# FU Berlin
dispatcher.addHandler(CommandHandler('fu_veggie', omnomnom.menu_fu_1), 2)
dispatcher.addHandler(CommandHandler('fu_2', omnomnom.menu_fu_2), 2)
dispatcher.addHandler(CommandHandler('fu_lankwitz', omnomnom.menu_fu_lankwitz), 2)
dispatcher.addHandler(CommandHandler('fu_dueppel', omnomnom.menu_fu_dueppel), 2)
dispatcher.addHandler(CommandHandler('fu_cafeteria', omnomnom.menu_fu_cafeteria), 2)
dispatcher.addHandler(CommandHandler('fu_cafe_koeniginluise', omnomnom.menu_fu_cafe_koenigin_luise), 2)
dispatcher.addHandler(CommandHandler('fu_cafe_vanthoff', omnomnom.menu_fu_cafe_vant_hoff), 2)
dispatcher.addHandler(CommandHandler('fu_cafe_ihne', omnomnom.menu_fu_cafe_ihne), 2)

# UDK Berlin
dispatcher.addHandler(CommandHandler('udk_jazz_cafe', omnomnom.menu_udk_jazz_cafe), 2)

logger.info('Start polling')
updater.start_polling()
