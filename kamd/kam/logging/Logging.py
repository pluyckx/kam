
## @package Logging
# Here is a logging class declared

import os, sys
import kam.base.ConfigLoader as ConfigLoader
import kam.utils.utils as kam_utils
from logging.handlers import RotatingFileHandler
import logging

logger = None

def _convertLevel(level):
	level = level.upper()
	if level == "ERROR":
		ret = logging.ERROR
	elif level == "WARNING":
		ret = logging.WARNING
	elif level == "INFO": 
		ret = logging.INFO
	elif level == "DEBUG":
		ret = logging.DEBUG
	elif level == "CRITICAL":
		ret = logging.CRITICAL
	else:
		ret = logging.CRITICAL + 1

	return ret

def _convertLevelToStr(level):
	if level == logging.ERROR:
		ret = "ERROR"
	elif level == logging.WARNING:
		ret = "WARNING"
	elif level == logging.INFO:
		ret = "INFO"
	elif level == logging.DEBUG:
		ret = "DEBUG"
	elif level == logging.CRITICAL:
		ret = "CRITICAL"
	else:
		ret = "NONE"

	return ret


## A logging class that can log output to files and standard output
#
# The log level is set using the NONE, ERROR, WARNING, INFO and DEBUG constants. When a
# level is selected, also lower levels are logged. So when DEBUG is set, everything is logged.
class Logger(object):
	def __init__(self):
		global logger

		if not logger is None:
			raise RuntimeError("There is already a logger available")

		self._conf = ConfigLoader.getConfigLoader(ConfigLoader.ConfigLoader.GENERAL)

		self._logger = logging.getLogger("kam_logger")
		self._logger.setLevel(1)

		self._rfh = None
		self._sh = None
		self._formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

		self._configChanged()

		self._conf.addListener(self._configChanged)

	def debug(self, obj, msg):
		self._logger.debug(self._format(obj, msg))

	def info(self, obj, msg):
		self._logger.info(self._format(obj, msg))

	def warning(self, obj, msg):
		self._logger.warning(self._format(obj, msg))

	def error(self, obj, msg):
		self._logger.error(self._format(obj, msg))

	def critical(self, obj, msg):
		self._logger.critical(self._format(obj, msg))
		

	def _format(self, obj, msg):
		return "{0}: {1}".format(obj.__class__.__name__, msg)

	def _configChanged(self):
		warnings = []

		fileLevel = self._conf.get("logging", "filelevel")
		stdoutLevel = self._conf.get("logging", "stdoutlevel")
		filepath = self._conf.get("logging", "filepath")
		filesize = self._conf.get("logging", "filesize")
		rotateCount = self._conf.get("logging", "rotatecount")

		if filepath is None:
			filepath = "/var/log/kamd.log"
			warnings.append("Default path used \"{0}\"".format(filepath))

		if filesize is None:
			filesize = "1MiB"
			warnings.append("Default file size used {0}".format(filesize))

		if rotateCount is None:
			rotateCount = 2
			warnings.append("Default rotation count used {0}".format(rotateCount))
		else:
			try:
				rotateCount = int(rotateCount)
			except:
				warnings.append("rotatecount contains an invalid value \"{0}\"".format(rotateCount))
				rotateCount = 2
				warnings.append("Setting rotatecount to default \"{0}\"".format(rotateCount))

		if fileLevel is None:
			fileLevel = "WARNING"
			warnings.append("No file level defined, using default \"{0}\"".format(fileLevel))

		if stdoutLevel is None:
			stdoutLevel = "NONE"
			warnings.append("No stdout level defined, using default \"{0}\"".format(stdoutLevel))

		self._fileLevel = _convertLevel(fileLevel)
		self._stdoutLevel = _convertLevel(stdoutLevel)
		self._filepath = filepath
		self._rotateCount = rotateCount
		(sizeInBytes, size, unit) = kam_utils.getTextAsSize(filesize)

		if sizeInBytes is None:
			warnings.append("Unknown unit found in \"{0}\"".format(filesize))
			filesize = "1MiB"
			sizeInBytes = 1024 * 1024
			warnings.append("Default file size used \"{0}\"".format(filesize))

		self._filesize = sizeInBytes

		fileLevel = _convertLevelToStr(self._fileLevel)
		stdoutLevel = _convertLevelToStr(self._stdoutLevel)

		self._conf.set("logging", "filelevel", fileLevel)
		self._conf.set("logging", "stdoutlevel", stdoutLevel)
		self._conf.set("logging", "filepath", filepath)
		self._conf.set("logging", "filesize", filesize)
		self._conf.set("logging", "rotatecount", str(rotateCount))

		self._conf.store()

		if not (self._rfh is None):
			self._rfh.close()

		if not (self._sh is None):
			self._sh.flush()
			self._sh.close()

		self._rfh = RotatingFileHandler(self._filepath, maxBytes=self._filesize, backupCount=self._rotateCount, encoding="UTF-8")
		self._rfh.setLevel(self._fileLevel)
		self._rfh.setFormatter(self._formatter)

		self._sh = logging.StreamHandler()
		self._sh.setLevel(self._stdoutLevel)
		self._sh.setFormatter(self._formatter)

		while self._logger.hasHandlers():
			self._logger.removeHandler(self._logger.handlers[0])

		self._logger.addHandler(self._rfh)
		self._logger.addHandler(self._sh)

		for msg in warnings:
			self.warning(self, msg)


def getLogger():
	global logger
	if logger is None:
		logger = Logger()

	return logger

