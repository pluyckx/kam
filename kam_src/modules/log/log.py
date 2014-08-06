
import os
from datetime import datetime

class Log:
	def __init__(self, path="/var/log/kam.log", max_lines=200):
		self._path = path
		self._max_lines=max_lines

	def log(self, msg):
		content = []
		if os.path.exists(self._path):
			with open(self._path, "r+") as f:
				for line in f:
					content.append(line.rstrip("\n"))

		msg = "On " + str(datetime.now()) + "\n" + msg
		new_lines = msg.split("\n")
		content = content + new_lines
		if len(content) < self._max_lines:
			with open(self._path, "a") as f:
				f.write(msg)
		else:
			start = len(content) - self._max_lines
			with open(self._path, "w") as f:
				f.write("\n".join(content[start:]))

