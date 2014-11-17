##\package debugger
# \brief This is a base class for debuggers
#
# You cannot instantiate this class directly.
# You must use a subclass for this.
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

class Debugger:
	## \brief We are logging the configuration
	TYPE_CONFIG = "config"
	## \brief Log the check function
	TYPE_CHECK = "check"
	## \brief Log the execute function
	TYPE_EXECUTE = "execute"

	## \brief A basic constructor
	def __init__(self):
		self._enabled = False

	## \brief Log a message with some handy information
	#
	# \public
	#
	# This is just a wrapper function which checks if the debugger is enabled.
	# If so, it will pass all the parameters to the \e _log() function.
	#
	# \param log_type One of the TYPE_* constants of this class
	# \param plugin The plugin which is logging, most of the time you can use \e self for this.
	# \param parameter_name The name of the parameter you are logging
	# \param parameter_value The value of the parameter
	# \param err_value An error string which is appended to the line
	# \param comments Some extra comments which are appended after the error value.
	def log(self, log_type, plugin, parameter_name, parameter_value, err_value, comments):
		if self._enabled:
			self._log(log_type, plugin, parameter_name, parameter_value, err_value, comments)

	## \brief The function which contains the code to actually log everything
	# \protected
	# For the parameters, please check the \e log() documentation.
	def _log(self, log_type, plugin, parameter_name, parameter_value, err_value, comments):
		raise KamFunctionNotImplemented("log not implemented in class {0}".format(self.__class__.__name__))

	## \brief Enable the debugger
	def _enable(self):
		self._enabled = True

	## \brief disable the debugger
	def _disable(self):
		self._enabled = False

	## \brief Load the configuraiton.
	#
	# \param config The configuration file in the form of a \configparser object.
	def loadConfig(self, config):
		pass
