
from modules.exceptions.exceptions import KamFunctionNotImplemented

class Logger:
	def __init__(self):
		self._enabled = False

	def log(self, plugin, msg):
		if self._enabled:
			self._log(plugin, msg)

	def _log(self, plugin, msg):
		raise KamFunctionNotImplemented("log not implemented in class {0}".format(self.__class__.__name__))

	def _enable(self):
		self._enabled = True

	def _disable(self):
		self._enabled = False

	def loadConfig(self, config):
		pass
