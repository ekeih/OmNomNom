import os
import sys
import urllib.request
import time
import re

def main(date):
  dishes = []
  pdf = "/tmp/MA-aktuell.pdf"
  url = "http://personalkantine.personalabteilung.tu-berlin.de/pdf/MA-aktuell.pdf"
  menu = "/tmp/MA-aktuell.txt"
  blocksPerDay = 1
  blockSizePerDay = [ 6 ]

  urllib.request.urlretrieve (url, pdf)
  os.system("pdftotext " + pdf)
  prepare_menu(menu)

  days = {  "Montag" : 0,
            "Dienstag" : 1,
            "Mittwoch" : 2,
            "Donnerstag" : 3,
            "Freitag" : 4
  }
  offset = -1
  header_end_line = -1

  # find current date, offset and header line numbers
  with open(menu) as search:
    # jump to start of file
    search.seek(0, 0)
    for i, line in enumerate(search):
      line = line.rstrip()
      # current date + offset handling
      if line == date:
        if before in days:
          offset = days[before];
          break
      else:
        before = line[:-1]

    # jump back to start of file
    search.seek(0, 0)
    # handle header
    for i, line in enumerate(search):
      line = line.rstrip()
      if line == "MwSt. enthalten":
        header_end_line = i
        break

    if offset == -1:
      return ["Date (" + date + ") not found."]

    if header_end_line == -1:
      return ["Header unexpected!"]

    dishes = []
    blockcount = 0
    linecount = 0

    # jump back to start of file
    search.seek(0, 0)
    for i, line in enumerate(search):
      line = line.rstrip()

      if i <= header_end_line:
        continue

      if line == "€":
        blockcount = blockcount + 1
        linecount = 0
        continue

      # finished after block
      if blockcount >= (offset + 1) * blocksPerDay:
          break

      # still not current block
      if blockcount < offset * blocksPerDay:
        continue

      inblockcount = blockcount - offset * blocksPerDay

      # read dish
      if linecount < blockSizePerDay[inblockcount]:
        dishes.append(line)
      # read price
      else:
        pos = linecount - blockSizePerDay[inblockcount];
        for k in range(0, inblockcount):
          pos = pos + blockSizePerDay[k]
        dishes[pos] = dishes[pos] + ": " + line + " €"

      linecount = linecount + 1

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
  before = ""
  with open(f, 'r') as menu:
    head = 1
    for line in menu:
      # remove header
      if head:
        if line == "Montag,\n":
          head = 0
        else:
          continue

      # remove footer
      if line == "€\n" and before == "€\n":
        break
      else:
        before = line[:-1]

      # remove indregend hints (e.g. '(Sch)')
      exp = re.compile('\([\w +]+\)')
      line = exp.sub('', line)

      # reduce whitespace
      exp = re.compile('[ \t]+')
      line = exp.sub(' ', line)

      if line.strip():
        new_menue.append(line)

  with open(f, 'w') as menu:
    menu.writelines(new_menue)

# vim:set ft et sw=2 sts=2:
