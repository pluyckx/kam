
from modules.exceptions.exceptions import KamFunctionNotImplemented

class Log:
	def __init__(self):
		pass

	def log(self, msg):
		raise KamFunctionNotImplemented("log not implemented in class {0}".format(self.__class__.__name__))

	def loadConfig(self, config):
		pass
