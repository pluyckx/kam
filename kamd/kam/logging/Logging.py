

class Logging(object):
	NONE = 0
	ERROR = 1
	WARNING = 2
	INFO = 3
	DEBUG = 4

	def __init__(self, fileLogLevel=Logging.INFO, \
	                   stdoutLogLevel=Logging.NONE):
		self._fileLogLevel = fileLogLevel
		self._stdoutLogLevel = stdoutLogLevel

	def debug(self, obj, msg):
		out = "[DEBUG] " + obj.__name__ + ": " + msg

		if self._fileLogLevel:
			pass

