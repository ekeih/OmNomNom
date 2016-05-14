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
from dateparser import parse as parseDate
from logging import getLogger
from telegram import ParseMode
from sys import exc_info
from time import strftime

logger = getLogger()

canteens = matheparser.CANTEENS + singh.CANTEENS + studentenwerk.CANTEENS

def get_canteens():
  return canteens

def _send_message(bot, update, text):
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
  logger.info('Out: %s' % target_chat)
  bot.sendMessage(chat_id=update.message.chat_id, text=text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

class OmNomNom:
  def __init__(self, cache):
    self._cache = cache

  def menu_makantine(self, bot, update, args):
    if args:
      try:
        all_args = ' '.join(args)
        day = parseDate(all_args, settings={'PREFER_DATES_FROM': 'future'})
        formatted_for_matheparser = day.date().strftime("%d.%m.%Y")
        text = matheparser.get_menu(date=formatted_for_matheparser)
        _send_message(bot, update, text)
      except:
        logger.error('Error:\n%s' % exc_info()[0])
        _send_message(bot, update, 'Leider habe ich das Datum nicht verstanden. Bitte gib einen Wochentag an.')
    else:
      _send_message(bot, update, self._cache.read('tu_personalkantine'))

  def menu_marchstrasse(self, bot, update):
    _send_message(bot, update, self._cache.read('tu_marchstrasse'))

  def menu_architektur(self, bot, update):
    _send_message(bot, update, self._cache.read('tu_architektur'))

  def menu_acker(self, bot, update):
    _send_message(bot, update, self._cache.read('tu_ackerstrasse'))

  def menu_mensa(self, bot, update):
    _send_message(bot, update, self._cache.read('tu_mensa'))

  def menu_tel(self, bot, update):
    _send_message(bot, update, self._cache.read('tu_tel'))

  def menu_tu_singh(self, bot, update):
    _send_message(bot, update, self._cache.read('tu_singh'))

# HU Berlin

  def menu_hu_nord(self, bot, update):
    _send_message(bot, update, self._cache.read('hu_nord'))

  def menu_hu_sued(self, bot, update):
    _send_message(bot, update, self._cache.read('hu_sued'))

  def menu_hu_adlershof(self, bot, update):
    _send_message(bot, update, self._cache.read('hu_adlershof'))

  def menu_hu_spandauer(self, bot, update):
    _send_message(bot, update, self._cache.read('hu_spandauer'))

# FU Berlin

  def menu_fu_1(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_veggie_no_1'))

  def menu_fu_2(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_mensa_2'))

  def menu_fu_lankwitz(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_lankwitz'))

  def menu_fu_dueppel(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_dueppel'))

  def menu_fu_cafeteria(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_koserstrasse'))

  def menu_fu_cafe_koenigin_luise(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_koenigin_luise'))

  def menu_fu_cafe_vant_hoff(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_vant_hoff'))

  def menu_fu_cafe_ihne(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_ihnestrasse'))

  def menu_fu_assmanshauser(self, bot, update):
    _send_message(bot, update, self._cache.read('fu_assmanshauser'))

# UDK Berlin
  def menu_udk_jazz_cafe(self, bot, update):
    _send_message(bot, update, self._cache.read('udk_jazz_cafe'))