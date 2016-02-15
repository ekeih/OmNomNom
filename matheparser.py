import os
import sys
import datetime
import time
import re
import urllib.request
from bs4 import BeautifulSoup

def main(date):
  dishes = []
  url = "http://personalkantine.personalabteilung.tu-berlin.de/"
  html = urllib.request.urlopen(url).read()
  menu = BeautifulSoup( html, 'html.parser' ).find("ul", class_="Menu__accordion")

  for day in menu.children:
    if day.name and date in day.find("h2").string:
      for dishlist in day.children:
        if dishlist.name == 'ul':
          for dish in dishlist.find_all('li'):
            this_dish = ""
            for string in dish.stripped_strings:
              this_dish = this_dish + " " + string
            this_dish = _format( this_dish )
            dishes.append( this_dish )

  return dishes

def _format(line):
  line = line.strip()

  # remove indregend hints
  exp = re.compile('\([\w\s+]+\)')
  line = exp.sub('', line)

  # use common price tag design
  exp = re.compile('\s+(\d,\d+)\s+€')
  line = exp.sub(': \g<1>€', line)

  return line

def get_menue(date):
  dishes = main(date)
  menue = ""
  for dish in dishes:
    menue = menue + dish + "\n"
  menue = menue.rstrip()
  return menue

if __name__ == '__main__':
  print( get_menue( datetime.date.today().strftime("%d.%m.%Y")))

# vim:set ft et sw=2 sts=2:
