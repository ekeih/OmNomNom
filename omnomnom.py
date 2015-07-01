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
import urllib.parse
import json
import feedparser
import sys
from bs4 import BeautifulSoup
import matheparser
import time

API_URL_BASE = 'https://api.telegram.org/bot'
API_URL = API_URL_BASE + config.AUTH_TOKEN
MENSA_DIC = {}

MENSA = [
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

class Mensa:
  mensa_id = ''
  title = ''
  names = []
  mensa_type = ''
  link = ''
  feed = ''
  votes = 0
  def __init__(self,mensa):
    self.mensa_id = mensa['id']
    self.title = mensa['title']
    self.names = mensa['names']
    self.mensa_type = mensa['type']
    self.link = mensa['link']
    self.feed = mensa['feed']
  def get_id(self):
    return self.mensa_id
  def get_title(self):
    return self.title
  def get_link(self):
    return self.link
  def get_type(self):
    return self.mensa_type
  def get_feed(self):
    return self.feed
  def get_names(self):
    return self.names

def api(function, values={}):
  data = urllib.parse.urlencode(values)
  data = data.encode('utf-8')
  req = urllib.request.Request(API_URL + '/' + function, data)
  response = urllib.request.urlopen(req)
  response = response.read()
  result = json.loads(response.decode('utf-8'))
  if result['ok'] == True:
    return result['result']
  else:
    print('API Error')
    return False

def get_help():
  help_text = '''/help - Hilfe
/speisepläne - Links zu allen Speiseplänen

=== Verfügbare Mensen ===
'''
  for key, mensa in MENSA_DIC.items():
    help_text = help_text + '/' + mensa.get_id() + ' - ' + mensa.get_title() + '\n'
  return help_text

def get_menu_studentenwerk(url):
  feed = feedparser.parse(url)
  summary = feed['entries'][0]['summary_detail']['value']
  soup = BeautifulSoup(summary)
  text = ""
  tables = soup.find_all('table', attrs={'class':"mensa_day_speise"})
  for table in tables:
    rows = table.find_all('tr', attrs={'class':"mensa_day_speise_row"})
    for row in rows:
      name = row.find('td', attrs={'class':"mensa_day_speise_name"})
      name = name.get_text().strip().rstrip('1234567890').strip()
      price = row.find('td', attrs={'class':"mensa_day_speise_preis"})
      price = price.get_text().split('/')[0].strip('EUR ')
      text = text + name+ ': ' + price + '€\n'
  return text

def get_menu_makantine():
  text = matheparser.get_menue(time.strftime('%d.%m.%y'))
  return text

def get_menu(mensa_id):
  mensa = MENSA_DIC[mensa_id]
  if mensa.get_type() == 'studentenwerk':
    menu = get_menu_studentenwerk(mensa.get_feed())
  elif mensa.get_type() == 'makantine':
    menu = get_menu_makantine()
  else:
    menu = 'Dieser Speiseplan ist in deinem Land nicht verfügbar.\n' + mensa.get_link()
  return menu

def parse_message(message):
  chat_id = False
  if 'chat' in message:
    chat = message['chat']
    if 'title' in chat:
      print('Group: ' + chat['title'])
    elif 'first_name' in chat:
      print('User: ' + chat['first_name'])
    chat_id = chat['id']
  if 'text' in message:
    print(message['text'])
    action,data = parse_text(message['text'].replace(config.BOT_USERNAME,'').strip())
    if action and data:
      data['chat_id'] = chat_id
      api(action,data)

def parse_text(text):
  response = False
  text = text.lower()
  if text in ['/help', '/h', '/hilfe']:
    response = get_help()
  elif text in ['/speiseplan', '/speisepläne']:
    response = ''
    for key, mensa in MENSA_DIC.items():
      response = response + mensa.get_title() + ': ' + mensa.get_link() + '\n'
  else:
    for key, mensa in MENSA_DIC.items():
      if text.strip('/') in mensa.get_names():
        response = get_menu(key)
  if response:
    data = { 'text' : response }
    return 'sendMessage',data
  else:
    return False, False

if __name__ == '__main__':
  for mensa in MENSA:
    MENSA_DIC[mensa['id']] = Mensa(mensa)
  message_offset = 0
  while True:
    try:
      data = { 'offset' : message_offset }
      updates = api('getUpdates', data)
      if (updates != False):
        for update in updates:
          parse_message(update['message'])
          message_offset = update['update_id'] + 1
    except KeyboardInterrupt:
      print('Bye!')
      sys.exit(0)
    except:
      print('Error in main loop')
