import datetime
import re
import urllib.request


from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from backend.backend import app, cache, cache_date_format, cache_ttl
from canteens.canteen import VEGGIE, MEAT, get_next_week, get_current_week

import emoji
WELLBALANCEDMEAL = emoji.emojize(':green_apple:')

logger = get_task_logger(__name__)

URL = 'https://www.bsr.de/bsr/speiseplan/internet_speiseplan.html'


def get_website():
    return urllib.request.urlopen(URL).read()


def main(date):
    dishes = []

    menus = BeautifulSoup(get_website(), 'html5lib').find_all('table', class_='Liste') #Note: Only html5lib can fix this broken html code.
    days  = BeautifulSoup(get_website(), 'html5lib').find_all('div', class_='KopfLeiste_o')

    if len(menus) != len(days): return ['Leider verstehe ich den Speiseplan heute nicht.']

    date = date.replace(datetime.datetime.now().strftime('%d.%m.%Y'), 'Heute')
    date = date.replace((datetime.date.today()+datetime.timedelta(days=1)).strftime('%d.%m.%Y'), 'Morgen')

    for day in days:
        m = menus.pop(0)
        if date in day.find('div').string:
            for dish in m.find_all('tr'):
                if dish.find(class_='Speise'):

                    title = dish.find('td', class_='Speise').text.strip()
                    price = dish.find('td', class_='PreisG').text.strip()

#                    annotation = dish.find('td', class_='Nr').text.strip()
                    annotation = MEAT #default
                    #is it a well-balanced meal and recommended for healthy eating?
                    if str(dish.find('td', class_='PreisG')).find("apfel-klein.png") != -1 :
                        annotation = "%s%s" % (annotation, WELLBALANCEDMEAL)

                    this_dish = '%s %s: *%s*' % (annotation, title, price)
                    dishes.append(this_dish)

    return beautify_menu(dishes) or ['Leider kenne ich keinen Speiseplan für diesen Tag.']


def beautify_menu(menu):
    # remove empty lines
    menu = [menu_e for menu_e in menu if menu_e.strip() ]

    # every day "Süßspeise des Tages" is announced. quite annoying.
    menu = [menu_e for menu_e in menu if menu_e.find("Süßspeise des Tages") == -1 ]

    # remove symbols for special ingredients
    sym_regex = re.compile(r'\([\w,]+\) *') #matches:"(A)","(1)","(1,2)","(1)foo" and "(1) foo"
    menu = [sym_regex.sub("", menu_e) for menu_e in menu ]

    return menu


def get_menu(date=False):
    requested_date = date or datetime.date.today().strftime('%d.%m.%Y')
    dishes = main(requested_date)
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
def update_bsr(self):
    try:
        logger.info('[Update] BSR Canteen')
        for day in get_date_range():
            day_website = day.strftime('%d.%m.%Y')
            menu = get_menu(date=day_website)
            if menu:
                menu = '[BSR Kantine](%s) (%s)\n\n*Speiseplan*\n%s\n\n*Öffnungszeiten*\nMo - Fr: 05:45 - 14 Uhr' % (URL, day_website, menu)
                cache.hset(day.strftime(cache_date_format), 'bsr', menu)
                cache.expire(day.strftime(cache_date_format), cache_ttl)
    except Exception as ex:
        raise self.retry(exc=ex)


if __name__ == "__main__":
    for day in get_date_range():
        day_website = day.strftime('%d.%m.%Y')
        menu = get_menu(date=day_website)
        print(menu)
