# Copyright (C) 2016  Max Rosin
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
import threading
from canteens import matheparser, singh, studentenwerk
from time import sleep

logger = logging.getLogger()

class Cache:
  def __init__(self):
    self._read_ready = threading.Condition(threading.Lock())
    self._readers = 0
    self.canteens = {}

  def read(self, canteen_id):
    self._acquire_read()
    cached_message = self.canteens[canteen_id]
    self._release_read()
    logger.info('Read from cache: %s' % canteen_id)
    return cached_message

  def _acquire_read(self):
    self._read_ready.acquire()
    try:
      self._readers += 1
    finally:
      self._read_ready.release()

  def _release_read(self):
    self._read_ready.acquire()
    try:
      self._readers -= 1
      if not self._readers:
        self._read_ready.notifyAll()
    finally:
      self._read_ready.release()

  def _acquire_write(self):
    self._read_ready.acquire()
    while self._readers > 0:
      self._read_ready.wait()

  def _release_write(self):
    self._read_ready.release()


class Refresh(threading.Thread):
  def __init__(self, cache):
    threading.Thread.__init__(self)
    self._cache = cache
    self.setDaemon(True)
  def _refresh_one_canteen(self, canteen):
    update = canteen.update(url=canteen.url)
    self._cache._acquire_write()
    self._cache.canteens[canteen.id_] = update
    logger.info('Cached: %s' % canteen.name)
    self._cache._release_write()
  def run(self):
    while True:
      logger.info('Cache update started')
      update_threads = []
      for canteen in matheparser.CANTEENS + singh.CANTEENS + studentenwerk.CANTEENS:
        t = threading.Thread(target=self._refresh_one_canteen, args=[canteen])
        t.start()
        update_threads.append(t)
      for t in update_threads:
        t.join()
      logger.info('Cache update done')
      sleep(60 * 60)