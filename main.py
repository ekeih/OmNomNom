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

from telegram.ext import Updater
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
dispatcher.addTelegramCommandHandler('start', __start_conversation)

# TU Berlin
dispatcher.addTelegramCommandHandler('personalkantine', OmNomNom.menu_makantine)
dispatcher.addTelegramCommandHandler('mar', OmNomNom.menu_marchstrasse)
dispatcher.addTelegramCommandHandler('a', OmNomNom.menu_architektur)
dispatcher.addTelegramCommandHandler('acker', OmNomNom.menu_acker)
dispatcher.addTelegramCommandHandler('mensa', OmNomNom.menu_mensa)
dispatcher.addTelegramCommandHandler('tel', OmNomNom.menu_tel)

# HU Berlin
dispatcher.addTelegramCommandHandler('HUNord', OmNomNom.menu_hu_nord)
dispatcher.addTelegramCommandHandler('HUSued', OmNomNom.menu_hu_sued)
dispatcher.addTelegramCommandHandler('HUAdlershof', OmNomNom.menu_hu_adlershof)
dispatcher.addTelegramCommandHandler('HUSpandauer', OmNomNom.menu_hu_spandauer)

# FU Berlin
dispatcher.addTelegramCommandHandler('FU1', OmNomNom.menu_fu_1)
dispatcher.addTelegramCommandHandler('FU2', OmNomNom.menu_fu_2)
dispatcher.addTelegramCommandHandler('FULankwitz', OmNomNom.menu_fu_lankwitz)
dispatcher.addTelegramCommandHandler('FUAssmannshauser', OmNomNom.menu_fu_assmannshauser)
dispatcher.addTelegramCommandHandler('FUDueppel', OmNomNom.menu_fu_dueppel)
dispatcher.addTelegramCommandHandler('FUCafeteria', OmNomNom.menu_fu_cafeteria)
dispatcher.addTelegramCommandHandler('FUCafeKoeniginLuise', OmNomNom.menu_fu_cafe_koenigin_luise)
dispatcher.addTelegramCommandHandler('FUCafeVantHoff', OmNomNom.menu_fu_cafe_vant_hoff)
dispatcher.addTelegramCommandHandler('FUCafeIhne', OmNomNom.menu_fu_cafe_ihne)

logger.debug('Start polling')
updater.start_polling()
