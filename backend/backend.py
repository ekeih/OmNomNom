#!/usr/bin/env python3

# Copyright (C) 2017  Max Rosin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import redis
import time

from canteens import matheparser, singh, studentenwerk

canteens = matheparser.CANTEENS + singh.CANTEENS + studentenwerk.CANTEENS

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

redis_host = os.environ.get('OMNOMNOM_REDIS_HOST') or 'localhost'
cache = redis.Redis(host=redis_host)

logger.debug('Initialize Cache')

while True:
    for canteen in canteens:
        menu = canteen.update(url=canteen.url)
        cache.set(canteen.id_, menu, ex=60*60)
        logger.debug('Cached %s' % canteen.id_)
    time.sleep(300)
