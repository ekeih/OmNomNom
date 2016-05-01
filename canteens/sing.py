# Copyright (C) 2016  Max Rosin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
from datetime import datetime
from terminaltables import AsciiTable
from urllib.request import urlopen

URL = 'http://singh-catering.de/cafe/'

def __parse_menu_items(items):
	table_data = []
	for item in items.find_all('li', class_='menu-list__item'):
		title = item.find('span', class_='item_title').get_text()
		price = item.find('span', class_='menu-list__item-price').get_text()
		table_data.append([title, price])
	table = AsciiTable(table_data)
	table.outer_border = False
	table.inner_column_border = False
	table.inner_heading_row_border = False
	return '```%s```' % table.table

def __parse_menu():
	today = datetime.now().weekday()
	html = urlopen(URL).read()
	soup = BeautifulSoup(html, 'html.parser')
	menu_items = soup.find_all('ul', class_='menu-list__items')

	menu = {
		0: __parse_menu_items(menu_items[0]), # Monday
		1: __parse_menu_items(menu_items[3]), # Tuesday
		2: __parse_menu_items(menu_items[1]), # Wednesday
		3: __parse_menu_items(menu_items[4]), # Thursday
		4: __parse_menu_items(menu_items[2]), # Friday
		5: 'Heute geschlossen.\nMontag gibt es:\n%s' % __parse_menu_items(menu_items[0]), # Saturday
		6: 'Heute geschlossen.\nMontag gibt es:\n%s' % __parse_menu_items(menu_items[0]), # Sunday
	}
	return '[Sing Catering](%s)\n%s' % (URL, menu[today])
	
def get_menu():
	return __parse_menu()

if __name__ == '__main__':
	print(__parse_menu())