#!/usr/bin/env python3

# A simple Telegram bot to get canteen information

#    Copyright (C) 2015  Max Rosin git@hackrid.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import config # has to set BOT_USERNAME, AUTH_TOKEN
import logging
import sys

from telegram.ext import Updater
from omnomnom import OmNomNom

# logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# initialize API
updater = Updater(token=config.AUTH_TOKEN)
dispatcher = updater.dispatcher

dispatcher.addTelegramCommandHandler('start', OmNomNom.start)
dispatcher.addTelegramCommandHandler('speiseplan', OmNomNom.menu_listing)
dispatcher.addTelegramCommandHandler('personalkantine', OmNomNom.menu_makantine)

updater.start_polling()

sys.exit(0)