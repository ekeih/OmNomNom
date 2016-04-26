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

import config # has to set BOT_USERNAME, AUTH_TOKEN
import logging
import sys

from telegram.ext import CommandHandler, Updater
from omnomnom import OmNomNom

# logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

logger.debug('Initialize API')
updater = Updater(token=config.AUTH_TOKEN)
dispatcher = updater.dispatcher

def __start_conversation(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Hello, I know the menus for some canteens in Berlin (Germany).")

logger.debug('Adding API callbacks')
dispatcher.addHandler(CommandHandler('start', __start_conversation))

# TU Berlin
dispatcher.addHandler(CommandHandler('personalkantine', OmNomNom.menu_makantine))
dispatcher.addHandler(CommandHandler('mar', OmNomNom.menu_marchstrasse))
dispatcher.addHandler(CommandHandler('a', OmNomNom.menu_architektur))
dispatcher.addHandler(CommandHandler('acker', OmNomNom.menu_acker))
dispatcher.addHandler(CommandHandler('mensa', OmNomNom.menu_mensa))
dispatcher.addHandler(CommandHandler('tel', OmNomNom.menu_tel))

# HU Berlin
dispatcher.addHandler(CommandHandler('hunord', OmNomNom.menu_hu_nord))
dispatcher.addHandler(CommandHandler('husued', OmNomNom.menu_hu_sued))
dispatcher.addHandler(CommandHandler('huadlershof', OmNomNom.menu_hu_adlershof))
dispatcher.addHandler(CommandHandler('huspandauer', OmNomNom.menu_hu_spandauer))

# FU Berlin
dispatcher.addHandler(CommandHandler('fu1', OmNomNom.menu_fu_1))
dispatcher.addHandler(CommandHandler('fu2', OmNomNom.menu_fu_2))
dispatcher.addHandler(CommandHandler('fulankwitz', OmNomNom.menu_fu_lankwitz))
dispatcher.addHandler(CommandHandler('fuassmannshauser', OmNomNom.menu_fu_assmannshauser))
dispatcher.addHandler(CommandHandler('fudueppel', OmNomNom.menu_fu_dueppel))
dispatcher.addHandler(CommandHandler('fucafeteria', OmNomNom.menu_fu_cafeteria))
dispatcher.addHandler(CommandHandler('fucafekoeniginluise', OmNomNom.menu_fu_cafe_koenigin_luise))
dispatcher.addHandler(CommandHandler('fucafevanthoff', OmNomNom.menu_fu_cafe_vant_hoff))
dispatcher.addHandler(CommandHandler('fucafeihne', OmNomNom.menu_fu_cafe_ihne))

logger.debug('Start polling')
updater.start_polling()
