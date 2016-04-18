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

import matheparser
import time

CANTEENS_DICT = {}

CANTEENS = [
  {
    'id'    : 'arch',
    'title' : 'Architekturgebäude',
    'names' : ['arch', 'architektur', 'a'],
    'type'  : 'studentenwerk',
    'link'  : 'http://www.studentenwerk-berlin.de/mensen/speiseplan/tu_cafe_erp/index.html',
    'feed'  : 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_erp/tag/lang/0000000000000000000000000'
  },
  {
    'id'    : 'singh',
    'title' : 'Singh Cafe',
    'names' : ['singh', 'ma', 'mathe-cafete', 'ma-unten'],
    'type'  : 'nofeed',
    'link'  : 'http://singh-catering.de/cafe',
    'feed'  : False
  },
  {
    'id'    : 'personalkantine',
    'title' : 'Personalkantine',
    'type'  : 'makantine',
    'names' : ['ma-kantine', 'personalkantine', 'ma-oben'],
    'link'  : 'http://personalkantine.personalabteilung.tu-berlin.de/pdf/MA-aktuell.pdf',
    'feed'  : False
  },
  {
    'id'    : 'mar',
    'title' : 'Marchstraße',
    'names' : ['march', 'marchstraße', 'mar'],
    'type'  : 'studentenwerk',
    'link'  : 'http://www.studentenwerk-berlin.de/mensen/speiseplan/tu_marchstr/index.html',
    'feed'  : 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu_marchstr/tag/lang/0000000000000000000000000'
  },
  {
    'id'    : 'mensa',
    'title' : 'Mensa',
    'names' : ['mensa', 'hauptmensa'],
    'type'  : 'studentenwerk',
    'link'  : 'http://www.studentenwerk-berlin.de/mensen/speiseplan/tu/index.html',
    'feed'  : 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu/tag/lang/0000000000000000000000000'
  }
]

class Canteen:
  canteen_id = ''
  title = ''
  names = []
  canteen_type = ''
  link = ''
  feed = ''
  votes = 0
  def __init__(self, canteen):
    self.canteen_id = canteen['id']
    self.title = canteen['title']
    self.names = canteen['names']
    self.canteen_type = canteen['type']
    self.link = canteen['link']
    self.feed = canteen['feed']
  def get_id(self):
    return self.canteen_id
  def get_title(self):
    return self.title
  def get_link(self):
    return self.link
  def get_type(self):
    return self.canteen_type
  def get_feed(self):
    return self.feed
  def get_names(self):
    return self.names

for canteen in CANTEENS:
  CANTEENS_DICT[canteen['id']] = Canteen(canteen)

class OmNomNom:
	def start(bot, update):
		bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
	def menu_listing(bot, update):
		bot.sendMessage(chat_id=update.message.chat_id, text="Guten Hunger")
	def menu_makantine(bot, update):
		text = matheparser.get_menue(time.strftime('%d.%m.%Y'))
		bot.sendMessage(chat_id=update.message.chat_id, text=text)
