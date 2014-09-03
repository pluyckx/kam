
import os

from modules.plugins.checks.basecheck import BaseCheck

class KickCheck(BaseCheck):
	CONFIG_NAME = "kick"
	CONFIG_ITEM_FILES = "files"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]

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
			self._debug.log(self._debug.TYPE_CHECK, self,\
			                self.CONFIG_ITEM_FILES, alive, "", "")

	def loadConfig(self, config):
		self._files = []
		err_value = ""

		try:
			section = config[self.CONFIG_NAME]
		except KeyError as e:
			section = None
			err_value = str(e)
		
		if section:
			files = section.get(self.CONFIG_ITEM_FILES).strip()
		else:
			files = None

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
                        self._debug.log(self._debug.TYPE_CONFIG, self,\
			                self.CONFIG_ITEM_FILES, files,\
			                err_value, self.isEnabled())


def createInstance(data_dict):
	return KickCheck(data_dict)
