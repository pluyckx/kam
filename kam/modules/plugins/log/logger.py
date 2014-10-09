##\package logger
# \brief A base class for loggers
#
# When you create a logger, you should use this template class.
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

from kam.modules.exceptions.exceptions import KamFunctionNotImplemented

class Logger:
	## \brief A basic constructor
	def __init__(self):
		self._enabled = False

	## \brief The log interface
	# \public
	#
	# This is a wrapper which checks if the logger is enabled. Then it calls the _log() function.
	#
	# \param plugin The plugin which is calling this log function. Most of the time you can use \e self.
	# \param msg The log message
	def log(self, plugin, msg):
		if self._enabled:
			self._log(plugin, msg)

	## \brief The actual log implementation
	# \protected
	#
	# For the parameters, check the \e log() function.
	def _log(self, plugin, msg):
		raise KamFunctionNotImplemented("log not implemented in class {0}".format(self.__class__.__name__))

	def _enable(self):
		self._enabled = True

	def _disable(self):
		self._enabled = False

	## \brief Load the configuration
	# \public
	# 
	# \param config The configuration in the form of a \e configparser object
	def loadConfig(self, config):
		pass
