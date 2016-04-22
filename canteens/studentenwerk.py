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
  },
  {
    'id'    : 'tel',
    'title' : 'Skyline TEL',
    'names' : ['tel', 'skyline'],
    'type'  : 'studentenwerk',
    'link'  : 'http://www.studentenwerk-berlin.de/mensen/speiseplan/tu_cafe_skyline/index.html',
    'feed'  : 'http://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_skyline/tag/lang/0000000000000000000000000'
  }
]

def get_menu(url):
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
