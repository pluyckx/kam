
from modules.plugins.core.base import CoreBase
from modules.plugins.debugger.debugger import Debugger

import time
import os

class IdleCommand(CoreBase):
	CONFIG_NAME = "global"
	CONFIG_ITEM_TIME = "idle_time"
	CONFIG_ITEM_COMMAND = "idle_command"

	def __init__(self, callbacks):
		super().__init__()

		self._log = callbacks["logs"]()
		self._debug = callbacks["debuggers"]()

		self._check_list = callbacks["checks"]()

		self._last_alive = time.clock_gettime(time.CLOCK_MONOTONIC)

		self.loadConfig(callbacks["config"]())

	def _execute(self):
		now = time.clock_gettime(time.CLOCK_MONOTONIC)
		delta = now - self._last_alive

		is_alive = False
		for check in self._check_list:
			if check.isEnabled():
				if check.isAlive():
					is_alive = True
					break

		if is_alive:
			self._last_alive = now
		elif delta >= self._idle_time * 60:
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
	

def createInstance(callbacks):
	return IdleCommand(callbacks)

