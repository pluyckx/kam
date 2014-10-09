##\package BaseCheck
# \brief A base class for checks
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

class BaseCheck:
	## \brief The constructor
	#
	# Note this constructor is actually 'protected', so you should not create a object of the class BaseCheck, but you should use a subclass that uses BaseCheck as base class.
	# \protected
	def __init__(self):
		self._keep_alive = False
		self._is_enabled = False

	## Call this method to check if the machine is alive
	#
	# \public
	def check(self):
		if self.isEnabled():
			self._run()

	## \brief Run the checkcode if the plugin is enabled
	#
	# You should not call this function directly, call check() instead.
	# If the plugin is enabled, the function check() will call this function.
	# You should overide this function in the check plugins.
	#
	# \protected
	# \throws KanFunctionNotImplemented if the function is not overriden by a subclass.
	def _run(self):
		raise KamFunctionNotImplemented("_run not implemented in class {0}".format(\
                                                self.__class__.__name__))

	## \brief Tell the base class the plugin is enabled, so it should call the function _run() when check() is called.
	#
	# \protected
	def _enable(self):
		self._is_enabled = True

	## \brief Tell the base class the plugin is disabled. _run() will not call check().
	#
	# \protected
	def _disable(self):
		self._is_enabled = False

	## \brief Return if the plugin is enabled or not.
	#
	# \public
	# \return True if enabled, otherwise False
	def isEnabled(self):
		return self._is_enabled

	## \brief Returns if the machine is alive (this plugin has detected activity).
	#
	# Before calling this function, you should call check()
	#
	# \public
	# \return True if alive, otherwise False
	def isAlive(self):
		return self._keep_alive and self._is_enabled

	## \brief Tell the base class the machine is alive.
	#
	# This is a helper function, so subclasses can notify the machine is alive.
	#
	# \protected
	def _alive(self):
		self._keep_alive = True

	## \brief same as _alive(), but the machine is dead.
	#
	# \protected
	def _dead(self):
		self._keep_alive = False

	## \brief a function prototype to load a config from a parsed config file
	#
	# \public
	# \param config_file config_file is of the type configparser and is already loaded.
	def loadConfig(self, config_file):
		pass
