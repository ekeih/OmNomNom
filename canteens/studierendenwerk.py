import bs4
import datetime
import fake_useragent
import re
import requests
from canteens.canteen import FISH, MEAT, VEGAN, VEGGIE
from omnomgram.tasks import send_message_to_admin
from backend.backend import app, cache, cache_interval
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def __parse_menu(id_):
    today = datetime.date.today()
    today_api = today.strftime('%Y-%m-%d')
    today_human = today.strftime('%d.%m.%Y')
    useragent = fake_useragent.UserAgent(fallback='Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0')
    params = {'resources_id': id_, 'date': today_api}
    headers = {'user-agent': useragent.random}

    def get_menu():
        request = requests.post('https://www.stw.berlin/xhr/speiseplan-wochentag.html', data=params, headers=headers)
        if request.status_code == requests.codes.ok:
            text = ''
            soup = bs4.BeautifulSoup(request.text, 'html.parser')
            menu_groups = soup.find_all('div', class_='splGroupWrapper')
            for group in menu_groups:
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
                    text = '%s%s %s: %s\n' % (text, annotation, title, price)
            if text.strip() == '':
                return text.strip()
            else:
                lines = text.split('\n')
                lines.sort()
                text = '\n'.join(lines)
                return '*Speiseplan*%s' % text
        else:
            send_message_to_admin.delay('Could not update %s with status code %s.'\
                                        % (mapping[id_]['name'], request.status_code))
            return ''

    def get_notes():
        notes = ''
        request = requests.post('https://www.stw.berlin/xhr/hinweise.html', data=params, headers=headers)
        if request.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(request.text, 'html.parser')
            soup.find('article', {'data-hid': '6046-1'}).decompose()
            notes = soup.get_text().strip()
        if notes == '':
            return ''
        else:
            return '*Hinweise*\n%s' % notes

    def get_business_hours():
        business_hours = ''
        request = requests.post('https://www.stw.berlin/xhr/speiseplan-und-standortdaten.html', data=params, headers=headers)
        if request.status_code == requests.codes.ok:
            soup = bs4.BeautifulSoup(request.text, 'html.parser')
            time = soup.find(class_='glyphicon-time')
            transfer = soup.find(class_='glyphicon-transfer')
            education = soup.find(class_='glyphicon-education')

            if time:
                business_hours += '\n*Öffnungszeiten*'
                for sib in time.parent.parent.next_siblings:
                    if type(sib) == bs4.Tag and transfer not in sib.descendants and education not in sib.descendants:
                        for item in sib.find_all('div', class_='col-xs-10'):
                            for string in item.stripped_strings:
                                business_hours += '\n%s' % string
        return business_hours.strip()

    result = '*%s* (%s)\n\n%s\n\n%s\n\n%s' % (mapping[id_]['name'], today_human, get_menu(), get_business_hours(), get_notes())
    return re.sub(r'\n\s*\n', '\n\n', result)

mapping = {
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
    631: {"name": "Cafeteria TU Hardenbergstraße", "command": "tu_mensa_cafeteria"},
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


@app.task(bind=True, default_retry_delay=30)
def update_all_studierendenwerk_canteens(self):
    for id_, canteen in mapping.items():
        update_studierendenwerk.delay(id_)


@app.task(bind=True, rate_limit='10/m', default_retry_delay=30)
def update_studierendenwerk(self, id_):
    try:
        logger.info('[Update] %s' % mapping[id_]['name'])
        menu = __parse_menu(id_)
        if menu.strip() == '':
            logger.info('No menu for %s' % mapping[id_]['name'])
            send_message_to_admin('No menu for %s' % mapping[id_]['name'])
        else:
            logger.info('Caching %s' % mapping[id_]['name'])
            cache.set(mapping[id_]['command'], menu, ex=cache_interval * 4)
    except Exception as ex:
        raise self.retry(exc=ex)
