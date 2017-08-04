from canteens.tasks import update_cafenero, update_personalkantine, update_singh, update_studierendenwerk

update_cafenero.delay()
update_personalkantine.delay()
update_singh.delay()
update_studierendenwerk.delay()
