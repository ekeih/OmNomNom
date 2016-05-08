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
import feedparser
from bs4 import BeautifulSoup
from canteens.canteen import Canteen
from telegram import Emoji

def __parse_menu(url, date=datetime.date.today().strftime('%d.%m.%Y')):
  feed = feedparser.parse(url)
  summary = feed['entries'][0]['summary_detail']['value']
  soup = BeautifulSoup(summary, "html.parser")
  text = ""
  tables = soup.find_all('table', attrs={'class':"mensa_day_speise"})
  for table in tables:
    rows = table.find_all('tr', attrs={'class':"mensa_day_speise_row"})
    for row in rows:
      name = row.find('td', attrs={'class':"mensa_day_speise_name"})
      name = name.get_text().replace('21a', '')
      name = name.replace('6a', '')
      name = name.replace('6b', '')
      name = name.strip().rstrip('1234567890').strip()
      price = row.find('td', attrs={'class':"mensa_day_speise_preis"})
      price = price.get_text().split('/')[0].strip('EUR ')
      veggie = row.find_all('a', href='#vegetarisch_siegel')
      vegan = row.find_all('a', href='#vegan_siegel')
      annotation = ''
      if veggie or vegan:
        annotation = Emoji.EAR_OF_MAIZE
      else:
        annotation = Emoji.POULTRY_LEG
      text = '%s%s %s: *%s€*\n' % (text, annotation, name, price)
  if text == '':
    text = 'Leider keine Mahlzeiten gefunden. Bitte schau manuell beim [Studentenwerk](http://www.studentenwerk-berlin.de/mensen/speiseplan/index.html) nach.'
  return text

_canteens = [
  {
    'id_': 'tu_architektur',
    'name': 'TU Architektur Cafeteria',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_erp/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'tu_ackerstrasse',
    'name': 'TU Ackerstraße',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_ackerstr/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'tu_marchstrasse',
    'name': 'TU Marchstraße',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_marchstr/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'tu_mensa',
    'name': 'TU Hauptmensa',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'tu_tel',
    'name': 'TU TEL Skyline',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_skyline/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'hu_nord',
    'name': 'HU Nord',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_nord/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'hu_sued',
    'name': 'HU Süd',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_sued/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'hu_adlershof',
    'name': 'HU Oase Adlershof',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_adlershof/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'hu_spandauer',
    'name': 'HU Spandauer Straße',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_spandauer/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_veggie_no_1',
    'name': 'FU Veggie No1',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu1/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_mensa_2',
    'name': 'FU Mensa II',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu2/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_lankwitz',
    'name': 'FU Mensa Lankwitz',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_lankwitz/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_dueppel',
    'name': 'FU Düppel',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_dueppel/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_koserstrasse',
    'name': 'FU Cafeteria Koserstraße',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafeteria/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_koenigin_luise',
    'name': 'FU Cafeteria Königin-Luise-Str.',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafe_koenigin_luise/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_vant_hoff',
    'name': 'FU Cafeteria V.-Hoff-Str',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafe_vant_hoff/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'fu_ihnestrasse',
    'name': 'FU Cafeteria Ihnestraße',
    'url': 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafe_ihne/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  },
  {
    'id_': 'udk_jazz_cafe',
    'name': 'UDK "Jazz Cafe"',
    'url': 'http://www.studentenwerk-berlin.de/speiseplan/rss/udk_jazzcafe/tag/lang/0000000000000000000000000',
    'update': __parse_menu
  }
]

CANTEENS = []
for canteen in _canteens:
  CANTEENS.append(Canteen(canteen))
