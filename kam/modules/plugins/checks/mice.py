##\package mice
# \brief This plugin checks if there is mouse input. If so, the machine is kept alive.
#
# In the config file you can create a sesction [mouse].
# Here you can define a comma separated list of mouse input locations: \e mouse, which the plugin must monitor.
# It is also possible to let the plugin find out the mouse input event in /dev/input, if it can autodetect your mice: great,
# if not, you need to find the input event yourself and add it to the list. You can also use auto detection + explicit define
# a path to a mouse input.
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

class MiceCheck(BaseCheck):
	CONFIG_NAME = "mouse"
	CONFIG_ITEM_MICE = "mice"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]
		self._pollmanager = data_dict["pollmanager"]
		self._files = []
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
			buf = f.read1(100)

	def _udev_event(self):
		if len(self._files) > 0:
			for f in self._files:
				try:
					f.close()
				except:
					pass # when the file does not exist...

			self._files = []

		self.loadConfig(self._config)


	def loadConfig(self, config):
		self._config = config

		err_value = ""

		try:
			section = config[self.CONFIG_NAME]
		except KeyError as e:
			section = None
			err_value = e
			s_mice = None

		if section:
			s_mice = section.get(self.CONFIG_ITEM_MICE)
		else:
			s_mice = None

		mice = []
		if s_mice:
			a_mice = s_mice.split(",")
			for s_mouse in a_mice:
				s_mouse = s_mouse.strip()
				if s_mouse == "auto":
					a_mouse = self._findMice()
				else:
					a_mouse = [ s_mouse ]

				for mouse in a_mouse:
					if not mouse in mice:
						mice.append(mouse)

		if len(mice) > 0:
			self._first_after_config = True
			self._enable()
			for mouse in mice:
				input_path = "/dev/input/{0}".format(mouse)
				f = open(input_path, "rb")
				self._files.append(f)
		else:
			self._disable()

		if self._debug:
			self._debug.log(self._debug.TYPE_CONFIG, self, self.CONFIG_ITEM_MICE,\
			                mice, err_value, self.isEnabled())

		if self._log:
			self._log.log(self, "Config loaded: enabled={0}; mice={1}\n".format(self.isEnabled(), mice))

	def _findMice(self):
		mice = []
		sys_path = "/sys/class/input"
		for event in os.listdir(sys_path):
			event_path = os.path.join(sys_path, event)
			device_path = os.path.join(event_path, "device")
			if os.path.exists(device_path):
				name_path = os.path.join(device_path, "name")
				if os.path.exists(name_path):
					with open(name_path, "r") as name_file:
						name = name_file.read().lower()

					if "mouse" in name or "mice" in name or "mouse" in name_path or "mice" in name_path:
						mice.append(event)

		return mice


def createInstance(data_dict):
	return MiceCheck(data_dict)

