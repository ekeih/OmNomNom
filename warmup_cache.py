from canteens.cafenero import update_cafenero
from canteens.personalkantine import update_personalkantine
from canteens.singh import update_singh
from canteens.studierendenwerk import update_all_studierendenwerk_canteens

update_cafenero.delay()
update_personalkantine.delay()
update_singh.delay()
update_all_studierendenwerk_canteens.delay()
