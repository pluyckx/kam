#!/usr/bin/python3

import os, sys, importlib
import configparser
import traceback
import time
import subprocess

import utils.utils as utils

from modules.plugins.log.logmanager import LogManager
from modules.plugins.debugger.debugmanager import DebugManager
from modules.exceptions.exceptions import KamFunctionNotImplemented

from modules.plugins.core.periodsleep import PeriodSleep
from modules.plugins.core.idlecommand import IdleCommand

# Move to the directory where this file is lcoated
# We are using dynamic importing and it works relative to the
# current working directory
# When running this script through a symlink, the CWD is wrong and we must
# correct it. This line will correct the CWD
os.chdir(os.path.dirname(os.path.realpath(__file__)))

checks = []
logmanager = LogManager()
debugmanager = DebugManager()
CNF = configparser.ConfigParser()

def getChecks():
	return checks

def getLogs():
	return logmanager

def getDebuggers():
	return debugmanager

def getConfig():
	return CNF

data_callbacks = {}
data_callbacks["checks"] = getChecks
data_callbacks["logs"] = getLogs
data_callbacks["debuggers"] = getDebuggers
data_callbacks["config"] = getConfig

# Load all modules from a path
# The modules must contain the function createInstance
def loadModules(path):
	# The following code will dynamically load all check plugins
	instances = []
	import_path = path.replace("/", ".") + "{0}"
	dirs = os.listdir(path)
	for d in dirs:
		if d[-3:] == ".py" and d != "__init__.py":
			f = d[:-3]
			imp = import_path.format(f)
			logmanager.log("Main", "importing {0}\n".format(imp))
			module = importlib.import_module(imp)
			if hasattr(module, "createInstance"):
				instances.append(module.createInstance(data_callbacks))

	return instances

# Some paths we will use later in the script
CNF_DIR = "/etc/kam/"
CNF_FILE = os.path.join(CNF_DIR, "kam.conf")

if os.path.isfile(CNF_FILE):
	CNF.read(CNF_FILE)

# load the log modules
logs = loadModules("modules/plugins/log/")
for log in logs:
	logmanager.add(log)

# load the debug modules
debuggers = loadModules("modules/plugins/debugger/")
for debugger in debuggers:
	debugmanager.add(debugger)

# load the core modules
core = loadModules("modules/plugins/core/")

# For now we must remove some core modules form the list and assign them to a
# specific variable, so we can call them in the right order.
# TODO add a system so the core modules are ordered and we just can itterate
# the list

period_sleep = None
idle_command = None
for core_module in core:
	if isinstance(core_module, PeriodSleep):
		period_sleep = core_module
	elif isinstance(core_module, IdleCommand):
		idle_command = core_module
		

if period_sleep:
	core.remove(period_sleep)
if idle_command:
	core.remove(idle_command)

# load all check modules
checks_tmp = loadModules("modules/plugins/checks/")

for check in checks_tmp:
	logmanager.log("Main", "Add check to list: {0}".format(check.__class__.__name__))
	checks.append(check)

# The main function which normally never stops, unless an exception occurs
def main():
	try:
		while True:
			for check in checks:
				logmanager.log("Main", "Checking {0}".format(check.__class__.__name__))
				check.check()

			idle_command.execute()
			period_sleep.execute()

	except Exception as ex:
		logmanager.log("Main", traceback.format_exc())
		raise ex

if __name__ == "__main__":
	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0) # we are the first run, we must exit

		main()
	except OSError as e:
		logmanager.log("Main", "Fork failed! {0}".format(str(e)))
		sys.exit(1)

