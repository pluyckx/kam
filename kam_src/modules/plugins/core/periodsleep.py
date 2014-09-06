##\package periodsleep
# \brief Kam periodically execute the check plugins. This \e period is controlled by this plugin.
#
# Check the config file for more information.
# Look for the field \e period in the section \e [global]
#
# \author Philp Luyckx
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

from modules.plugins.core.base import CoreBase

import time

class PeriodSleep(CoreBase):
	CONFIG_NAME = "global"
	CONFIG_ITEM_PERIOD = "period"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]
		self._last_run = time.clock_gettime(time.CLOCK_MONOTONIC)


	def _execute(self):
		now = time.clock_gettime(time.CLOCK_MONOTONIC)
		delta = now - self._last_run
		time_to_sleep = self._sleep - delta

		if time_to_sleep > 0:
			time.sleep(time_to_sleep)

		self._last_run = time.clock_gettime(time.CLOCK_MONOTONIC)

	def loadConfig(self, config):
		err_value = ""
		section = config[self.CONFIG_NAME]
		if section:
			try:
				sleep = int(section.get(self.CONFIG_ITEM_PERIOD))
			except ValueError as e:
				err_value = str(e)
				sleep = 0
		else:
			sleep = None

		if sleep != None and sleep > 10:
			self._sleep = sleep
			self._enable()
		else:
			sleep = 0
			self._sleep = 10
			err_value += ";No sleep value entered or sleep < 10, using default sleep period of 10 seconds"

		if self._log:
			if sleep == None:
				self._log.log(self,\
				              "No section [global] found to load the period from! Using default of 10 for sleep!")
			elif sleep == 0:
				self._log.log(self,\
				              "The config contains an invalid vlaue for [global] -> period. Please enter an integer larger than 0, default sleep value of 10 used!")
			else:
				self._log.log(self,\
				              "Config loaded, period time = {0} seconds".format(self._sleep))

		if self._debug:
			self._debug.log(self._debug.TYPE_CONFIG, self,\
					self.CONFIG_ITEM_PERIOD, self._sleep,\
					err_value, self.isEnabled())

def createInstance(data_dict):
	return PeriodSleep(data_dict)

