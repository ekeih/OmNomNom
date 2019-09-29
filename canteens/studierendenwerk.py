import datetime
import re
import time

import bs4
import requests
from celery.utils.log import get_task_logger

from backend.backend import app, cache, cache_date_format, cache_ttl
from canteens.canteen import get_current_week, get_next_week, get_useragent, FISH, MEAT, VEGAN, VEGGIE

logger = get_task_logger(__name__)

DATE_FORMAT_API = '%Y-%m-%d'
CANTEENS = {
    534: {"name": "Mensa ASH Berlin Hellersdorf", "command": "ash_hellersdorf"},
    535: {"name": "Mensa Beuth Hochschule für Technik Kurfürstenstraße", "command": "beuth_kurfuerstenstr"},
    527: {"name": "Mensa Beuth Hochschule für Technik Luxemburger Straße", "command": "beuth_luxembugerstr"},
    537: {"name": "Mensa Charité Zahnklinik", "command": "charite_zahnklinik"},
    529: {"name": "Mensa EHB Teltower Damm", "command": "ehb_teltower_damm"},
    271: {"name": "Mensa FU Herrenhaus Düppel", "command": "fu_dueppel"},
    322: {"name": "Mensa FU II Otto-von-Simson-Straße", "command": "fu_2"},
    528: {"name": "Mensa FU Lankwitz Malteserstraße", "command": "fu_lankwitz"},
    531: {"name": "Mensa HfM Charlottenstraße", "command": "hfm_charlottenstr"},
    533: {"name": "Mensa HfS Schnellerstraße", "command": "hfs_schnellerstr"},
    320: {"name": "Mensa HTW Treskowallee", "command": "htw_treskowallee"},
    319: {"name": "Mensa HTW Wilhelminenhof", "command": "htw_wilhelminenhof"},
    147: {"name": "Mensa HU Nord", "command": "hu_nord"},
    191: {"name": "Mensa HU Oase Adlershof", "command": "hu_adlershof"},
    367: {"name": "Mensa HU Süd", "command": "hu_sued"},
    270: {"name": "Mensa HU Spandauer Straße", "command": "hu_spandauer"},
    526: {"name": "Mensa HWR Badensche Straße", "command": "hwr_badenschestr"},
    532: {"name": "Mensa Katholische HS für Sozialwesen", "command": "khs_mensa"},
    530: {"name": "Mensa KHS Weißensee", "command": "khs_weissensee"},
    321: {"name": "Mensa TU Hardenbergstraße", "command": "tu_mensa"},
    631: {"name": "Mensa TU Veggie 2.0", "command": "tu_veggie"},
    323: {"name": "Mensa Veggie N° 1 - Die grüne Mensa", "command": "fu_veggie"},
    368: {"name": "Cafeteria FU Ihnestraße", "command": "fu_ihnestr"},
    660: {"name": "Cafeteria FU Koserstraße", "command": "fu_koserstr"},
    542: {"name": "Cafeteria FU Pharmazie", "command": "fu_pharmazie"},
    277: {"name": "Cafeteria FU Rechtswissenschaft", "command": "fu_rechtswissenschaft"},
    543: {"name": "Cafeteria FU Wirtschaftswissenschaften", "command": "fu_wirtschaftswissenschaften"},
    726: {"name": "Cafeteria HTW Treskowallee", "command": "htw_treskowallee_cafeteria"},
    659: {"name": "Cafeteria HU „Jacob und Wilhelm Grimm Zentrum“", "command": "hu_wilhelm_grimm_zentrum"},
    539: {"name": "Cafeteria TU Ackerstraße", "command": "tu_ackerstr"},
    540: {"name": "Cafeteria TU Architektur", "command": "tu_architektur"},
    657: {"name": "Cafeteria TU „Skyline“", "command": "tu_skyline"},
    541: {"name": "Cafeteria TU Hauptgebäude „Wetterleuchten“", "command": "tu_wetterleuchten"},
    538: {"name": "Cafeteria TU Marchstraße", "command": "tu_marchstr"},
    722: {"name": "Cafeteria UdK „Jazz-Cafe“", "command": "udk_jazz_cafe"},
    658: {"name": "Cafeteria UdK Lietzenburger Straße", "command": "udk_lietzenburgerstr"},
    647: {"name": "Coffeebar Beuth Hochschule", "command": "beuth_coffeebar"},
    648: {"name": "Coffeebar Beuth Hochschule Haus Grashof", "command": "beuth_coffeebar_haus_grashof"},
    1407: {"name": "Coffeebar EHB Teltower Damm", "command": "ehb_teltower_damm_coffeebar"},
    723: {"name": "Coffeebar HfM „Neuer Marstall“", "command": "hfm_neuer_marstall"},
    724: {"name": "Coffeebar HfM Charlottenstraße", "command": "hfm_charlottenstr_coffeebar"},
    725: {"name": "Coffeebar HTW Wilhelminenhof", "command": "htw_wilhelminenhof_coffeebar"},
    661: {"name": "Coffeebar HU „c.t“", "command": "hu_ct"},
    721: {"name": "Coffeebar HU Mensa Nord", "command": "hu_nord_coffeebar"},
    720: {"name": "Coffeebar HU Oase Adlershof", "command": "hu_adlershof_coffeebar"},
    727: {"name": "Coffeebar HWR Alt-Friedrichsfelde", "command": "hwr_alt_friedrichsfelde"},
    728: {"name": "Coffeebar HWR Badensche Straße", "command": "hwr_badenschestr_coffeebar"},
    649: {"name": "Coffeebar Mensa FU II", "command": "fu_2_coffeebar"},
    650: {"name": "Coffeebar Mensa Lankwitz", "command": "fu_lankwitz_coffeebar"},
    632: {"name": "Coffeebar TU Hardenbergstraße", "command": "tu_mensa_coffeebar"},
}


def download_menu(canteen_id, date):
    url = 'https://www.stw.berlin/xhr/speiseplan-wochentag.html'
    params = {'resources_id': canteen_id, 'date': date}
    headers = {'user-agent': get_useragent()}
    request = requests.post(url, data=params, headers=headers)
    request.raise_for_status()
    return request.text


def download_notes(canteen_id):
    url = 'https://www.stw.berlin/xhr/hinweise.html'
    params = {'resources_id': canteen_id, 'date': datetime.date.today().strftime(DATE_FORMAT_API)}
    headers = {'user-agent': get_useragent()}
    request = requests.post(url, data=params, headers=headers)
    request.raise_for_status()
    return request.text


def download_business_hours(canteen_id):
    url = 'https://www.stw.berlin/xhr/speiseplan-und-standortdaten.html'
    params = {'resources_id': canteen_id, 'date': datetime.date.today().strftime(DATE_FORMAT_API)}
    headers = {'user-agent': get_useragent()}
    request = requests.post(url, data=params, headers=headers)
    request.raise_for_status()
    return request.text


def parse_menu(menu_html):
    text = ''
    soup = bs4.BeautifulSoup(menu_html, 'html.parser')
    menu_groups = soup.find_all('div', class_='splGroupWrapper')
    for group in menu_groups:
        group_lines = []
        menu_items = group.find_all('div', class_='splMeal')
        for item in menu_items:
            veggie = item.find_all('img', class_='splIcon')
            annotation = None
            for icon in veggie:
                if 'icons/15.png' in icon.attrs['src']:
                    annotation = VEGAN
                elif 'icons/1.png' in icon.attrs['src']:
                    annotation = VEGGIE
                elif 'icons/38.png' in icon.attrs['src']:
                    annotation = FISH
            if annotation is None:
                annotation = MEAT
            title = item.find('span', class_='bold').text.strip()
            price = item.find('div', class_='text-right').text.strip()
            price_exp = re.compile(r'€ (\d,\d+).*$')
            price = price_exp.sub('*\g<1>€*', price)
            group_lines.append('%s %s: %s' % (annotation, title, price))

        if len(group_lines) > 0:
            group_heading = group.find('div').find('div').text.strip()
            group_text = '\n'.join(sorted(group_lines)).strip()
            text += '\n*%s*\n%s\n' % (group_heading, group_text)
    return text.strip()


def parse_notes(notes_html):
    soup = bs4.BeautifulSoup(notes_html, 'html.parser')
    bookmarking_note = soup.find('article', {'data-hid': '6046-1'})
    if bookmarking_note:
        bookmarking_note.decompose()
    popup_note = soup.find(text=re.compile('Diese Anzeige wird'))
    if popup_note:
        popup_note.parent.decompose()
    notes = soup.get_text().strip()
    if notes == '':
        return ''
    else:
        return '*Hinweise*\n%s' % notes


def parse_business_hours(business_hours_html):
    business_hours = ''
    soup = bs4.BeautifulSoup(business_hours_html, 'html.parser')
    time_icon = soup.find(class_='glyphicon-time')
    transfer_icon = soup.find(class_='glyphicon-transfer')
    education_icon = soup.find(class_='glyphicon-education')

    if time_icon:
        business_hours += '\n*Öffnungszeiten*'
        for sib in time_icon.parent.parent.next_siblings:
            if type(sib) == bs4.Tag and transfer_icon not in sib.descendants and education_icon not in sib.descendants:
                for item in sib.find_all('div', class_='col-xs-10'):
                    for string in item.stripped_strings:
                        business_hours += '\n%s' % string
    return business_hours.strip()


def get_full_text(canteen_id, canteen_business_hours, canteen_notes, date=None):
    day = date or datetime.date.today()
    date_api = day.strftime(DATE_FORMAT_API)
    date_human = day.strftime('%d.%m.%Y')

    menu_html = download_menu(canteen_id, date_api)
    menu = parse_menu(menu_html)

    result = '*%s* (%s)\n\n%s\n\n%s\n\n%s' % (CANTEENS[canteen_id]['name'], date_human, menu, canteen_business_hours,
                                              canteen_notes)
    return re.sub(r'\n\s*\n', '\n\n', result)


def get_date_range():
    return get_current_week() + get_next_week()


@app.task()
def update_all_studierendenwerk_canteens():
    for canteen_id, canteen in CANTEENS.items():
        update_studierendenwerk.delay(canteen_id)


@app.task(bind=True, rate_limit='60/m', default_retry_delay=30, max_retries=20)
def update_studierendenwerk_by_date(self, canteen_id, date, business_hours, notes):
    try:
        day = datetime.datetime.strptime(date, DATE_FORMAT_API)
        logger.info('[Update] %s (%s)' % (CANTEENS[canteen_id]['name'], date))
        menu = get_full_text(canteen_id, business_hours, notes, date=day)
        if menu.strip() == '':
            logger.info('No menu for %s (%s)' % (CANTEENS[canteen_id]['name'], date))
            raise self.retry()
        else:
            logger.info('Caching %s (%s)' % (CANTEENS[canteen_id]['name'], date))
            cache.hset(day.strftime(cache_date_format), CANTEENS[canteen_id]['command'], menu)
            cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)


@app.task(bind=True, default_retry_delay=30, max_retries=20)
def update_studierendenwerk(self, canteen_id):
    try:
        logger.info('[Update] %s' % CANTEENS[canteen_id]['name'])
        notes = parse_notes(download_notes(canteen_id))
        time.sleep(0.5)
        business_hours = parse_business_hours(download_business_hours(canteen_id))
        time.sleep(0.5)
        for day in get_date_range():
            update_studierendenwerk_by_date.delay(canteen_id, day.strftime(cache_date_format), business_hours, notes)
    except Exception as ex:
        raise self.retry(exc=ex)
