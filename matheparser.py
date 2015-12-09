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
  blocksPerDay = 2
  blockSizePerDay = [4, 1]

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

  # find current date and save offset
  with open(menu) as search:
    for i, line in enumerate(search):
      line = line.rstrip()
      if line == date:
        if before in days:
          offset = days[before];
          break
      else:
        before = line[:-1]

    if offset == -1:
      return ["Date (" + date + ") not found."]

    # jump back to start of file
    search.seek(0, 0)

    dishes = []
    blockcount = 0
    linecount = 0
    for i, line in enumerate(search):
      # skip date header
      if i < 10:
          continue

      line = line.rstrip()

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
      if linecount < blockSizePerDay[inblockcount]:
        dishes.append(line)
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
      if line == "Änderungen bleiben vorbehalten\n":
          break

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

#vim:set ft=vim et sw=2 sts=2
