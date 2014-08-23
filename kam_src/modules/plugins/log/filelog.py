
import os
import syslog
from datetime import datetime
from modules.plugins.log.logger import Logger

class FileLog(Logger):
	CONFIG_NAME = "filelog"
	CONFIG_ITEM_LINES = "max_lines"
	CONFIG_ITEM_PATH = "path"

	def __init__(self, callbacks):
		self.loadConfig(callbacks["config"]())
		

	def log(self, plugin, msg):
		if isinstance(plugin, str):
			plugin_name = plugin
		else:
			plugin_name = plugin.__class__.__name__

		content = []
		if os.path.exists(self._path):
			with open(self._path, "r+") as f:
				for line in f:
					content.append(line.rstrip("\n"))

		# we do not allow to print multiple lines, make one line of it!
		msg = msg.rstrip("\n").replace("\n", "; ")
		line = "{0} [{1}]: {2}\n".format(\
		                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),\
		                            plugin_name,\
		                            msg)
		                            

		if len(content) + 1 < self._max_lines or self._max_lines == 0:
			with open(self._path, "a") as f:
				f.write(line)
		else:
			start = len(content) - self._max_lines - 1
			with open(self._path, "w") as f:
				f.write("\n".join(content[start:]))
				f.write("\n")
				f.write(line)

	def loadConfig(self, config):
		config_name = self.CONFIG_NAME

		try:
			section = config[config_name]
		except KeyError:
			section = None

		if section:
			try:
				max_lines = section.get(self.CONFIG_ITEM_LINES)
			except KeyError:
				max_lines = None

			try:
				path = section.get(self.CONFIG_ITEM_PATH)
			except KeyError:
				path = None

			self._enable()
		else:
			self._disable()
			max_lines = None
			path = None
			syslog.syslog("[Kam-FileLog] No file log specified. File logging not enabled")

		if path == None:
			path = "/var/log/kam.log"
		if max_lines == None:
			max_lines = 0

		self._path = path
		try:
			self._max_lines = int(max_lines)
		except ValueError as ex:
			self._max_lines = 0

			syslog.syslog("[Kam-FileLog] Failed to parse max_lines from {0}; ValueError: {1}\n".format(max_lines, str(ex)))
		except TypeError as ex:
			self._max_lines = 0
			syslog.syslog("[Kam-FileLog] Failed to parse max_lines from {0}; Type Error {1}\n".format(max_lines, str(ex)))

		directory = os.path.dirname(self._path)
		if not os.path.exists(directory):
			os.makedirs(directory)

		self.log(self, "Config read, path={0}; max_lines={1}\n".format(self._path, self._max_lines))

def createInstance(callbacks):
	return FileLog(callbacks)

