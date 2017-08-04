#!/usr/bin/env python3

import bs4
import requests

HEADERS = {'user-agent': 'User-Agent: Mozilla'}
PARAMS = {'resources_id': 534}
URL = 'https://www.stw.berlin/xhr/speiseplan-und-standortdaten.html'

request = requests.post(URL, headers=HEADERS, data=PARAMS)

if request.status_code == requests.codes.ok:
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    listbox = soup.find('select', class_='listboxStandorte')
    options = listbox.findAll('option')

    for option in options:
        canteen = '%s : %s' % (option.attrs['value'], option.get_text())
        print(canteen)
