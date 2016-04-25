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

import canteens.matheparser
import canteens.studentenwerk
import telegram
import time

class OmNomNom:
  def menu_makantine(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text = canteens.matheparser.get_menu(time.strftime('%d.%m.%Y'))
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def menu_marchstrasse(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text = canteens.studentenwerk.menu_mar()
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def menu_architektur(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text = canteens.studentenwerk.menu_a()
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def menu_acker(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text = canteens.studentenwerk.menu_acker()
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def menu_mensa(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text = canteens.studentenwerk.menu_mensa()
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def menu_tel(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text = canteens.studentenwerk.menu_tel()
    bot.sendMessage(chat_id=update.message.chat_id, text=text)
