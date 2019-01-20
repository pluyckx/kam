##\package keyboard
# \brief This plugin checks if there is keyboard input. If so, the machine is kept alive.
#
# In the config file you can create a sesction [keyboard].
# Here you can define a comma separated list of keyboard input locations: \e keyboards, which the plugin must monitor.
# It is also possible to let the plugin find out the keyboad input event in /dev/input, if it can autodetect your keyboads: great,
# if not, you need to find the input event yourself and add it to the list. You can also use auto detection + explicit define
# a path to a keyboad input.
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

from kam.modules.plugins.checks.basecheck import BaseCheck
from threading import Lock

import os

class KeyboardCheck(BaseCheck):
	CONFIG_NAME = "keyboard"
	CONFIG_ITEM_KEYBOARDS = "keyboards"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]
		self._pollmanager = data_dict["pollmanager"]
		self._files = []
		self._keyboards = []
		self._first_after_config = False

		self._udevmonitor = data_dict["udevmonitor"]
		self._udevmonitor.addCallback(self._udev_event)

	def _run(self):
		read_from = []

		for f in self._files:
			try: # There is a change the file does not exist anymore!
				if self._pollmanager.hasInput(f.fileno()):
					self._flush_input(f)
					read_from.append(f.name)
			except:
				if not os.path.exists(f.name):
					try:
						f.close()
					except:
						# TODO: propably this is not necessary, check if we should close a file that does not exist anymore.
						pass

				self._files.remove(f)


		if len(read_from) > 0 or self._first_after_config:
			self._first_after_config = False
			self._alive()
		else:
			self._dead()

		if self._debug:
			self._debug.log(self._debug.TYPE_CHECK, self, "read from: ", read_from, "", super().isAlive())


	def _flush_input(self, f):
		while self._pollmanager.hasInput(f.fileno()):
			_ = f.read1(100)


	def _udev_event(self):
		self.loadConfig(self._config)

	def loadConfig(self, config):
		self._config = config
		err_value = ""

		try:
			section = config[self.CONFIG_NAME]
		except KeyError as e:
			section = None
			err_value = e
			s_keyboards = None

		if section:
			s_keyboards = section.get(self.CONFIG_ITEM_KEYBOARDS)
		else:
			s_keyboards = None

		keyboards = []
		if s_keyboards:
			a_keyboards = s_keyboards.split(",")
			for s_keyboard in a_keyboards:
				s_keyboard = s_keyboard.strip()
				if s_keyboard == "auto":
					a_keyboard = self._findKeyboards()
				else:
					a_keyboard = [ s_keyboard ]

				for keyboard in a_keyboard:
					if not keyboard in keyboards:
						keyboards.append(keyboard)

		if len(keyboards) > 0:
			self._enable()

			if self._newKeyboardsFound(keyboards):
				self._first_after_config = True

				for f in self._files:
					try:
						f.close()
					except:
						pass

				self._keyboards = keyboards
				self._files = []

				for keyboard in keyboards:
					input_path = "/dev/input/{0}".format(keyboard)
					f = open(input_path, "rb")
					self._files.append(f)
		else:
			self._disable()

		if self._debug:
			self._debug.log(self._debug.TYPE_CONFIG, self, self.CONFIG_ITEM_KEYBOARDS,\
			                keyboards, err_value, self.isEnabled())

		if self._log:
			self._log.log(self, "Config loaded: enabled={0}; trigger_alive={2}; keyboards={1}\n".format(self.isEnabled(), keyboards, self._first_after_config))

	def _findKeyboards(self):
		keyboards = []
		sys_path = "/sys/class/input"
		for event in os.listdir(sys_path):
			event_path = os.path.join(sys_path, event)
			device_path = os.path.join(event_path, "device")
			if os.path.exists(device_path):
				name_path = os.path.join(device_path, "name")
				if os.path.exists(name_path):
					with open(name_path, "r") as name_file:
						name = name_file.read().lower()

					if "keyboard" in name or "keyboard" in name_path:
						keyboards.append(event)

		return keyboards


	def _newKeyboardsFound(self, newKeyboards):
		for keyboard in self._keyboards:
			if keyboard not in newKeyboards:
				return True

		for keyboard in newKeyboards:
			if keyboard not in self._keyboards:
				return True

		return False


def createInstance(data_dict):
	return KeyboardCheck(data_dict)

