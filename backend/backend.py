from celery import Celery
from celery.utils.log import get_task_logger
from os import environ
from redis import Redis

logger = get_task_logger(__name__)

redis_host = environ.get('OMNOMNOM_REDIS_HOST') or 'localhost'
redis_port = environ.get('OMNOMNOM_REDIS_PORT') or 6379

cache_interval = environ.get('OMNOMNOM_CACHE_INTERVAL') or 60 * 60
cache_database = environ.get('OMNOMNOM_CACHE_DATABASE') or 0

celery_database = environ.get('OMNOMNOM_CELERY_DATABASE') or 1

cache = Redis(host=redis_host, port=redis_port, db=cache_database)

app = Celery('backend',
             broker='redis://%s:%s/%s' % (redis_host, redis_port, celery_database),
             include=[
                 'canteens.cafenero',
                 'canteens.personalkantine',
                 'canteens.singh',
                 'canteens.studierendenwerk',
                 'omnomgram.tasks',
                 'stats.tasks'
             ]
             )
app.conf.timezone = 'Europe/Berlin'
app.conf.beat_schedule = {
    'update cafenero': {
        'task': 'canteens.cafenero.update_cafenero',
        'schedule': cache_interval
    },
    'update singh': {
        'task': 'canteens.singh.update_singh',
        'schedule': cache_interval
    },
    'update personalkantine': {
        'task': 'canteens.personalkantine.update_personalkantine',
        'schedule': cache_interval
    },
    'update ash_hellersdorf': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [534],
        'schedule': cache_interval
    },
    'update beuth_kurfuerstenstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [535],
        'schedule': cache_interval
    },
    'update beuth_luxembugerstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [527],
        'schedule': cache_interval
    },
    'update charite_zahnklinik': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [537],
        'schedule': cache_interval
    },
    'update ehb_teltower_damm': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [529],
        'schedule': cache_interval
    },
    'update fu_dueppel': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [271],
        'schedule': cache_interval
    },
    'update fu_2': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [322],
        'schedule': cache_interval
    },
    'update fu_lankwitz': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [528],
        'schedule': cache_interval
    },
    'update hfm_charlottenstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [531],
        'schedule': cache_interval
    },
    'update hfs_schnellerstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [533],
        'schedule': cache_interval
    },
    'update htw_treskowallee': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [320],
        'schedule': cache_interval
    },
    'update htw_wilhelminenhof': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [319],
        'schedule': cache_interval
    },
    'update hu_nord': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [147],
        'schedule': cache_interval
    },
    'update hu_adlershof': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [191],
        'schedule': cache_interval
    },
    'update hu_sued': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [367],
        'schedule': cache_interval
    },
    'update hu_spandauer': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [270],
        'schedule': cache_interval
    },
    'update hwr_badenschestr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [526],
        'schedule': cache_interval
    },
    'update khs_mensa': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [532],
        'schedule': cache_interval
    },
    'update khs_weissensee': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [530],
        'schedule': cache_interval
    },
    'update tu_mensa': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [321],
        'schedule': cache_interval
    },
    'update fu_veggie': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [323],
        'schedule': cache_interval
    },
    'update fu_ihnestr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [368],
        'schedule': cache_interval
    },
    'update fu_koserstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [660],
        'schedule': cache_interval
    },
    'update fu_pharmazie': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [542],
        'schedule': cache_interval
    },
    'update fu_rechtswissenschaft': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [277],
        'schedule': cache_interval
    },
    'update fu_wirtschaftswissenschaften': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [543],
        'schedule': cache_interval
    },
    'update htw_treskowallee_cafeteria': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [726],
        'schedule': cache_interval
    },
    'update hu_wilhelm_grimm_zentrum': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [659],
        'schedule': cache_interval
    },
    'update tu_ackerstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [539],
        'schedule': cache_interval
    },
    'update tu_architektur': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [540],
        'schedule': cache_interval
    },
    'update tu_skyline': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [657],
        'schedule': cache_interval
    },
    'update tu_mensa_cafeteria': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [631],
        'schedule': cache_interval
    },
    'update tu_wetterleuchten': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [541],
        'schedule': cache_interval
    },
    'update tu_marchstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [538],
        'schedule': cache_interval
    },
    'update udk_jazz_cafe': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [722],
        'schedule': cache_interval
    },
    'update udk_lietzenburgerstr': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [658],
        'schedule': cache_interval
    },
    'update beuth_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [647],
        'schedule': cache_interval
    },
    'update beuth_coffeebar_haus_grashof': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [648],
        'schedule': cache_interval
    },
    'update ehb_teltower_damm_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [1407],
        'schedule': cache_interval
    },
    'update hfm_neuer_marstall': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [723],
        'schedule': cache_interval
    },
    'update hfm_charlottenstr_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [724],
        'schedule': cache_interval
    },
    'update htw_wilhelminenhof_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [725],
        'schedule': cache_interval
    },
    'update hu_ct': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [661],
        'schedule': cache_interval
    },
    'update hu_nord_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [721],
        'schedule': cache_interval
    },
    'update hu_adlershof_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [720],
        'schedule': cache_interval
    },
    'update hwr_alt_friedrichsfelde': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [727],
        'schedule': cache_interval
    },
    'update hwr_badenschestr_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [728],
        'schedule': cache_interval
    },
    'update fu_2_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [649],
        'schedule': cache_interval
    },
    'update fu_lankwitz_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [650],
        'schedule': cache_interval
    },
    'update tu_mensa_coffeebar': {
        'task': 'canteens.studierendenwerk.update_studierendenwerk',
        'args': [632],
        'schedule': cache_interval
    }
}


if __name__ == '__main__':
    app.start()
