##\package kick
# \brief This plugins checks if the machine is alive by checking if a file exists.
#
# In the config file you can create a section [kick].
# This section contains the field \e files.
# In this field you can define a list of files, separated by commas.
# The plugin will check if each file exists.
# When one file in the list exists, the server is kept alive.
# All files in the list are removed if they exist.
#
# This way you can implement a sort of "kick" mechanism, where the creation of a file from the list is a kick.
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

class KickCheck(BaseCheck):
	CONFIG_NAME = "kick"
	CONFIG_ITEM_FILES = "files"
	DEFAULT_PATH = "/tmp/kam_kick"

	def __init__(self, data_dict):
		super().__init__()
		self._debug = data_dict["debug"]
		self._log = data_dict["log"]

	def _run(self):
		alive = []

		for f in self._files:
			if os.path.exists(f):
				alive.append(f)
				os.remove(f)

		if len(alive) > 0:
			self._alive()
		else:
			self._dead()

		if self._debug:
			self._debug.log(self._debug.TYPE_CHECK, self,\
			                self.CONFIG_ITEM_FILES, alive, "", "")

	def loadConfig(self, config):
		self._files = []
		err_value = ""

		try:
			section = config[self.CONFIG_NAME]
		except KeyError as e:
			section = None
			err_value = str(e)
		
		if section:
			files = section.get(self.CONFIG_ITEM_FILES).strip()
		else:
			files = None

		self._files.append(self.DEFAULT_PATH)
		self._enable()

		if files:
			files = files.split(",")
			for f in files:
				self._files.append(f.strip())

		if self._log:
			self._log.log(self,\
			              "Config loaded, enabled={0}; files specified: {1}\n"\
			                .format(self.isEnabled(), self._files))
		
		if self._debug:
                        self._debug.log(self._debug.TYPE_CONFIG, self,\
			                self.CONFIG_ITEM_FILES, self._files,\
			                err_value, self.isEnabled())


## \brief Create an instance of this class
#
# \public
# \param data_dict This dictionary must contain the keys "log" and "config" and optionally "debug". They contain an object of the type Log, configparser and Debug respectively.
# \return An object of the type KickCheck
def createInstance(data_dict):
	return KickCheck(data_dict)
