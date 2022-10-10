#!/usr/bin/env python3

import bs4
import requests

HEADERS = {'user-agent': 'User-Agent: Mozilla'}
URL = 'https://www.stw.berlin/mensen/'

command_map = {
    147: "hu_nord",
    191: "hu_adlershof",
    270: "hu_spandauer",
    271: "fu_dueppel",
    277: "fu_rechtswissenschaft",
    319: "htw_wilhelminenhof",
    320: "htw_treskowallee",
    321: "tu_mensa",
    322: "fu_2",
    323: "fu_1",
    367: "hu_sued",
    368: "fu_osi",
    526: "hwr_badenschestr",
    527: "bht_luxembugerstr",
    528: "fu_lankwitz",
    529: "ehb_teltower_damm",
    530: "khs_weissensee",
    531: "hfm_charlottenstr",
    532: "khs_backshop",
    533: "hfs_ernstbusch",
    534: "ash_hellersdorf",
    537: "charite_zahnklinik",
    538: "tu_marchstr",
    540: "tu_architektur",
    541: "tu_wetterleuchten",
    542: "fu_pharmazie",
    631: "tu_veggie",
    657: "tu_skyline",
    660: "fu_koserstr",
    661: "hu_ct",
    723: "hfm_neuer_marstall",
    727: "hwr_alt_friedrichsfelde",
    5477: "bht_luxemburgerstr_backshop",
    5501: "hfm_charlottenstr_backshop",
    5302: "tu_mensa_backshop"
}

parsed_canteens = {}
unknown_canteens = {}
removed_canteens = {}
botfather_commands = []


request = requests.get(URL, headers=HEADERS) #, data=PARAMS)

if request.status_code == requests.codes.ok:
    checked_urls = []
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    overview = soup.find(text="Übersicht").parent.parent
    canteens = overview.findAll("div", class_="addrcard")
    for canteen in canteens:
        url = "https://www.stw.berlin/%s" % canteen.a.attrs["href"]
        name = canteen.a.text
        if url in checked_urls:
            print("Skipping duplicate: %s (%s)" % (name, url))
        else:
            print("Inspecting canteen: %s (%s)" % (name, url))
            checked_urls.append(url)
            canteen_request = requests.get(url, headers=HEADERS)
            if canteen_request.status_code == requests.codes.ok:
                canteen_soup = bs4.BeautifulSoup(canteen_request.text, 'html.parser')
                canteen_favorite = canteen_soup.find("div", id="favoriteMensa").attrs["onclick"]
                canteen_id = int(canteen_favorite.removeprefix("mensaFavorite(").split(",")[0])
                if command_map.get(canteen_id):
                    parsed_canteens[canteen_id] = {
                        "name": name,
                        "command": command_map.get(canteen_id),
                        # "url": url
                    }
                    botfather_commands.append("%s - %s" % (command_map.get(canteen_id), name))
                else:
                    unknown_canteens[canteen_id] = {
                        "name": name,
                        "url": url
                    }

for canteen_id, command in command_map.items():
    if not parsed_canteens.get(canteen_id):
        removed_canteens[canteen_id] = {
            "command": command
        }

print("\n=== Found canteens ===")
for canteen_id, canteen in parsed_canteens.items():
    print("%s: %s" % (canteen_id, canteen))

print("\n=== Unknwon canteens ===")
for canteen_id, canteen in unknown_canteens.items():
    print("%s: %s" % (canteen_id, canteen))


print("\n=== Removed canteens ===")
for canteen_id, canteen in removed_canteens.items():
    print("%s: %s" % (canteen_id, canteen))

print("\n=== BotFather commands ===")
botfather_commands_all = """
about - Über OmNomNom
help - Hilfe zum Bot
"""
botfather_commands.append("tu_personalkantine - TU Personalkantine")
botfather_commands.append("tu_en_kantine - TU EN Kantine")
botfather_commands.append("tu_singh - TU Singh")
botfather_commands.append("tu_cafenero - Cafeteria in der Volkswagen Bibliothek")
for command in sorted(botfather_commands):
    botfather_commands_all += "%s\n" % command
botfather_commands_all = botfather_commands_all.strip()
print(botfather_commands_all)

print("\n=== CANTEENS snippet ===")
print(parsed_canteens)
