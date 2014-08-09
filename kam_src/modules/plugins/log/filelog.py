
import os
from datetime import datetime
from modules.plugins.log.log import Log

class FileLog(Log):
	CONFIG_NAME = "{0}"
	CONFIG_ITEM_LINES = "max_lines"
	CONFIG_ITEM_PATH = "path"

	def __init__(self, config, log_type="log", log=None):
		self._log = log
		self._log_type = log_type
		self.loadConfig(config)
		

	def log(self, msg):
		content = []
		if os.path.exists(self._path):
			with open(self._path, "r+") as f:
				for line in f:
					content.append(line.rstrip("\n"))

		msg = "On " + str(datetime.now()) + "\n" + msg
		new_lines = msg.split("\n")
		content = content + new_lines
		if len(content) < self._max_lines or self._max_lines == 0:
			with open(self._path, "a") as f:
				f.write(msg)
		else:
			start = len(content) - self._max_lines
			with open(self._path, "w") as f:
				f.write("\n".join(content[start:]))

	def loadConfig(self, config):
		config_name = self.CONFIG_NAME.format(self._log_type)

		try:
			section = config[config_name]
		except KeyError:
			section = None

		if self._log:
			log = self._log
		else:
			log = self

		if section:
			try:
				max_lines = section.get(self.CONFIG_ITEM_LINES)
			except KeyError:
				max_lines = None

			try:
				path = section.get(self.CONFIG_ITEM_PATH)
			except KeyError:
				path = None

		else:
			max_lines = None
			path = None

		if path == None:
			path = "/var/log/kam." + self._log_type
		if max_lines == None:
			max_lines = 0

		self._path = path
		try:
			self._max_lines = int(max_lines)
		except ValueError:
			self._max_lines = 0

			log.log("[FileLog] Failed to parse max_lines from {0}\n".format(max_lines))
		except TypeError:
			self._max_lines = 0

		directory = os.path.dirname(self._path)
		if not os.path.exists(directory):
			os.makedirs(directory)

		log.log("[FileLog] config read, path={0}; max_lines={1}\n".format(self._path, self._max_lines))

