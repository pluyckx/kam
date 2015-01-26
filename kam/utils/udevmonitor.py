
import subprocess

class UDevMonitor(object):
	def __init__(self, data_dict):
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]
		self._pollmanager = data_dict["pollmanager"]

		self._callbacks = []

	def start(self):
		self._proc = subprocess.Popen([ "udevadm", "monitor" ], stdout=subprocess.PIPE, bufsize=0)

	def addCallback(self, callback):
		self._callbacks.append(callback)

	def check(self):
		if self._pollmanager.hasInput(self._proc.stdout):
			while self._pollmanager.hasInput(self._proc.stdout):
				igonore = self._proc.stdout.read(1000)

			for callback in self._callbacks:
				callback()

