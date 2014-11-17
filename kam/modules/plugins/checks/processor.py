##\package processor
# \brief This plugin checks the processor usage to keep the machine alive
#
# In the config file you can define a section [processor].
# Here you can use two fields: \e total_load and \e per_cpu_load.
# 
# The \e total_load field defines the threshold of the avarage cpu load over all cpus.
# This value is a value between 0 and 100.
# 100 is used when all cores are 100% occupied and thus 0% idle.
#
# The \e per_cpu_load is a threshold per cpu.
# This value is also between 0 and 100.
#
# Look at the documentatino of the config file for more information.
#
# \author Philip Luyckx
# \copyright GNU Public License

# This file is part of Keep Alive Monitor (kam).
#
# Keep Alive Monitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Keep Alive Monitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Keep Alive Monitor.  If not, see <http://www.gnu.org/licenses/>.

import os

from kam.modules.plugins.checks.basecheck import BaseCheck

import psutil

class ProcessorCheck(BaseCheck):
	CONFIG_NAME = "processor"
	CONFIG_ITEM_TOTAL = "total_load"
	CONFIG_ITEM_PER_CPU = "per_cpu_load"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]

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

			if delta_time == 0:
				delta_time = 1

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
		err_value = ""
		err_total = ""
		err_per_cpu = ""

		try:
			section = config[self.CONFIG_NAME]
		except KeyError as ex:
			err_value = ex

		if section:
			try:
				total = float(section.get(self.CONFIG_ITEM_TOTAL))
			except ValueError as ex:
				total = None
				err_total = str(ex)

			try:
				per_cpu = section.get(self.CONFIG_ITEM_PER_CPU)
			except ValueError as ex:
				per_cpu = None
				err_per_cpu = str(ex)
		else:
			total = None
			per_cpu = None

		self._total = float(total) if total else None
		self._per_cpu = float(per_cpu) if per_cpu else None

		if self._total != None or self._per_cpu != None:
			self._enable()
		else:
			self._disable()

		if self._debug:
			self._debug.log(self._debug.TYPE_CONFIG, self, self.CONFIG_ITEM_TOTAL,\
			                self._total, err_value + ";" + err_total, self.isEnabled())
			self._debug.log(self._debug.TYPE_CONFIG, self, self.CONFIG_ITEM_PER_CPU,\
			                self._per_cpu, err_value + ";" + err_per_cpu, self.isEnabled())

		if self._log:
			self._log.log(self, "Config file read!\nenabled = {0}\ntotal = {1}\nper_cpu = {2}\n".format(self.isEnabled(), self._total, self._per_cpu))

def createInstance(data_dict):
	return ProcessorCheck(data_dict)

