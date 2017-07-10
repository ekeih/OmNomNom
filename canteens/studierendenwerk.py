import bs4
import requests
from canteens.canteen import Canteen, VEGGIE, MEAT
from omnomgram.tasks import send_message_to_admin


def __parse_menu(url):
    params = {'resources_id': url}
    headers = {'user-agent': 'User-Agent: Mozilla'}

    def get_menu():
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
                    veggie = item.find_all('img', class_='splIcon')
                    annotation = MEAT
                    for icon in veggie:
                        if 'icons/1.png' in icon.attrs['src'] or 'icons/15.png' in icon.attrs['src']:
                            annotation = VEGGIE
                    title = item.find('span', class_='bold').text.strip()
                    price = item.find('div', class_='text-right').text.strip()
                    text = '%s%s %s: %s\n' % (text, annotation, title, price)
            return text
        else:
            send_message_to_admin.delay('Could not update %s' % url)
            return 'Sorry, leider konnte ich den Speiseplan nicht korrekt abrufen.'

    def get_notes():
        request = requests.post('https://www.stw.berlin/xhr/hinweise.html', data=params, headers=headers)
        if request.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(request.text, 'html.parser')
            return '\n%s' % soup.get_text().strip()

    return '%s%s' % (get_menu(), get_notes())

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
        id_='fu_veggie',
        name='FU Veggie No1',
        update=__parse_menu,
        url=323
    ),
    Canteen(
        id_='fu_2',
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

