
from modules.checkplugins.basecheck import BaseCheck

import psutil

class ProcessesCheck(BaseCheck):
	CONFIG_NAME = "process"
	CONFIG_ITEM_PROCESSES = "processes"
	CONFIG_ITEM_MIN_COUNT = "min_{0}"

	def __init__(self, config, log, debug = None):
		self._debug = debug
		self._log = log
		self.loadConfig(config)

	def check(self):
		if len(self._processes) == 0:
			self._dead()
			return

		for cnf_process in self._processes:
			cnf_process.resetCount()
		
		found_processes = []
		for process in psutil.process_iter():
			found_processes.append(process.name)

		alive = None

		for process in found_processes:
			for cnf_process in self._processes:
				if cnf_process.isProcess(process):
					cnf_process.incCount()
					if cnf_process.getCount() >= cnf_process.getMinCount():
						alive = cnf_process
						break
			if alive:
				break

		if alive:
			self._keepAlive()
		else:
			self._dead()

		if self._debug:
			self._debug.log("[Process] config list = {0}\n".format(self._processes))
			self._debug.log("[Process] found = {0}\n".format(found_processes))
			self._debug.log("[Process] Kept alive {0} due to process {1}\n".format(alive != None, alive))

	def loadConfig(self, config):
		self._processes = []
		try:
			s_processes = config[self.CONFIG_NAME].get(self.CONFIG_ITEM_PROCESSES)
		except KeyError:
			s_processes = 0

		if s_processes:
			s_processes = s_processes.split(",")
			for s_process in s_processes:
				s_process = s_process.strip()
				min_count = config[self.CONFIG_NAME].get(self.CONFIG_ITEM_MIN_COUNT.format(s_process))
				if min_count:
					try:
						min_count = int(min_count)
					except Exception as ex:
						self._log.log(str(ex))

				if not min_count:
					min_count = 1

				self._processes.append(Process(s_process, min_count))

		if self._debug:
			self._debug.log("[process] Config loaded: {0}\n".format(self._processes))


class Process:
	def __init__(self, name, min_count):
		self._name = name
		self._min_count = min_count
		self._count = 0

	def isProcess(self, name):
		return self._name == name

	def getCount(self):
		return self._count

	def getMinCount(self):
		return self._min_count

	def resetCount(self):
		self._count = 0

	def incCount(self):
		self._count += 1

	def __str__(self):
		return "{0} ({1})".format(self._name, self._min_count)

	def __repr__(self):
		return str(self)

