##\package pollmanager
# \brief This utility class can be used to poll files using a thread so they are "non-blocking".
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

from threading import Thread, Lock
import select

class PollManager(Thread):
	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]

	def hasInput(self, fd):
		poll = select.poll()
		poll.register(fd, select.POLLIN)
		more_input = len(poll.poll(0)) == 1
		poll.unregister(fd)

		return more_input
	

def createInstance(data_dict):
	return PollManager(data_dict)

