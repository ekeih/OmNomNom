from datetime import datetime, timedelta
from emoji import emojize

tvstud = emojize('*:zap::zap: 2. Warnstreik der studentischen Beschäftigten :zap::zap:*\n\n'
                 'Nach 17 Jahren Lohnstillstand und 5 gescheiterten Verhandlungsrunden streiken '
                 'die studentischen Beschäftigten Berlins vom *23.01. bis 25.01.* für einen neuen '
                 'Tarifvertrag. Auch als Studierende könnt ihr helfen, indem ihr an den Kundgebungen teilnehmt '
                 'und euch bei der Uni [beschwert](https://jetzt-streik.de).\n\n:mega: Streikt mit '
                 ':mega:\n:bangbang: Solidarisiert euch :bangbang:\n'
                 ':point_right: [Informiert euch](https://tvstud.berlin) :point_left:', use_aliases=True)


def get_daily_schedule(date):
    schedules = {
        '2018-01-23': emojize('*:zap::zap:TUB Programm für den 23.01.:zap::zap:*\n\n'
                              '- ab 9.30 Uhr Streikcafé im ASTA TU Berlin\n'
                              '- 9.30-12 Uhr TU aufwecken! Aktionen auf dem Campus (Treffpunkt: ASTA TU Berlin) '
                              '(Streikposten einrichten, Flyern, Banner aufhängen, Folientranspi uvm.)\n'
                              '- 12-14 Uhr studentische Vollversammlung (Raum H 1058)\n'
                              '- ab 15 Uhr Soli-Küche\n'
                              '- 15-20 Uhr Kundgebung und Konzerte',
                              use_aliases=True),
        '2018-01-24': emojize('*:zap::zap:TUB Programm für den 24.01.:zap::zap:*\n\n'
                              '- ab 9.30 Uhr Streikcafé im ASTA TU Berlin und Aktionen auf dem Campus\n'
                              '- 10-12 Uhr Campusrundgang\n'
                              '- 12 Uhr Workshops (Bühnenfechten - Mathematik-Foyer/1.OG, Tanzen - Architektur-Foyer, '
                              'Kurzfilme - Café Shila, Arbeitsrecht - Blaues Foyer (Hauptgebäude EG rechts), '
                              'Literaturkreis und Häkeln - Hauptgebäude Foyer, Blue Engineering, '
                              'Tapeten/Schilder malen)\n'
                              '- 13 Uhr gemeinsames Essen in der Mensa\n'
                              '- 14 Uhr Science Slam/Poetry Slam bzw. Powerpoint Karaoke (Hauptgebäude)\n'
                              '- 16 Uhr Filmvorführung "We want sex/Made in Dunghamn" (Hauptgebäude/MA)',
                              use_aliases=True),
        '2018-01-25': emojize('*:zap::zap:TUB Programm für den 25.01.:zap::zap:*\n\n'
                              '- ab 9.30 Uhr Streikcafé im ASTA TU Berlin und Aktionen auf dem Campus\n'
                              '- 13 Uhr Gemeinsame Anfahrt zur Demo mit der U2 bis Wittenbergplatz\n'
                              '- 13:30 Uhr berlinweite Demo vom Olof-Palme-Platz (Elefantentor des Zoos) zur TU)\n'
                              '- ab ca. 15 Uhr Kundgebung, danach Party :tada:',
                              use_aliases=True)
    }
    message_for_all_days = '*Kommt auch wenn ihr nicht studentisch beschäftigt seid!*\n\n' \
                           'Parallel wird es im ASTA TU Berlin (KF-Gebäude hinter dem Hauptgebäude) jeweils ' \
                           'tagsüber ein Streikbüro geben.\nFür Kunstinteressierte gibt es sogar einen Streikstein ' \
                           'im Foyer des MAR-Gebäudes zu finden, den die freitagsrunde (MAR 0.005) installiert hat.\n' \
                           'Streiklisten werden an den dezentralen Tagen von ver.di und GEW im ASTA-TU-Streikbüro ' \
                           'ausliegen. Am zentralen, berlinweiten Streiktag (Donnerstag) werden die Streiklisten bei ' \
                           'der Demo zu finden sein.'
    schedule = schedules.get(date.strftime('%Y-%m-%d'))

    if schedule:
        return '%s\n\n%s' % (schedule, message_for_all_days)
    else:
        return False


def get_strike_message():
    today = datetime.now()
    if today.hour > 19:
        schedule = get_daily_schedule(today + timedelta(1))
    else:
        schedule = get_daily_schedule(today)
    if schedule:
        return '%s\n\n%s\n\n\n' % (tvstud, schedule)
    else:
        return '%s\n\n\n' % tvstud
