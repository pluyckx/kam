
from modules.checkplugins.basecheck import BaseCheck
import psutil
from datetime import datetime, timedelta

class NetworkSpeedCheck(BaseCheck):
	CONFIG_NAME = "network"
	CONFIG_ITEM_UP_SPEED = "upload_speed"
	CONFIG_ITEM_DOWN_SPEED = "download_speed"

	def __init__(self, config, debug = None):
		self._debug = debug
		self._last_check = datetime.now()
		self._prev_down = 0
		self._prev_up = 0
		self.loadConfig(config)

	def check(self):
		network = psutil.net_io_counters(True)
		network_dl = 0
		network_up = 0

		for k in network:
			if k != "lo":
				network_dl += network[k].bytes_recv
				network_up += network[k].bytes_sent

		now = datetime.now()
		delta = now - self._last_check

		dl = (network_dl - self._prev_down) / delta.total_seconds()
		up = (network_up - self._prev_up) / delta.total_seconds()

		self._last_check = now
		self._prev_down = network_dl
		self._prev_up = network_up

		if dl >= self._down or up >= self._up:
			self._keepAlive()
		else:
			self._dead()

		if self._debug:
			self._debug.log("[NetworkSpeedCheck] down={0}, up={1} --> {2}\n".format(dl, up, self.isKeepAlive()))

	def loadConfig(self, config):
		try:
			down = self._convertToFloat(config[self.CONFIG_NAME].get(self.CONFIG_ITEM_DOWN_SPEED))
		except KeyError:
			self._down = None

		try:
			up = self._convertToFloat(config[self.CONFIG_NAME].get(self.CONFIG_ITEM_UP_SPEED))
		except KeyError:
			self._up = None

		self._down = down if down != None else 10.0 * 1024
		self._up = up if up != None else 10.0 * 1024

		if self._debug:
			self._debug.log("[NetworkSpeedCheck] Config file read.\ndownload_speed = {0}\nupload_speed = {1}\n".format(self._down, self._up))

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
