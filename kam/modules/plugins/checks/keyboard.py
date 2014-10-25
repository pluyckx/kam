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

		if self._debug:
			self._read_from = []

	def isAlive(self):
		alive = super().isAlive()
		self._dead()
		return alive

	def _run(self):
		if self._debug:
			self._debug.log(self._debug.TYPE_CHECK, self, "read from: ", self._read_from, "", super().isAlive())
			self._read_from.clear()

	def _keyboardActive(self, fd, event):
		for f in self._files:
			if f.fileno() == fd:
				self._alive()
				while self._pollmanager.hasInput(f.fileno()):
					buf = f.read1(100)

				if self._debug and not f.name in self._read_from:
					self._read_from.append(f.name)

	def loadConfig(self, config):
		self._keyboards = []
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
		
		if s_keyboards:
			a_keyboards = s_keyboards.split(",")
			for s_keyboard in a_keyboards:
				s_keyboard = s_keyboard.strip()
				if s_keyboard == "auto":
					a_keyboard = self._findKeyboards()
				else:
					a_keyboard = [ s_keyboard ]

				for keyboard in a_keyboard:
					if not keyboard in self._keyboards:
						self._keyboards.append(keyboard)

		if len(self._keyboards) > 0:
			self._enable()
			for keyboard in self._keyboards:
				input_path = "/dev/input/{0}".format(keyboard)
				f = open(input_path, "rb")
				self._files.append(f)
				self._pollmanager.add(f.fileno(), self._keyboardActive)
		else:
			self._disable()

		if self._debug:
			self._debug.log(self._debug.TYPE_CONFIG, self, self.CONFIG_ITEM_KEYBOARDS,\
			                self._keyboards, err_value, self.isEnabled())

		if self._log:
			self._log.log(self, "Config loaded: enabled={0}; keyboards={1}\n".format(self.isEnabled(), self._keyboards))

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


def createInstance(data_dict):
	return KeyboardCheck(data_dict)

