import emoji
from canteens.canteen import FISH, MEAT, VEGAN, VEGGIE

about_text = """*OmNomNom*

OmNomNom is a Telegram bot to get canteen information. Currently it supports only canteens in Berlin (Germany) \
and most of its answers are in German.
The bot is available as [@OmnBot](https://telegram.me/OmnBot). Feel free to talk to it and invite it to your groups.

Find out more about it on [Github](https://github.com/ekeih/OmNomNom). Pull requests and issues are always welcome. If \
you have questions you can talk to me via [Telegram](https://telegram.me/ekeih).

OmNomNom is licensed under the [GNU AGPL v3](https://github.com/ekeih/OmNomNom#license).
"""


help_text = """
*OmNomNom - Hilfe*

Hallo,

für jede Mensa gibt es einen Befehl, den du mir schicken kannst.

Für die Mensa der TU-Berlin ist das zum Beispiel: /tu\_mensa.

Außerdem kannst du in gewissem Rahmen auch nach Speiseplänen aus der Zukunft fragen. Ob diese wirklich verfügbar sind, \
hängt davon ab, ob die Kantinen sie bereitstellen. Zum Beispiel:

```
/tu_mensa montag
/tu_mensa tomorrow
/tu_mensa next friday
```

Alle verfügbaren Mensen und andere Befehle (wie zum Beispiel /help oder /about) findest du über die \
Auto-Vervollständigung von Telegram, wenn du anfängst eine Nachricht zu tippen, die mit `/` beginnt.
Außerdem gibt es in den meisten Telegram-Clients neben dem Textfeld einen viereckigen Button, der einen `/` enthält, \
über den du alle verfügbaren Befehle auswählen kannst.

Übrigens kannst du mich auch in Gruppen einladen, sodass mich dort jeder nach den Speiseplänen fragen kann.

Ich markiere Gerichte nach bestem Gewissen, aber ohne Garantie, mit folgenden Symbolen:

%s = Vegan
%s = Vegetarisch
%s = Fleisch
%s = Fisch

Viel Spaß und guten Appetit! %s
Bei Problemen sprich einfach @ekeih an.

PPS: Der Bot ist OpenSource (GNU AGPL v3) und den Code findest du auf [GitHub](https://github.com/ekeih/OmNomNom). %s
""" % (VEGAN, VEGGIE, MEAT, FISH, emoji.emojize(':cake:', language='alias'),
       emoji.emojize(':smile:', language='alias'))
