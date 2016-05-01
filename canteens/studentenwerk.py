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

import feedparser
from bs4 import BeautifulSoup

CANTEEN_A     = 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_erp/tag/lang/0000000000000000000000000'
CANTEEN_ACKER = 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_ackerstr/tag/lang/0000000000000000000000000'
CANTEEN_MAR   = 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_marchstr/tag/lang/0000000000000000000000000'
CANTEEN_MENSA = 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu/tag/lang/0000000000000000000000000'
CANTEEN_TEL   = 'https://www.studentenwerk-berlin.de/speiseplan/rss/tu_cafe_skyline/tag/lang/0000000000000000000000000'

HU_NORD = 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_nord/tag/lang/0000000000000000000000000'
HU_SUED = 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_sued/tag/lang/0000000000000000000000000'
HU_ADLERSHOF = 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_adlershof/tag/lang/0000000000000000000000000'
HU_SPANDAUER = 'https://www.studentenwerk-berlin.de/speiseplan/rss/hu_spandauer/tag/lang/0000000000000000000000000'

FU_1 = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu1/tag/lang/0000000000000000000000000'
FU_2 = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu2/tag/lang/0000000000000000000000000'
FU_LANKWITZ = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_lankwitz/tag/lang/0000000000000000000000000'
FU_ASSMANNSHAUSER = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_assmannshauser/tag/lang/0000000000000000000000000'
FU_DUEPPEL = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_dueppel/tag/lang/0000000000000000000000000'
FU_CAFETERIA = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafeteria/tag/lang/0000000000000000000000000'
FU_CAFE_KOENIGIN_LUISE = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafe_koenigin_luise/tag/lang/0000000000000000000000000'
FU_CAFE_VANT_HOFF = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafe_vant_hoff/tag/lang/0000000000000000000000000'
FU_CAFE_IHNE = 'https://www.studentenwerk-berlin.de/speiseplan/rss/fu_cafe_ihne/tag/lang/0000000000000000000000000'

def menu_a():
  return __parse_menu(CANTEEN_A)

def menu_acker():
  return __parse_menu(CANTEEN_ACKER)

def menu_mar():
  return __parse_menu(CANTEEN_MAR)

def menu_mensa():
  return __parse_menu(CANTEEN_MENSA)

def menu_tel():
  return __parse_menu(CANTEEN_TEL)

# HU Berlin

def menu_hu_nord():
  return __parse_menu(HU_NORD)

def menu_hu_sued():
  return __parse_menu(HU_SUED)

def menu_hu_adlershof():
  return __parse_menu(HU_ADLERSHOF)

def menu_hu_spandauer():
  return __parse_menu(HU_SPANDAUER)

# FU Berlin

def menu_fu_1():
  return __parse_menu(FU_1)

def menu_fu_2():
  return __parse_menu(FU_2)

def menu_fu_lankwitz():
  return __parse_menu(FU_LANKWITZ)

def menu_fu_assmannshauser():
  return __parse_menu(FU_ASSMANNSHAUSER)

def menu_fu_dueppel():
  return __parse_menu(FU_DUEPPEL)

def menu_fu_cafeteria():
  return __parse_menu(FU_CAFETERIA)

def menu_fu_cafe_koenigin_luise():
  return __parse_menu(FU_CAFE_KOENIGIN_LUISE)

def menu_fu_cafe_vant_hoff():
  return __parse_menu(FU_CAFE_VANT_HOFF)

def menu_fu_cafe_ihne():
  return __parse_menu(FU_CAFE_IHNE)

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
      name = name.get_text().replace('21a', '')
      name = name.strip().rstrip('1234567890').strip()
      price = row.find('td', attrs={'class':"mensa_day_speise_preis"})
      price = price.get_text().split('/')[0].strip('EUR ')
      text = text + name+ ': ' + price + '€\n'
  return text
