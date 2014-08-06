
from exceptions.exceptions import KamFunctionNotImplemented

class BaseCheck:
	def __init__(self):
		self._keep_alive = False

	def check(self):
		raise KamFunctionNotImplemented("Process not implemented for class {0}".format(\
						self.__class__.__name__))

	def isKeepAlive(self):
		return self._keep_alive

	def _keepAlive(self):
		self._keep_alive = True

	def _dead(self):
		self._keep_alive = False

	def loadConfig(self, config_file):
		pass
