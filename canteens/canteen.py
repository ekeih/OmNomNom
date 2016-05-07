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

class Canteen:
	def __init__(self, canteen):
		self.id_ = canteen['id_']
		self.name = canteen['name']
		self.url = canteen['url']
		self.website = canteen.get('website') or canteen['url']
		self.update = canteen['update']
	def __str__(self):
		return 'Canteen: %s' % self.name