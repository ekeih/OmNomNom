import datetime
import re
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from celery.utils.log import get_task_logger

from backend.backend import app, cache, cache_date_format, cache_ttl
from canteens.canteen import get_current_week, get_next_week, VEGGIE, MEAT, FISH

logger = get_task_logger(__name__)
URL = 'https://personalkantine.personalabteilung.tu-berlin.de'


def get_date_range():
    today = datetime.date.today()
    if today.weekday() > 4:
        return get_next_week()
    else:
        return get_current_week()


def get_menu() -> Dict[datetime.datetime, str]:
    menu_str = download_menu()
    soup = BeautifulSoup(menu_str, 'html.parser')

    menus = soup.find_all("ul", class_="Menu__accordion")
    if len(menus) == 0:
        logger.error('Could not find any menu items for EN Kantine')
        raise Exception
    if len(menus) > 1:
        logger.warning('Found more than one menu item for EN Kantine, using the first one')

    return parse_menu(menus[0])


def download_menu() -> str:
    try:
        request = requests.get(URL)
        request.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as ex:
        raise ex
    if request.status_code != requests.codes.ok:
        logger.error('Could not update EN Kantine with status code %s' % request.status_code)
        raise Exception

    return request.text


def parse_menu(menu: Tag) -> Dict[datetime.datetime, str]:
    parsed_menu = {}

    for day in menu.children:
        date_tag = day.find("h2")
        if date_tag == -1:
            continue

        date_str = date_tag.text.split(" ")[1]
        date_time = datetime.datetime.strptime(date_str, '%d.%m.%Y')
        dishlist = day.find("ul")
        if dishlist == -1:
            logger.warn('Could not find any dishes in EN Kantine for %s' % date_str)
            continue

        menu_str = "\n".join(parse_menu_items(dishlist.find_all("li")))
        parsed_menu[date_time] = '[EN Kantine](%s) (%s)\n%s\n\n*Öffnungszeiten*\nMo - Fr: 11 - 15 Uhr' % (URL, date_str, menu_str)

    return parsed_menu


def parse_menu_items(dishes: List[Tag]) -> List[str]:
    parsed_dishes = []

    for dish in dishes:
        dish_text = dish.text.lower()
        if '(v)' in dish_text or 'gemüseplatte' in dish_text:
            annotation = VEGGIE
        elif '(F)' in dish_text:
            annotation = FISH
        else:
            annotation = MEAT

        parsed_dish = format_dish(" ".join(dish.stripped_strings))
        parsed_dishes.append('%s %s' % (annotation, parsed_dish))

    return parsed_dishes or ['Leider kenne ich (noch) keinen Speiseplan für diesen Tag.']


def format_dish(dish: str) -> str:
    dish = dish.strip()

    # remove ingredient hints
    dish = re.sub(r'\([\w\s+]+\)', '', dish)

    # use common price tag design
    dish = re.sub(r'\s+(\d,\d+)\s+€', r': *\g<1>€*', dish)

    return dish


@app.task(bind=True, default_retry_delay=30)
def update_personalkantine(self):
    try:
        logger.info('[Update] TU Personalkantine')
        for day in get_date_range():
            menu = 'Die Personalkantine hat leider bis auf weiteres geschlossen. (https://personalkantine.personalabteilung.tu-berlin.de)'
            cache.hset(day.strftime(cache_date_format), 'tu_personalkantine', menu)
            cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)


@app.task(bind=True, default_retry_delay=30)
def update_en_canteen(self):
    try:
        logger.info('[Update] TU EN Canteen')
        menu = get_menu()
        for day in get_date_range():
            day_menu = menu.get(day)
            if day_menu:
                cache.hset(day.strftime(cache_date_format), 'tu_en_kantine', day_menu)
                cache.expire(day.strftime(cache_date_format), cache_ttl)

    except Exception as ex:
        raise self.retry(exc=ex)
