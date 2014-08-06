
import os

from modules.checkplugins.basecheck import BaseCheck
import psutil

class ProcessorCheck(BaseCheck):
	CONFIG_NAME = "processor"
	CONFIG_ITEM_TOTAL = "total_load"
	CONFIG_ITEM_PER_CPU = "per_cpu_load"

	def __init__(self, config, debug = None):
		self._total = 50
		self._per_cpu = 40
		self._debug = debug

		self._prev_times = []

		for i in range(0, os.cpu_count()):
			self._prev_times.append((0.0, 0.0))

		self.loadConfig(config)

	def check(self):
		per_cpu = psutil.cpu_times(percpu=True)
		per_cpu_percent = []
		total = 0
		total_idle = 0
		keep_alive = False

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

			if percent >= self._per_cpu:
				keep_alive = True

		total = total / os.cpu_count()

		keep_alive = keep_alive or (total >= self._total)

		if keep_alive:
			self._keepAlive()
		else:
			self._dead()

		if self._debug:
			self._debug.log("Cpu check: total={0} per_cpu={1} --> {2}\n".format(total, per_cpu_percent, keep_alive))

	def loadConfig(self, config):
		try:
			self._total = float(config[self.CONFIG_NAME].get(self.CONFIG_ITEM_TOTAL))
		except KeyError:
			self._total = 50.0

		try:
			self._per_cpu = float(config[self.CONFIG_NAME].get(self.CONFIG_ITEM_PER_CPU))
		except KeyError:
			self._per_cpu = 40.0

		if self._debug:
			self._debug.log("Config file read!\ntotal = {0}\nper_cpu = {1}\n".format(self._total, self._per_cpu))
