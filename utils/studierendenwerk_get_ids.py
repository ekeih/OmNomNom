#!/usr/bin/env python3

import bs4
import requests
import textwrap

HEADERS = {'user-agent': 'User-Agent: Mozilla'}
PARAMS = {'resources_id': 534}
URL = 'https://www.stw.berlin/xhr/speiseplan-und-standortdaten.html'

request = requests.post(URL, headers=HEADERS, data=PARAMS)

if request.status_code == requests.codes.ok:
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    listbox = soup.find('select', class_='listboxStandorte')
    options = listbox.findAll('option')

    # Prepare Mapping
    # print('mapping = {')
    # for option in options:
    #     id_ = option.attrs['value']
    #     name = option.get_text()
    #     print('%s: "%s",' % (id_, name))
    # print('}')

    mapping = {
        534: "ash_hellersdorf",
        535: "beuth_kurfuerstenstr",
        527: "beuth_luxembugerstr",
        537: "charite_zahnklinik",
        529: "ehb_teltower_damm",
        271: "fu_dueppel",
        322: "fu_2",
        528: "fu_lankwitz",
        531: "hfm_charlottenstr",
        533: "hfs_schnellerstr",
        320: "htw_treskowallee",
        319: "htw_wilhelminenhof",
        147: "hu_nord",
        191: "hu_adlershof",
        367: "hu_sued",
        270: "hu_spandauer",
        526: "hwr_badenschestr",
        532: "khs_mensa",
        530: "khs_weissensee",
        321: "tu_mensa",
        323: "fu_veggie",
        368: "fu_ihnestr",
        660: "fu_koserstr",
        542: "fu_pharmazie",
        277: "fu_rechtswissenschaft",
        543: "fu_wirtschaftswissenschaften",
        726: "htw_treskowallee_cafeteria",
        659: "hu_wilhelm_grimm_zentrum",
        539: "tu_ackerstr",
        540: "tu_architektur",
        657: "tu_skyline",
        631: "tu_mensa_cafeteria",
        541: "tu_wetterleuchten",
        538: "tu_marchstr",
        722: "udk_jazz_cafe",
        658: "udk_lietzenburgerstr",
        647: "beuth_coffeebar",
        648: "beuth_coffeebar_haus_grashof",
        1407: "ehb_teltower_damm_coffeebar",
        723: "hfm_neuer_marstall",
        724: "hfm_charlottenstr_coffeebar",
        725: "htw_wilhelminenhof_coffeebar",
        661: "hu_ct",
        721: "hu_nord_coffeebar",
        720: "hu_adlershof_coffeebar",
        727: "hwr_alt_friedrichsfelde",
        728: "hwr_badenschestr_coffeebar",
        649: "fu_2_coffeebar",
        650: "fu_lankwitz_coffeebar",
        632: "tu_mensa_coffeebar",
    }

    # Generate Celery Tasks
    # for option in options:
    #     id_ = int(option.attrs['value'])
    #     name = option.get_text()
    #     func = """\
    #     # %s
    #     @app.task(bind=True, default_retry_delay=30)
    #     def update_%s(self):
    #         try:
    #             logger.info('[Update] %s')
    #             menu = __parse_menu(%s)
    #             if menu:
    #                 cache.set("%s", menu, ex=cache_interval * 4)
    #         except Exception as ex:
    #             raise self.retry(exc=ex)
    #
    #     """ % (name, mapping[id_], name, id_, mapping[id_])
    #     print(textwrap.dedent(func))

    # BotFather
    # for option in options:
    #     id_ = int(option.attrs['value'])
    #     name = option.get_text()
    #     print('%s - %s' % (mapping[id_], name))
    # print('about - Über OmNomNom')
    # print('tu_personalkantine - TU Personalkantine')
    # print('tu_singh - TU Singh')

    # new mapping
    # print('mapping = {')
    # for option in options:
    #     id_ = int(option.attrs['value'])
    #     name = option.get_text()
    #     canteen = '%s: { "name": "%s", "command": "%s"},' % (id_, name, mapping[id_])
    #     print(textwrap.dedent(canteen))
    # print('}')

    # beat
    for option in options:
        id_ = int(option.attrs['value'])
        name = option.get_text()
        schedule = """\
        'update %s': {
            'task': 'canteens.studierendenwerk.update_studierendenwerk',
            'args': [%s],
            'schedule': cache_interval
        },\
        """ % (mapping[id_], id_)
        print(textwrap.dedent(schedule))

    # warmup
    # for option in options:
    #     id_ = int(option.attrs['value'])
    #     print('update_studierendenwerk.delay(%s)' % id_)
