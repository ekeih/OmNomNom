import datetime
import re
import urllib.request
from bs4 import BeautifulSoup
from backend.canteens.canteen import Canteen, VEGGIE, MEAT

URL = 'http://personalkantine.personalabteilung.tu-berlin.de/#speisekarte'


def main(date):
    dishes = []
    html = urllib.request.urlopen(URL).read()
    menu = BeautifulSoup(html, 'html.parser').find('ul', class_='Menu__accordion')

    for day in menu.children:
        if day.name and date.lstrip('0') in day.find('h2').string:
            for dishlist in day.children:
                if dishlist.name == 'ul':
                    items = dishlist.find_all('li')
                    for counter, dish in enumerate(items):
                        if counter >= len(items)-2:
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


def get_menu(url='', date=False):
    requested_date = date or datetime.date.today().strftime('%d.%m.%Y')
    dishes = main(requested_date)
    menu = ''
    for dish in dishes:
        menu = '%s%s\n' % (menu, dish)
    menu = menu.rstrip()
    menu = '[Personalkantine](%s) (%s) (11:00 - 16:00)\n%s' % (URL, requested_date, menu)
    return menu


personalkantine = Canteen(
    id_='tu_personalkantine',
    name='Personalkantine',
    url='http://personalkantine.personalabteilung.tu-berlin.de/#speisekarte',
    update=get_menu,
    website='http://personalkantine.personalabteilung.tu-berlin.de'
)

CANTEENS = [personalkantine]
