##\package base
# \brief The base class for a core plugin.
#
# Core plugins are plugins that do not check parameters to keep the machine alive.
# They just execute some code to get a wanted behaviour.
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

from modules.exceptions.exceptions import KamFunctionNotImplemented

class CoreBase:
	## \brief The constructor
	def __init__(self):
		self._enabled = False

	## \brief Check if the core plugin is enabled, and call the _execute function if so.
	#
	# \public
	def execute(self):
		if self._enabled:
			self._execute()

	## \brief The actual implementation to execute when execute() is called
	#
	# Subclasses must override this function.
	def _execute(self):
		raise KamFunctionNotImplemented("_execute not implemented in class {0}".format(\
		                                self.__class__.__name__))

	## \brief Enable the plugin
	#
	# \protected
	def _enable(self):
		self._enabled = True

	## \brief disable the plugin
	#
	# \protected
	def _disable(self):
		self._enabled = True

	## \brief Check if the plugin is enabled
	#
	# \public
	def isEnabled(self):
		return self._enabled

	## \brief Load the configuration
	#
	# \public
	#
	# \param config The config file in the form of a \e configparser object.
	def loadConfig(self, config):
		pass
