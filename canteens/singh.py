from datetime import datetime

import requests
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from backend.backend import app, cache, cache_date_format, cache_ttl
from canteens.canteen import MEAT, VEGAN, VEGGIE, get_current_week, get_next_week
from omnomgram.tasks import send_message_to_admin

logger = get_task_logger(__name__)
URL = 'http://singh-catering.de/cafe/'


def parse_menu_items(items):
    text = ''
    for item in items.find_all('li', class_='menu-list__item'):
        title = item.find('span', class_='item_title').get_text()
        price = item.find('span', class_='menu-list__item-price').get_text()
        veggie = item.find('span', class_='menu-list__item-highlight-title')
        annotation = MEAT
        if veggie:
            if 'VEGAN!' in veggie:
                annotation = VEGAN
            elif 'VEGETARISCH!' in veggie:
                annotation = VEGGIE
        description = item.find('span', class_='desc__content').get_text()
        text = '%s%s *%s: %s*\n_%s_\n' % (text, annotation, title, price, description)
    return text


def get_menu():
    try:
        request = requests.get(URL)
        request.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as ex:
        send_message_to_admin('```\n%s\n```' % ex)
        raise ex
    if request.status_code == requests.codes.ok:
        soup = BeautifulSoup(request.text, 'html.parser')
        menu_items = soup.find_all('ul', class_='menu-list__items')
        date_range = get_date_range()

        menu = {
            0: '[Singh Catering](%s) (%s) (08:00-18:00)\n%s' % (URL, date_range[0].strftime('%d.%m.%Y'),
                                                                parse_menu_items(menu_items[0])),  # Monday
            1: '[Singh Catering](%s) (%s) (08:00-18:00)\n%s' % (URL, date_range[1].strftime('%d.%m.%Y'),
                                                                parse_menu_items(menu_items[3])),  # Tuesday
            2: '[Singh Catering](%s) (%s) (08:00-18:00)\n%s' % (URL, date_range[2].strftime('%d.%m.%Y'),
                                                                parse_menu_items(menu_items[1])),  # Wednesday
            3: '[Singh Catering](%s) (%s) (08:00-18:00)\n%s' % (URL, date_range[3].strftime('%d.%m.%Y'),
                                                                parse_menu_items(menu_items[4])),  # Thursday
            4: '[Singh Catering](%s) (%s) (08:00-18:00)\n%s' % (URL, date_range[4].strftime('%d.%m.%Y'),
                                                                parse_menu_items(menu_items[2])),  # Friday
        }
        return menu
    else:
        send_message_to_admin('Could not update Singh with status code %s' % request.status_code)
        raise Exception


def get_date_range():
    if datetime.now().weekday() > 4:
        return get_next_week()
    else:
        return get_current_week()


@app.task(bind=True, default_retry_delay=30, max_retries=20)
def update_singh(self):
    try:
        logger.info('[Update] TU Singh')
        menu = get_menu()
        for day in get_date_range():
            day_menu = menu.get(day.weekday())
            if day_menu:
                cache.hset(day.strftime(cache_date_format), 'tu_singh', day_menu)
                cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)


if __name__ == '__main__':
    print(get_menu())
