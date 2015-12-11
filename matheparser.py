import os
import sys
import urllib.request
import time
import re
import itertools

def main(date):
  dishes = []
  pdf = "/tmp/MA-aktuell.pdf"
  url = "http://personalkantine.personalabteilung.tu-berlin.de/pdf/MA-aktuell.pdf"
  menu = "/tmp/MA-aktuell.txt"

  urllib.request.urlretrieve (url, pdf)
  os.system("pdftotext -layout -nopgbrk " + pdf + " " + menu)
  prepare_menu(menu)

  # find current date, offset and header line numbers
  with open(menu) as f:
    date_found = 0
    # jump to start of file
    f.seek(0, 0)
    for i, line in enumerate(f):
      dishes = []
      line = line.rstrip()

      # check for not price finished line (occurs after friday)
      if date_found == 1:
        if not line.endswith("€"):
          endline = i
          date_found = 0

      # check for next date
      if date_found == 1:
        exp = re.compile('^\d\d\.\d\d\.\d\d ')
        if exp.match(line):
          endline = i-1
          date_found = 0

      # find start line (MUST be after checking for next date)
      if line.startswith( date ):
        startline = i-1
        date_found = 1

    f.seek(0, 0)
    lines = itertools.islice(f, startline, endline)
    for line in lines:
      line = line.rstrip()

      # remove date tag
      exp = re.compile('^\d\d\.\d\d\.\d\d ')
      line = exp.sub('', line)

      # remove day tag
      exp = re.compile('^(Montag|Dienstag|Mittwoch|Donnerstag|Freitag), ')
      line = exp.sub('', line)

      # replave "vegetarisch" durch "(veg)"
      exp = re.compile('^vegetarisch')
      line = exp.sub('(veg)', line)

      # use common price tag design
      exp = re.compile(' +(\d,\d+) +€$')
      line = exp.sub(': \g<1>€', line)

      dishes.append(line)

  # cleanup
  os.system("rm " + pdf + " " + menu)
  return dishes

def get_menue(date):
  dishes = main(date)
  menue = ""
  for dish in dishes:
    menue = menue + dish + "\n"
  menue = menue.rstrip()
  return menue

def prepare_menu(f):
  new_menue = []
  with open(f, 'r') as menu:
    for line in menu:
      # remove indregend hints (e.g. '(Sch)')
      exp = re.compile('\([\w +]+\)')
      line = exp.sub('', line)

      # reduce whitespace
      exp = re.compile('[ \t]+')
      line = exp.sub(' ', line)

      # remove leading whitespace
      exp = re.compile('^ ')
      line = exp.sub('', line)

      # remove empty lines
      if line.strip():
        new_menue.append(line)

  with open(f, 'w') as menu:
    menu.writelines(new_menue)
if __name__ == '__main__':
  print( get_menue("11.12.15"))

# vim:set ft et sw=2 sts=2:
