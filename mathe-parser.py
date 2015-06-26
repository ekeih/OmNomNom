import os
import sys
import urllib

def main():
  if len(sys.argv) != 2:
    print sys.argv[0] + " must have provided the date as argmuent."
    sys.exit(1)

  pdf = "/tmp/MA-aktuell.pdf"
  menu = "/tmp/MA-aktuell.txt"
  date = sys.argv[1]
  SETLENGTH = 18
  SETSTART = 34
  DATESTART = 15

  urllib.urlretrieve ("http://personalkantine.personalabteilung.tu-berlin.de/pdf/MA-aktuell.pdf", pdf)
  os.system("pdftotext " + pdf)

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
      if i < DATESTART -1:
        continue
      if line == date:
        if before in days:
          offset = days[before];
          break
        else:
          print "Date found but at wrong position."
          sys.exit(2)
      else:
        before = line[:-1]

    if offset == -1:
      print "Date not found."
      sys.exit(3)

    # jump back to start of file
    search.seek(0, 0)

    cnt = 0
    dishes = []
    curset = SETSTART + offset * SETLENGTH -1

    for i, line in enumerate(search):
      if i < curset:
        continue
      if i >= curset + SETLENGTH:
        break

      line = line.rstrip()
      j = i - curset + 1

      if (j <= 4) or (j == 13):
        dishes.append(line)
      if (j >= 6) and (j <= 9):
        dishes[i - curset -5] = dishes[i - curset -5] + " (" + line + " Euro)"
      if j == 15:
        dishes[4] = dishes[4] + " (" + line + " Euro)"

    print str(dishes)
  # cleanup
  os.system("rm " + pdf + " " + menu)

if __name__ == "__main__":
  main()
