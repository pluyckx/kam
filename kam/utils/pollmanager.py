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

		self._fds = []
		self._fds_new = []
		self._lock = Lock()
		self._lock_poll = Lock()
		self._stop_poll = True
		self._poll = select.poll()

	def add(self, fd, callback, event_mask = 1):
		self._lock.acquire()
		self._fds_new.append((fd, event_mask, callback))
		self._lock.release()

		if not self.isAlive() and self._stop_poll:
			self._stop_poll = False
			self.start()

	def remove(self, fd, callback):
		rm = []
		for fds in self._fds:
			(_fd, _, _callback) = fds
			if _fd == fd and _callback == callback:
				rm.append(fds)

		for i in rm:
			if self._debug:
				self._debug.log(self._debug.TYPE_EXECUTE, self, "Remove", i, None, None)
			self._fds.remove(i)

	def stop(self):
		self._stop_poll = True

	def run(self):
		poll = self._poll

		while not self._stop_poll and (len(self._fds) > 0 or len(self._fds_new) > 0):
			self._lock.acquire()
			while len(self._fds_new) > 0:
				fd = self._fds_new.pop()
				self._fds.append((fd[0], fd[1], fd[2]))
				poll.register(fd[0], fd[1])
			self._lock.release()

			self._lock_poll.acquire()
			ret = poll.poll(1000)
			self._lock_poll.release()

			if len(ret) > 0:
				for (fd, event) in ret:
					f = self._find_fd(fd)
					if not f:
						self._log.log(self, "fd {0} not found in registered list!".format(fd))
					else:
						f[2](fd, event)

	def hasInput(self, fd):
		self._lock_poll.acquire()
		f = self._find_fd(fd)
		if f:
			self._poll.unregister(fd)

		poll = select.poll()
		poll.register(fd, select.POLLIN)
		more_input = len(poll.poll(0)) == 1

		poll.unregister(fd)
		if f:
			self._poll.register(f[0], f[1])
		self._lock_poll.release()

		return more_input
	

	def _find_fd(self, fd):
		for f in self._fds:
			if f[0] == fd:
				return f

		return None

def createInstance(data_dict):
	return PollManager(data_dict)

