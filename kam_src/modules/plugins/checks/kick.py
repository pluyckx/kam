
import os

from modules.plugins.checks.basecheck import BaseCheck

class KickCheck(BaseCheck):
	CONFIG_NAME = "kick"
	CONFIG_ITEM_FILES = "files"

	def __init__(self, config, log, debug = None):
		super().__init__()
		self._debug = debug
		self._log = log

		self.loadConfig(config)

	def _run(self):
		alive = []

		for f in self._files:
			if os.path.exists(f):
				alive.append(f)
				os.remove(f)

		if len(alive) > 0:
			self._alive()
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
			self._enable()
			files = files.split(",")
			for f in files:
				self._files.append(f.strip())
		else:
			self._disable()

		if self._log:
			self._log.log("[Kick] Config loaded, enabled={0}; files specified: {1}\n".format(self.isEnabled(), self._files))

