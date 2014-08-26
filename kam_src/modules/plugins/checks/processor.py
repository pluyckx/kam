
import os

from modules.plugins.checks.basecheck import BaseCheck

import psutil

class ProcessorCheck(BaseCheck):
	CONFIG_NAME = "processor"
	CONFIG_ITEM_TOTAL = "total_load"
	CONFIG_ITEM_PER_CPU = "per_cpu_load"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debuggers"]
		self._log = data_dict["logs"]

		self._total = 50
		self._per_cpu = 40

		self._prev_times = []
		for i in range(0, os.cpu_count()):
			self._prev_times.append((0.0, 0.0))


	def _run(self):
		per_cpu = psutil.cpu_times(percpu=True)
		per_cpu_percent = []
		total = 0
		total_idle = 0
		keep_alive_total = False
		keep_alive_per_cpu = False

		for i in range(0, len(per_cpu)):
			cpu = per_cpu[i]
			(prev_total, prev_idle) = self._prev_times[i]

			total_time = cpu.user + cpu.system + cpu.idle + cpu.nice + cpu.iowait + cpu.irq + cpu.softirq + cpu.steal + cpu.guest + cpu.guest_nice

			delta_time = total_time - prev_total
			delta_idle = cpu.idle - prev_idle

			percent = (1 - delta_idle / delta_time) * 100
			total += percent

			self._prev_times[i] = (total_time, cpu.idle)

			per_cpu_percent.append(percent)

			if self._per_cpu != None and percent >= self._per_cpu:
				keep_alive_per_cpu = True

		total = total / os.cpu_count()

		keep_alive_total = (total != None and total >= self._total)
		keep_alive = keep_alive_total or keep_alive_per_cpu

		if keep_alive:
			self._alive()
		else:
			self._dead()

		if self._debug:
			self._debug.log(self._debug.TYPE_CHECK, self, "total_load", total, "", keep_alive_total)
			self._debug.log(self._debug.TYPE_CHECK, self, "per_cpu_load", per_cpu_percent, "", keep_alive_per_cpu)

	def loadConfig(self, config):
		try:
			total = config[self.CONFIG_NAME].get(self.CONFIG_ITEM_TOTAL)
		except KeyError:
			total = None

		try:
			per_cpu = config[self.CONFIG_NAME].get(self.CONFIG_ITEM_PER_CPU)
		except KeyError:
			per_cpu = None

		self._total = float(total) if total else total
		self._per_cpu = float(per_cpu) if per_cpu else per_cpu

		if self._total != None or self._per_cpu != None:
			self._enable()
		else:
			self._disable()

		if self._log:
			self._log.log(self, "Config file read!\nenabled = {0}\ntotal = {1}\nper_cpu = {2}\n".format(self.isEnabled(), self._total, self._per_cpu))

def createInstance(data_dict):
	return ProcessorCheck(data_dict)

