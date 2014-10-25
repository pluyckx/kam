##\package utils
# \brief Here are some handy generic functions defined
#
# \author Philip Luyckx
# \copyright GNU Public License

# This file is part of Keep Alive Monitor (kam).
#
# Keep Alive Monitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Keep Alive Monitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Keep Alive Monitor.  If not, see <http://www.gnu.org/licenses/>.


def toBool(value):
	if isinstance(value, str):
		try:
			s_as_int = int(value)
		except:
			s_as_int = None

		true_list = [ "true", "True", "yes", "Yes" ]
		false_list = [ "false", "False", "no", "No" ]

		if value in true_list or (s_as_int != None and s_as_int):
			return True
		elif value in false_list or (s_as_int != None and not s_as_int):
			return False
	elif isinstance(value, int):
		return value != 0
	elif isinstance(value, float):
		return value != 0.0
	else:
		return False
