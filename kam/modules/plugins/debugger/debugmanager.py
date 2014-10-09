##\package debugmanager
# \brief This debugger can hold other debugger objects and then passes all log messages to all of them.
#
# When you want to use multiple debuggers, you can use the DebugManager to hold all the debuggers.
# When you want to log, call the log() function of the DebugManager and he will delegate the log call to all debuggers he is holding.
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

from kam.modules.plugins.debugger.debugger import Debugger

class DebugManager(Debugger):
	
	def __init__(self):
		super().__init__()
		self._debuggers = []

	def _log(self, log_type, plugin, parameter_name, parameter_value, err_value, comments):
		for debugger in self._debuggers:
			debugger.log(log_type, plugin, parameter_name, parameter_value, err_value, comments)

	def add(self, debugger):
		if isinstance(debugger, Debugger):
			self._enable()
			self._debuggers.append(debugger)
