## @package ConfigLoader
# In this package a loader for a config file is specified

import os, sys
import configparser

configLoaders = {}

## A ConfigLoader which can read and write config files using configparser
class ConfigLoader(object):
	## this can be used for the module parameter. This will load the generic settings.
	GENERAL = "settings"

	## Initialize a new ConfigLoader.
	#
	# You should not instantiate a config loader yourself. You should use the function
	# getConfigLoader for this. This function makes sure a config file is only loaded
	# by one ConfigLoader, so when you change stuff, it is visible for every module
	# which uses the config file. The constructor will check if the file is not yet
	# loaded and will raise a RuntimeError if this is the case!
	def __init__(self, module):
		global configLoaders

		if not isinstance(module, str):
			raise Exception("Expected 'str' as type for 'module'")

		if module in configLoaders:
			raise RuntimeError("The config file for \"{0}\" is already loaded!".format(module))

		basedir = "/etc/kam"

		if not os.path.exists(basedir):
			os.mkdir(basedir)

		if not os.path.isdir(basedir):
			raise RuntimeError("Expected \"{0}\" to be a directory".format(basedir))

		if module != ConfigLoader.GENERAL:
			basedir = os.path.join(basedir, "module")

			if not os.path.exists(basedir):
				os.mkdir(basedir)

			if not os.path.isdir(basedir):
				raise RuntimeError("Expected \"{0}\" to be a directory".format(basedir))

		self._filepath = os.path.join(basedir, module + ".conf")

		self.reload()
		self._listeners = []

	## Read the config file again
	def reload(self):
		self._confObj = configparser.SafeConfigParser()

		if os.path.isfile(self._filepath):
			self._confObj.read(self._filepath)

		self._isChanged = False

	## store the current config file if changed
	def store(self):
		if self._isChanged:
			with open(self._filepath, "w") as f:
				self._confObj.write(f)

		self._isChanged = False


	## Get a value from an option in a section
	#
	# @param section The section
	# @param option The option
	# @return None if the section or option does not exist
	# @returns A the value if the section and option exist in the config file
	def get(self, section, option):
		ret = None

		if self._confObj.has_section(section) and self._confObj.has_option(section, option):
			ret = self._confObj.get(section, option)

		return ret

	## Return all sections in the config file
	def getSections(self):
		return self._confObj.sections()

	## Return all options in a section
	#
	# @return None If the section does not exist
	# @return list If the section exists
	def getOptions(self, section):
		ret = None

		if self._confObj.has_section(section):
			ret = self._confObj.options(section)

		return ret

	## Set the value for an option
	#
	# If the section and or option does not yet exist, they are created.
	# If the value is None, then the option is removed. If no options are left in the
	# section, the section is also removed
	#
	# @param section The section
	# @param option The option
	# @param value The value we should assign to the option. Can be an empty string. None will remove the option
	def set(self, section, option, value):
		changed = False

		if value is None:
			if self._confObj.has_section(section) and self._confObj.has_option(section, option):
				self._confObj.remove_option(section, option)
				changed = True

			if self._confObj.has_section(section) and len(self._confObj.options(section)) == 0:
				self._confObj.remove_section(section)
				changed = True
		else:
			if not self._confObj.has_section(section):
				self._confObj.add_section(section)

			if not (self._confObj.has_option(section, option) and \
			   (self._confObj.get(section, option) == str(value))):
				self._confObj.set(section, option, value)
				changed = True

		self._isChanged |= changed

		if changed:
			for listener in self._listeners:
				listener()

	## Returns if the config file is changed
	def isChanged(self):
		return self._isChanged

	## Add a listener if the config file changes
	def addListener(self, callback):
		self._listeners.append(callback)

	## Remove a listener
	def removeListener(self, callback):
		self._listeners.remove(callback)


## A function to get a config loader. If the loader does not yet exist, it is created.
# Otherwise the loader is returned so every part of the application will use the same loader.
def getConfigLoader(module):
	global configLoaders

	if not (module in configLoaders):
		loader = ConfigLoader(module)
		configLoaders[module] = loader

	return configLoaders[module]

