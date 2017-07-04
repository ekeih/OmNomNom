# Copyright (C) 2017  Max Rosin
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

import bs4
import requests
from canteens.canteen import Canteen


def __parse_menu(url):
    params = {'resources_id': url}
    headers = {'user-agent': 'User-Agent: Mozilla'}
    request = requests.post('https://www.stw.berlin/xhr/speiseplan-und-standortdaten.html',
                            data=params, headers=headers)
    if request.status_code == requests.codes.ok:
        text = ''
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        menu = soup.find('div', id='speiseplan')
        menu_groups = menu.find_all('div', class_='splGroupWrapper')
        for group in menu_groups:
            menu_items = group.find_all('div', class_='splMeal')
            for item in menu_items:
                title = item.find('span', class_='bold').text.strip()
                price = item.find('div', class_='text-right').text.strip()
                text = '%s%s: %s\n' % (text, title, price)
        return text
    else:
        return 'Sorry, leider konnte ich den Speiseplan nicht korrekt abrufen.'

_canteens = [
    Canteen(
        id_='tu_architektur',
        name='TU Architektur Cafeteria',
        update=__parse_menu,
        url=540
    ),
    Canteen(
        id_='tu_acker',
        name='TU Ackerstraße',
        update=__parse_menu,
        url=539
    ),
    Canteen(
        id_='tu_mar',
        name='TU Marchstraße',
        update=__parse_menu,
        url=538
    ),
    Canteen(
        id_='tu_mensa',
        name='TU Hauptmensa',
        update=__parse_menu,
        url=321
    ),
    Canteen(
        id_='tu_tel',
        name='TU TEL Skyline',
        update=__parse_menu,
        url=657
    ),
    Canteen(
        id_='hu_nord',
        name='HU Nord',
        update=__parse_menu,
        url=147
    ),
    Canteen(
        id_='hu_sued',
        name='HU Süd',
        update=__parse_menu,
        url=367
    ),
    Canteen(
        id_='hu_adlershof',
        name='HU Oase Adlershof',
        update=__parse_menu,
        url=191
    ),
    Canteen(
        id_='hu_spandauer',
        name='HU Spandauer Straße',
        update=__parse_menu,
        url=270
    ),
    Canteen(
        id_='fu_veggie_no_1',
        name='FU Veggie No1',
        update=__parse_menu,
        url=323
    ),
    Canteen(
        id_='fu_mensa_2',
        name='FU Mensa II',
        update=__parse_menu,
        url=322
    ),
    Canteen(
        id_='fu_lankwitz',
        name='FU Mensa Lankwitz',
        update=__parse_menu,
        url=528
    ),
    Canteen(
        id_='fu_dueppel',
        name='FU Düppel',
        update=__parse_menu,
        url=271
    ),
    Canteen(
        id_='fu_koserstrasse',
        name='FU Cafeteria Koserstraße',
        update=__parse_menu,
        url=660
    ),
    Canteen(
        id_='fu_koenigin_luise',
        name='FU Cafeteria Königin-Luise-Str.',
        update=__parse_menu,
        url=542
    ),
    Canteen(
        id_='fu_vant_hoff',
        name='FU Cafeteria V.-Hoff-Str',
        update=__parse_menu,
        url=277
    ),
    Canteen(
        id_='fu_ihnestrasse',
        name='FU Cafeteria Ihnestraße',
        update=__parse_menu,
        url=368
    ),
    Canteen(
        id_='udk_jazz_cafe',
        name='UDK "Jazz Cafe"',
        update=__parse_menu,
        url=722
    )
]

CANTEENS = []
for canteen in _canteens:
    CANTEENS.append(canteen)
