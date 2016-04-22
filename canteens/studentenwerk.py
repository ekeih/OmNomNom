#    Copyright (C) 2016  Max Rosin git@hackrid.de
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

import feedparser
from bs4 import BeautifulSoup

CANTEEN_A     = 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_erp/tag/lang/0000000000000000000000000'
CANTEEN_MAR   = 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu_marchstr/tag/lang/0000000000000000000000000'
CANTEEN_MENSA = 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu/tag/lang/0000000000000000000000000'
CANTEEN_TEL   = 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_skyline/tag/lang/0000000000000000000000000'

def menu_a():
  return __parse_menu(CANTEEN_A)

def menu_mar():
  return __parse_menu(CANTEEN_MAR)

def menu_mensa():
  return __parse_menu(CANTEEN_MENSA)

def menu_tel():
  return __parse_menu(CANTEEN_TEL)

def __parse_menu(url):
  feed = feedparser.parse(url)
  summary = feed['entries'][0]['summary_detail']['value']
  soup = BeautifulSoup(summary, "html.parser")
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
