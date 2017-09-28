import datetime
import re
import urllib.request

from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from backend.backend import app, cache, cache_date_format, cache_ttl
from canteens.canteen import VEGGIE, MEAT, get_next_week, get_current_week

EMPLOYEE_CANTEEN = 0
EN_CANTEEN = 1

logger = get_task_logger(__name__)

URL = 'http://personalkantine.personalabteilung.tu-berlin.de/#speisekarte'


def get_website():
    return urllib.request.urlopen(URL).read()


def main(date, canteen=EMPLOYEE_CANTEEN):
    dishes = []
    html = get_website()
    menus = BeautifulSoup(html, 'html.parser').find_all('ul', class_='Menu__accordion')

    for day in menus[canteen].children:
        if day.name and date.lstrip('0') in day.find('h2').string:
            for dishlist in day.children:
                if dishlist.name == 'ul':
                    items = dishlist.find_all('li')
                    for dish in items:
                        if '(v)' in dish.text or '(V)' in dish.text or 'Gemüseplatte' in dish.text:
                            annotation = VEGGIE
                        else:
                            annotation = MEAT
                        this_dish = ''
                        for string in dish.stripped_strings:
                            this_dish = '%s %s' % (this_dish, string)
                        this_dish = '%s %s' % (annotation, _format(this_dish))
                        dishes.append(this_dish)

    return dishes or ['Leider kenne ich (noch) keinen Speiseplan für diesen Tag.']


def _format(line):
    line = line.strip()

    # remove indregend hints
    exp = re.compile('\([\w\s+]+\)')
    line = exp.sub('', line)

    # use common price tag design
    exp = re.compile('\s+(\d,\d+)\s+€')
    line = exp.sub(': *\g<1>€*', line)

    return line


def get_menu(date=False, canteen=EMPLOYEE_CANTEEN):
    requested_date = date or datetime.date.today().strftime('%d.%m.%Y')
    dishes = main(requested_date, canteen)
    menu = ''
    for dish in dishes:
        menu = '%s%s\n' % (menu, dish)
    menu = menu.rstrip()
    return menu


def get_date_range():
    today = datetime.date.today()
    if today.weekday() > 4:
        return get_next_week()
    else:
        return get_current_week()


@app.task(bind=True, default_retry_delay=30)
def update_personalkantine(self):
    try:
        logger.info('[Update] TU Personalkantine')
        for day in get_date_range():
            day_website = day.strftime('%d.%m.%Y')
            menu = get_menu(date=day_website, canteen=EMPLOYEE_CANTEEN)
            if menu:
                menu = '[Personalkantine](%s) (%s) (11:00-16:00)\n%s' % (URL, day_website, menu)
                cache.hset(day.strftime(cache_date_format), 'tu_personalkantine', menu)
                cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)


@app.task(bind=True, default_retry_delay=30)
def update_en_canteen(self):
    try:
        logger.info('[Update] TU EN Canteen')
        for day in get_date_range():
            day_website = day.strftime('%d.%m.%Y')
            menu = get_menu(date=day_website, canteen=EN_CANTEEN)
            if menu:
                menu = '[EN Kantine](%s) (%s)\n%s\n\n*Öffnungszeiten*\nMo - Do: 07 - 17 Uhr\nFr: 07 - 16 Uhr' \
                       % (URL, day_website, menu)
                cache.hset(day.strftime(cache_date_format), 'tu_en_kantine', menu)
                cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)
