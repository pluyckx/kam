
from modules.plugins.log.logger import Logger

class LogManager(Logger):
	
	def __init__(self):
		super().__init__()
		self._loggers = []

	def _log(self, plugin, msg):
		for logger in self._loggers:
			logger.log(plugin, msg)

	def add(self, logger):
		if isinstance(logger, Logger):
			self._enable()
			self._loggers.append(logger)
