
from modules.exceptions.exceptions import KamFunctionNotImplemented

class CoreBase:
	def __init__(self):
		self._enabled = False

	def execute(self):
		if self._enabled:
			self._execute()

	def _execute(self):
		raise KamFunctionNotImplemented("_execute not implemented in class {0}".format(\
		                                self.__class__.__name__))

	def _enable(self):
		self._enabled = True

	def _disable(self):
		self._enabled = True

	def isEnabled(self):
		return self._enabled

	def loadConfig(self, config):
		pass
