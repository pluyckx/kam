##\package logmanager
# \brief A manager like the DebugManager, but for logging.
#
# This manager can hold multiple loggers and will delegate calls to the log() function to them.
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

from modules.plugins.log.logger import Logger

class LogManager(Logger):
	
	def __init__(self):
		super().__init__()
		self._loggers = []

	def _log(self, plugin, msg):
		for logger in self._loggers:
			logger.log(plugin, msg)

	def add(self, logger):
		if isinstance(logger, Logger):
			self._enable()
			self._loggers.append(logger)
