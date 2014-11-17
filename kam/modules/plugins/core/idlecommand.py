##\package idlecommand
# \brief This plugin checks if the machine is idle and executes the idlecommand
#
# Check the config file for more information.
# Check the section [global] for the field \e idle_time and \e idle_command
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

from kam.modules.plugins.core.base import CoreBase
from kam.modules.plugins.debugger.debugger import Debugger

import time
import os

class IdleCommand(CoreBase):
	CONFIG_NAME = "global"
	CONFIG_ITEM_TIME = "idle_time"
	CONFIG_ITEM_COMMAND = "idle_command"

	def __init__(self, data_dict):
		super().__init__()

		self._log = data_dict["log"]
		self._debug = data_dict["debug"]

		self._check_list = data_dict["checks"]

		self._last_alive = time.clock_gettime(time.CLOCK_MONOTONIC)


	def _execute(self):
		now = time.clock_gettime(time.CLOCK_MONOTONIC)
		delta = now - self._last_alive

		is_alive = False
		no_checks_enabled = True
		for check in self._check_list:
			if check.isEnabled():
				no_checks_enabled = False
				if check.isAlive():
					is_alive = True
					break

		if is_alive:
			self._last_alive = now
		elif delta >= self._idle_time * 60:
			if no_checks_enabled:
				if self._log:
					self._log.log(self, "No checks enable. We do not execute the idle command!")
			else:
				os.system(self._idle_command)

		if self._log:
			self._log.log(self, "It is now {0}, the server is alive: {1}, when the server is dead for {2} seconds, the server will shutdown".format(\
			                     now, is_alive,
			                     self._idle_time * 60 if is_alive else self._idle_time*60 - delta))

	def loadConfig(self, config):
		err_value = ""
		section = config[self.CONFIG_NAME]

		if section:
			try:
				idle_time = int(section.get(self.CONFIG_ITEM_TIME))
				self._enable()
			except Exception as ex:
				err_value = str(ex)
				idle_time = 0
				self._disable()

			if idle_time > 0:
				idle_command = section.get(self.CONFIG_ITEM_COMMAND)
			else:
				idle_command = None

		else:
			self._disable()
			idle_time = None
			idle_command = None

		self._idle_time = idle_time
		self._idle_command = idle_command

		if self._log:
			if idle_time == None:
				self._log.log(self,\
				              "There is no global section which contains a value for idle_time.")
			elif idle_time <= 0:
				self._log.log(self,\
				              "idle_time contains an invalid value. Use an integer value larger than 0.")
			else:
				self._log.log(self,\
				              "Config loaded, idle_time = {0}, idle_command = {1}".format(self._idle_time, self._idle_command))

		if self._debug:
				self._debug.log(Debugger.TYPE_CONFIG, self,\
				                self.CONFIG_ITEM_TIME,\
				                self._idle_time,\
				                err_value, self.isEnabled())

				self._debug.log(Debugger.TYPE_CONFIG, self,\
				                self.CONFIG_ITEM_COMMAND,\
				                self._idle_command,\
				                "", self.isEnabled())
	

def createInstance(data_dict):
	return IdleCommand(data_dict)

