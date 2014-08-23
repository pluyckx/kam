
from modules.exceptions.exceptions import KamFunctionNotImplemented

class Debugger:
	TYPE_CONFIG = "config"
	TYPE_CHECK = "check"

	def __init__(self):
		self._enabled = False

	def log(self, log_type, plugin, parameter_name, parameter_value, err_value, comments):
		if self._enabled:
			self._log(log_type, plugin, parameter_name, parameter_value, err_value, comments)

	def _log(self, log_type, plugin, parameter_name, parameter_value, err_value, comments):
		raise KamFunctionNotImplemented("log not implemented in class {0}".format(self.__class__.__name__))

	def _enable(self):
		self._enabled = True

	def _disable(self):
		self._enabled = False

	def loadConfig(self, config):
		pass
