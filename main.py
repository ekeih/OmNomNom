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
dispatcher.addHandler(CommandHandler('personalkantine', OmNomNom.menu_makantine), 'parsing_command')
dispatcher.addHandler(CommandHandler('mar', OmNomNom.menu_marchstrasse), 'parsing_command')
dispatcher.addHandler(CommandHandler('a', OmNomNom.menu_architektur), 'parsing_command')
dispatcher.addHandler(CommandHandler('acker', OmNomNom.menu_acker), 'parsing_command')
dispatcher.addHandler(CommandHandler('mensa', OmNomNom.menu_mensa), 'parsing_command')
dispatcher.addHandler(CommandHandler('tel', OmNomNom.menu_tel), 'parsing_command')

# HU Berlin
dispatcher.addHandler(CommandHandler('hunord', OmNomNom.menu_hu_nord), 'parsing_command')
dispatcher.addHandler(CommandHandler('husued', OmNomNom.menu_hu_sued), 'parsing_command')
dispatcher.addHandler(CommandHandler('huadlershof', OmNomNom.menu_hu_adlershof), 'parsing_command')
dispatcher.addHandler(CommandHandler('huspandauer', OmNomNom.menu_hu_spandauer), 'parsing_command')

# FU Berlin
dispatcher.addHandler(CommandHandler('fu1', OmNomNom.menu_fu_1), 'parsing_command')
dispatcher.addHandler(CommandHandler('fu2', OmNomNom.menu_fu_2), 'parsing_command')
dispatcher.addHandler(CommandHandler('fulankwitz', OmNomNom.menu_fu_lankwitz), 'parsing_command')
dispatcher.addHandler(CommandHandler('fuassmannshauser', OmNomNom.menu_fu_assmannshauser), 'parsing_command')
dispatcher.addHandler(CommandHandler('fudueppel', OmNomNom.menu_fu_dueppel), 'parsing_command')
dispatcher.addHandler(CommandHandler('fucafeteria', OmNomNom.menu_fu_cafeteria), 'parsing_command')
dispatcher.addHandler(CommandHandler('fucafekoeniginluise', OmNomNom.menu_fu_cafe_koenigin_luise), 'parsing_command')
dispatcher.addHandler(CommandHandler('fucafevanthoff', OmNomNom.menu_fu_cafe_vant_hoff), 'parsing_command')
dispatcher.addHandler(CommandHandler('fucafeihne', OmNomNom.menu_fu_cafe_ihne), 'parsing_command')

dispatcher.addHandler(CommandHandler('sing', OmNomNom.menu_tu_sing), 'parsing_command')

logger.debug('Start polling')
updater.start_polling()
