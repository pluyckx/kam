
from modules.exceptions.exceptions import KamFunctionNotImplemented

class BaseCheck:
	def __init__(self):
		self._keep_alive = False
		self._is_enabled = False

	def check(self):
		if self.isEnabled():
			self._run()

	def _run(self):
		raise KamFunctionNotImplemented("_run not implemented in class {0}".format(\
                                                self.__class__.__name__))

	def _enable(self):
		self._is_enabled = True

	def _disable(self):
		self._is_enabled = False

	def isEnabled(self):
		return self._is_enabled

	def isAlive(self):
		return self._keep_alive and self._is_enabled

	def _alive(self):
		self._keep_alive = True

	def _dead(self):
		self._keep_alive = False

	def loadConfig(self, config_file):
		pass
