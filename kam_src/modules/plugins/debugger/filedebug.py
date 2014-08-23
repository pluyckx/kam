
import os
from datetime import datetime
from modules.plugins.debugger.debugger import Debugger

class FileDebug(Debugger):
	CONFIG_NAME = "filedebug"
	CONFIG_ITEM_LINES = "max_lines"
	CONFIG_ITEM_PATH = "path"
	MSG_FORMAT = "{0} [{1}:{2}] {3} = {4}; {5} // {6}\n"

	def __init__(self, callbacks):
		self._logger = callbacks["logs"]()
		self.loadConfig(callbacks["config"]())
		

	def _log(self, log_type, plugin, parameter_name, parameter_value, err_value, comments):
		if isinstance(plugin, str):
			plugin_name = plugin
		else:
			plugin_name = plugin.__class__.__name__

		content = []
		if os.path.exists(self._path):
			with open(self._path, "r+") as f:
				for line in f:
					content.append(line.rstrip("\n"))

		now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		line = self.MSG_FORMAT.format(now, plugin_name, log_type,\
		                                  parameter_name, parameter_value,\
		                                  err_value, comments)

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

		if path == None:
			path = "/var/log/kam.debug"
		if max_lines == None:
			max_lines = 0

		self._path = path
		try:
			self._max_lines = int(max_lines)
		except ValueError:
			self._max_lines = 0

			if self._logger:
				self._logger.log("[DebugLog] Failed to parse max_lines from {0}\n".format(max_lines))
		except TypeError:
			self._max_lines = 0

		directory = os.path.dirname(self._path)
		if not os.path.exists(directory):
			os.makedirs(directory)

		if self._logger:
			self._logger.log(self, "Config read, path={0}; max_lines={1}\n".format(self._path, self._max_lines))

def createInstance(callbacks):
	return FileDebug(callbacks)

