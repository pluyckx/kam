
from modules.plugins.debugger.debugger import Debugger

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
