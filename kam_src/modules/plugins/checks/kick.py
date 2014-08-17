
import os

from modules.plugins.checks.basecheck import BaseCheck
from modules.plugins.log.debuglog import DebugLog

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
			self._debug.log(DebugLog.TYPE_CHECK, self,\
			                self.CONFIG_ITEM_FILES, alive, "", "")

	def loadConfig(self, config):
		self._files = []
		err_value = ""

		try:
			files = config[self.CONFIG_NAME].get(self.CONFIG_ITEM_FILES).strip()
		except KeyError as e:
			files = None
			err_value = str(e)

		if files:
			self._enable()
			files = files.split(",")
			for f in files:
				self._files.append(f.strip())
		else:
			self._disable()

		if self._log:
			self._log.log(self,\
			              "Config loaded, enabled={0}; files specified: {1}\n"\
			                .format(self.isEnabled(), self._files))
		
		if self._debug:
                        self._debug.log(DebugLog.TYPE_CONFIG, self,\
			                self.CONFIG_ITEM_FILES, files,\
			                err_value, self.isEnabled())

def createInstance(config, log, debug = None):
	return KickCheck(config, log, debug)
