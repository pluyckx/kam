
from modules.plugins.checks.basecheck import BaseCheck
import psutil
import time

class NetworkSpeedCheck(BaseCheck):
	CONFIG_NAME = "network"
	CONFIG_ITEM_UP_SPEED = "upload_speed"
	CONFIG_ITEM_DOWN_SPEED = "download_speed"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debuggers"]
		self._log = data_dict["logs"]

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

		if (self._down != None and dl >= self._down) or \
		   (self._up != None and up >= self._up):
			self._alive()
		else:
			self._dead()

		if self._debug:
			self._debug.log(self._debug.TYPE_CHECK, self,\
			                "upload_speed", up, "", up >= self._up)
			self._debug.log(self._debug.TYPE_CHECK, self,\
			                "download_speed", dl, "", dl >= self._down)

	def loadConfig(self, config):
		try:
			down = self._convertToFloat(config[self.CONFIG_NAME].get(self.CONFIG_ITEM_DOWN_SPEED))
		except KeyError:
			down = None

		try:
			up = self._convertToFloat(config[self.CONFIG_NAME].get(self.CONFIG_ITEM_UP_SPEED))
		except KeyError:
			up = None

		self._down = down
		self._up = up

		if self._down != None or self._up != None:
			self._enable()
		else:
			self._disable()

		if self._log:
			self._log.log(self, "Config file read.\nenabled = {0}\ndownload_speed = {1}\nupload_speed = {2}\n".format(self.isEnabled(), self._down, self._up))

	def _convertToFloat(self, s):
		if not s:
			return None

		last_ch = s[len(s)-1]
		if last_ch.isdigit():
			return float(s)
		else:
			try:
				value = float(s[:len(s)-1])
			except ValueError:
				return None

			if last_ch == 'K':
				value *= 1024
			elif last_ch == 'M':
				value *= 1024 * 1024

			return value

def createInstance(data_dict):
	return NetworkSpeedCheck(data_dict)

