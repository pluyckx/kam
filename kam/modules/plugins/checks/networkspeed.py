##\package networkspeed
# \brief This plugin checks the current network activity.
#
# In the config file you can define a section [network] with the fields upload_speed and download_speed.
# They define thresholds and when more bandwidth is used, the machine is kept alive.
# This plugin calculates the bandwidth between two successive calls of check().
# So the first check() is actually a calibration and if needed, you should ignore the value of isAlive().
# Starting from the second call of check(), isAlive() contains a valid value.
#
# In the fields you can use the suffixes K and M.
# 1K = 1024bytes, 1M = 1024 * 1024 bytes
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

from kam.modules.plugins.checks.basecheck import BaseCheck
import psutil
import time

class NetworkSpeedCheck(BaseCheck):
	CONFIG_NAME = "network"
	CONFIG_ITEM_UP_SPEED = "upload_speed"
	CONFIG_ITEM_DOWN_SPEED = "download_speed"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]

		self._last_check = time.clock_gettime(time.CLOCK_MONOTONIC)
		self._prev_down = 0
		self._prev_up = 0


	def _run(self):
		network = psutil.net_io_counters(True)
		network_dl = 0
		network_up = 0

		for k in network:
			if k != "lo":
				network_dl += network[k].bytes_recv
				network_up += network[k].bytes_sent

		now = time.clock_gettime(time.CLOCK_MONOTONIC)
		delta = now - self._last_check

		dl = (network_dl - self._prev_down) / delta
		up = (network_up - self._prev_up) / delta

		self._last_check = now
		self._prev_down = network_dl
		self._prev_up = network_up

		if (self._down is not None and dl >= self._down) or \
		   (self._up is not None and up >= self._up):
			self._alive()
		else:
			self._dead()

		if self._debug:
			if self._up is not None:
				self._debug.log(self._debug.TYPE_CHECK, self,\
				                "upload_speed", up, "", up >= self._up)
			if self._down is not None:
				self._debug.log(self._debug.TYPE_CHECK, self,\
				                "download_speed", dl, "", dl >= self._down)

	def loadConfig(self, config):
		err_value = ""
		err_up = ""
		err_down = ""

		try:
			section = config[self.CONFIG_NAME]
		except KeyError as ex:
			err_value = ex
			section = None

		if section:
			down = self._convertToFloat(section.get(self.CONFIG_ITEM_DOWN_SPEED))
			up = self._convertToFloat(section.get(self.CONFIG_ITEM_UP_SPEED))

		if isinstance(down, float):
			self._down = down
		else:
			err_down = down
			self._down = None

		if isinstance(up, float):
			self._up = up
		else:
			err_up = up
			self._up = None

		if self._down != None or self._up != None:
			self._enable()
		else:
			self._disable()

		if self._debug:
			self._debug.log(self._debug.TYPE_CONFIG, self, self.CONFIG_ITEM_DOWN_SPEED,\
			                self._down, err_value + ";" + err_down, self.isEnabled() and self._down is not None)
			self._debug.log(self._debug.TYPE_CONFIG, self, self.CONFIG_ITEM_UP_SPEED,\
			                self._up, err_value + ";" + err_up, self.isEnabled() and self._up is not None)


		if self._log:
			self._log.log(self, "Config file read.\nenabled = {0}\ndownload_speed = {1}\nupload_speed = {2}\n".format(self.isEnabled(), self._down, self._up))

	def _convertToFloat(self, s):
		if not s:
			return "Parameter is \"{0}\"".format(s)

		last_ch = s[len(s)-1]
		if last_ch.isdigit():
			try:
				f = float(s)
				return f
			except ValueError as e:
				return str(e)
		else:
			try:
				value = float(s[:len(s)-1])
			except ValueError as e:
				return str(e)

			if last_ch == 'K':
				value *= 1024
			elif last_ch == 'M':
				value *= 1024 * 1024

			return value

def createInstance(data_dict):
	return NetworkSpeedCheck(data_dict)

