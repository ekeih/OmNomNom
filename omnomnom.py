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

from canteens import matheparser, singh, studentenwerk
from logging import getLogger
from telegram import ParseMode
from time import strftime

def _send_message(bot, update, text):
  logger = getLogger()
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
  logger.info('Out: %s\n%s\n' % (target_chat, text))
  bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

class OmNomNom:
  def menu_makantine(bot, update):
    text = matheparser.get_menu(strftime('%d.%m.%Y'))
    _send_message(bot, update, text)

  def menu_marchstrasse(bot, update):
    text = studentenwerk.menu_mar()
    _send_message(bot, update, text)

  def menu_architektur(bot, update):
    text = studentenwerk.menu_a()
    _send_message(bot, update, text)

  def menu_acker(bot, update):
    text = studentenwerk.menu_acker()
    _send_message(bot, update, text)

  def menu_mensa(bot, update):
    text = studentenwerk.menu_mensa()
    _send_message(bot, update, text)

  def menu_tel(bot, update):
    text = studentenwerk.menu_tel()
    _send_message(bot, update, text)

  def menu_tu_singh(bot, update):
    text = singh.get_menu()
    _send_message(bot, update, text)

# HU Berlin

  def menu_hu_nord(bot, update):
    text = studentenwerk.menu_hu_nord()
    _send_message(bot, update, text)

  def menu_hu_sued(bot, update):
    text = studentenwerk.menu_hu_sued()
    _send_message(bot, update, text)

  def menu_hu_adlershof(bot, update):
    text = studentenwerk.menu_hu_adlershof()
    _send_message(bot, update, text)

  def menu_hu_spandauer(bot, update):
    text = studentenwerk.menu_hu_spandauer()
    _send_message(bot, update, text)

# FU Berlin

  def menu_fu_1(bot, update):
    text = studentenwerk.menu_fu_1()
    _send_message(bot, update, text)

  def menu_fu_2(bot, update):
    text = studentenwerk.menu_fu_2()
    _send_message(bot, update, text)

  def menu_fu_lankwitz(bot, update):
    text = studentenwerk.menu_fu_lankwitz()
    _send_message(bot, update, text)

  def menu_fu_assmannshauser(bot, update):
    text = studentenwerk.menu_fu_assmannshauser()
    _send_message(bot, update, text)

  def menu_fu_dueppel(bot, update):
    text = studentenwerk.menu_fu_dueppel()
    _send_message(bot, update, text)

  def menu_fu_cafeteria(bot, update):
    text = studentenwerk.menu_fu_cafeteria()
    _send_message(bot, update, text)

  def menu_fu_cafe_koenigin_luise(bot, update):
    text = studentenwerk.menu_fu_cafe_koenigin_luise()
    _send_message(bot, update, text)

  def menu_fu_cafe_vant_hoff(bot, update):
    text = studentenwerk.menu_fu_cafe_vant_hoff()
    _send_message(bot, update, text)

  def menu_fu_cafe_ihne(bot, update):
    text = studentenwerk.menu_fu_cafe_ihne()
    _send_message(bot, update, text)
