
import os

from modules.checkplugins.basecheck import BaseCheck

class KickCheck(BaseCheck):
	CONFIG_NAME = "kick"
	CONFIG_ITEM_FILES = "files"

	def __init__(self, config, log, debug = None):
		self._debug = debug
		self._log = log

		self.loadConfig(config)

	def check(self):
		alive = []

		for f in self._files:
			if os.path.exists(f):
				alive.append(f)
				os.remove(f)

		if len(alive) > 0:
			self._keepAlive()
		else:
			self._dead()

		if self._debug:
			self._debug.log("[Kick] Kicked by files: {0}\n".format(alive))

	def loadConfig(self, config):
		self._files = []

		try:
			files = config[self.CONFIG_NAME].get(self.CONFIG_ITEM_FILES).strip()
		except KeyError:
			files = None


		if files:
			files = files.split(",")
			for f in files:
				self._files.append(f.strip())

		if self._debug:
			self._debug.log("[Kick] Config loaded, files specified: {0}\n".format(self._files))

