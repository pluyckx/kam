## @package BaseModule
# In this package you can find a base class for modules to monitor activities
# 

from kam.base.ConfigLoader import ConfigLoader

## BaseModule is a class that every monitor module must inherit
#
# The class has some base functionalities like loading the config file.
# It also has an interface to set if the system is active or not.
#
# You should not directoy create an instance of this class. This will result
# in errors due do not implemented functions.
class BaseModule(object):
	## The section of the config file used by the BaseModule implementation
	BASE_SECTION = "generic"
	## An option that is located in the generic section to tell if this module is enabled or not
	OPTION_ENABLED = "enabled"

	## Initilize the base module
	#
	# A subclass must call this init function! This function tries to receive the module
	# and gets the config file. Then it calls _loadConfig. When necessary, the subclass
	# should override this function.
	def __init__(self, logger):
		self._logger = logger

		module = self._getModuleName()

		self._config = ConfigLoader(module, defaultSettings)
		self._loadConfig()

		self._active = False

	## This is the public function to let the module do its work
	#
	# All doWork functions are called sequentially. If necessary, the module must use threads.
	# Do not override this function!
	def doWork(self):
		if self._enabled:
			self._doWork()
		else:
			self._inactive()

	## This is an abstract function which is called by doWork if the module is enabled.
	#
	# A subclass must override this function to perform its work! Keep in mind to
	# keep the worload as low as possible, because a module can monitor the cpu and
	# if you keep the cpu busy, this module will think that the system is active.
	def _doWork(self):
		raise NotImplementedError()

	## Returns if the module detects activity
	def isActive(self):
		return self._active

	## Returns if the module is enabled
	def isEnabled(self):
		return self._enabled

	## Enable the module
	#
	# @param temporary If this value is True, the config file is not updated
	def enable(self, temporary=True):
		self._enabled = True

		if not temporary:
			self._config.set(BaseModule.BASE_SECTION, BaseModule.ENABLED, enabled)
			self._config.storeConfig()

	## Disable the module
	#
	# @param temporary If this value is True, the config file is not updated
	def disable(self, temporary=True):
		self._enabled = False

		if not temporary:
			self._config.set(BaseModule.BASE_SECTION, BaseModule.ENABLED, enabled)
			self._config.storeConfig()

	## Tells the base implementation activity is detected
	def _active(self):
		self._active = True

	## Tells the base implementation no activity is detected
	def _inactive(self):
		self._active = False

	## Receive the config object. A subclass should call this function to receive the config object
	def _getConfigObject(self):
		return self._config

	## Request to reload the configuration.
	#
	# A subclass should not override this function. This function calls self._loadConfig
	def reloadConfig(self):
		self._config.reloadConfig()
		self._loadConfig()

	## Let the base implementation load the generic section of the config file
	#
	# A subclass should load its own configuration first, and then call the base
	# implementation. If the subclass has set some sections and options, they are
	# written out by calling the base implementation.
	#
	# When necessary, a subclass must override this function to load its configration.
	def _loadConfig(self):
		enabled = self._config.get(BaseModule.BASE_SECTION, BaseModule.ENABLED)

		if enabled is None:
			enabled = False # default False
			self._config.set(BaseModule.BASE_SECTION, BaseModule.ENABLED, enabled)

		self._enabled = enabled
		self._config.storeConfig() # if changed, the config file is stored

	## An abstract function to receive the modulename
	#
	# Each module must have a module name. This name is used to load the config file.
	# So each subclass must override this function and return a valid module name. A
	# good practice as module name is using its python library name, eg: base.BaseModule or
	# modules.networking.ConnectionMonitor
	def _getModuleName(self):
		raise NotImplementedError()
