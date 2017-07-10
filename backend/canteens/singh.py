from bs4 import BeautifulSoup
from backend.canteens.canteen import Canteen, VEGGIE, MEAT
from datetime import datetime
from urllib.request import urlopen

URL = 'http://singh-catering.de/cafe/'


def __parse_menu_items(items):
    text = ''
    for item in items.find_all('li', class_='menu-list__item'):
        title = item.find('span', class_='item_title').get_text()
        price = item.find('span', class_='menu-list__item-price').get_text()
        veggie = item.find('span', class_='menu-list__item-highlight-title')
        if veggie and (('VEGAN!' in veggie) or ('VEGETARISCH!' in veggie)):
            annotation = VEGGIE
        else:
            annotation = MEAT
        description = item.find('span', class_='desc__content').get_text()
        text = '%s%s *%s: %s*\n_%s_\n' % (text, annotation, title, price, description)
    return text


def __parse_menu():
    today = datetime.now().weekday()
    html = urlopen(URL).read()
    soup = BeautifulSoup(html, 'html.parser')
    menu_items = soup.find_all('ul', class_='menu-list__items')

    menu = {
        0: __parse_menu_items(menu_items[0]),  # Monday
        1: __parse_menu_items(menu_items[3]),  # Tuesday
        2: __parse_menu_items(menu_items[1]),  # Wednesday
        3: __parse_menu_items(menu_items[4]),  # Thursday
        4: __parse_menu_items(menu_items[2]),  # Friday
        5: 'Heute geschlossen.\nMontag gibt es:\n%s' % __parse_menu_items(menu_items[0]),  # Saturday
        6: 'Heute geschlossen.\nMontag gibt es:\n%s' % __parse_menu_items(menu_items[0]),  # Sunday
    }
    return '[Singh Catering](%s) (bis 18:00)\n%s' % (URL, menu[today])


def get_menu(url=''):
    return __parse_menu()

singh = Canteen(
    id_='tu_singh',
    name='Singh Catering',
    url='http://singh-catering.de/cafe/',
    update=get_menu,
    website='http://singh-catering.de'
)

CANTEENS = [singh]

if __name__ == '__main__':
    print(__parse_menu())
