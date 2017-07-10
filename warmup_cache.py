from backend.canteens.tasks import update_personalkantine, update_singh, update_studierendenwerk

update_personalkantine.delay()
update_singh.delay()
update_studierendenwerk.delay()
