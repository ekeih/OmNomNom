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

from telegram import ChatAction
from telegram.ext import CommandHandler, RegexHandler, Updater
from omnomnom import OmNomNom

# logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

token = os.environ.get('TELEGRAM_BOT_AUTH_TOKEN')
if not token:
	logging.error('You have to set your auth token as environment variable in TELEGRAM_BOT_AUTH_TOKEN')
	sys.exit()

logger.debug('Initialize API')
updater = Updater(token=token)
dispatcher = updater.dispatcher

def __start_conversation(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Hello, I know the menus for some canteens in Berlin (Germany).")

def __send_typing_action(bot, update):
  logger.debug("Send typing")
  bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)

def __error_handler(bot, update, error):
  logger.info(error)

logger.debug('Adding API callbacks')
dispatcher.addErrorHandler(__error_handler)
dispatcher.addHandler(CommandHandler('start', __start_conversation))
dispatcher.addHandler(RegexHandler('.*', __send_typing_action))

# TU Berlin
dispatcher.addHandler(CommandHandler('personalkantine', OmNomNom.menu_makantine), 1)
dispatcher.addHandler(CommandHandler('mar', OmNomNom.menu_marchstrasse), 1)
dispatcher.addHandler(CommandHandler('a', OmNomNom.menu_architektur), 1)
dispatcher.addHandler(CommandHandler('acker', OmNomNom.menu_acker), 1)
dispatcher.addHandler(CommandHandler('mensa', OmNomNom.menu_mensa), 1)
dispatcher.addHandler(CommandHandler('tel', OmNomNom.menu_tel), 1)
dispatcher.addHandler(CommandHandler('singh', OmNomNom.menu_tu_singh), 1)

# HU Berlin
dispatcher.addHandler(CommandHandler('hunord', OmNomNom.menu_hu_nord), 1)
dispatcher.addHandler(CommandHandler('husued', OmNomNom.menu_hu_sued), 1)
dispatcher.addHandler(CommandHandler('huadlershof', OmNomNom.menu_hu_adlershof), 1)
dispatcher.addHandler(CommandHandler('huspandauer', OmNomNom.menu_hu_spandauer), 1)

# FU Berlin
dispatcher.addHandler(CommandHandler('fu1', OmNomNom.menu_fu_1), 1)
dispatcher.addHandler(CommandHandler('fu2', OmNomNom.menu_fu_2), 1)
dispatcher.addHandler(CommandHandler('fulankwitz', OmNomNom.menu_fu_lankwitz), 1)
dispatcher.addHandler(CommandHandler('fuassmannshauser', OmNomNom.menu_fu_assmannshauser), 1)
dispatcher.addHandler(CommandHandler('fudueppel', OmNomNom.menu_fu_dueppel), 1)
dispatcher.addHandler(CommandHandler('fucafeteria', OmNomNom.menu_fu_cafeteria), 1)
dispatcher.addHandler(CommandHandler('fucafekoeniginluise', OmNomNom.menu_fu_cafe_koenigin_luise), 1)
dispatcher.addHandler(CommandHandler('fucafevanthoff', OmNomNom.menu_fu_cafe_vant_hoff), 1)
dispatcher.addHandler(CommandHandler('fucafeihne', OmNomNom.menu_fu_cafe_ihne), 1)

logger.debug('Start polling')
updater.start_polling()
