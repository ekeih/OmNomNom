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

import datetime
import re
import urllib.request
from bs4 import BeautifulSoup
from canteens.canteen import Canteen
from telegram import Emoji

URL = 'http://personalkantine.personalabteilung.tu-berlin.de/#speisekarte'

def main(date):
  dishes = []
  html = urllib.request.urlopen(URL).read()
  menu = BeautifulSoup(html, 'html.parser').find('ul', class_='Menu__accordion')

  for day in menu.children:
    if day.name and date in day.find('h2').string:
      for dishlist in day.children:
        if dishlist.name == 'ul':
          items = dishlist.find_all('li')
          for counter,dish in enumerate(items):
            if counter >= len(items)-2:
              annotation = Emoji.EAR_OF_MAIZE
            else:
              annotation = Emoji.POULTRY_LEG
            this_dish = ''
            for string in dish.stripped_strings:
              this_dish = '%s %s' % (this_dish, string)
            this_dish = '%s %s' % (annotation, _format(this_dish))
            dishes.append( this_dish )

  return dishes or ['Heute geschlossen.']

def _format(line):
  line = line.strip()

  # remove indregend hints
  exp = re.compile('\([\w\s+]+\)')
  line = exp.sub('', line)

  # use common price tag design
  exp = re.compile('\s+(\d,\d+)\s+€')
  line = exp.sub(': *\g<1>€*', line)

  return line

def get_menu(url='', date = datetime.date.today().strftime('%d.%m.%Y')):
  dishes = main(date)
  menu = ''
  for dish in dishes:
    menu = '%s%s\n' % (menu, dish)
  menu = menu.rstrip()
  menu = '[Personalkantine](%s) (11:00 - 16:00)\n%s' % (URL, menu)
  return menu

personalkantine = {
  'id_': 'tu_personalkantine',
  'name': 'Personalkantine',
  'url': 'http://personalkantine.personalabteilung.tu-berlin.de/#speisekarte',
  'update': get_menu
}

CANTEENS = [Canteen(personalkantine)]
