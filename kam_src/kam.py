#!/usr/bin/python3

import os, sys, importlib
import configparser
import traceback
import time
import subprocess

import utils.utils as utils

from modules.plugins.log.filelog import FileLog
from modules.exceptions.exceptions import KamFunctionNotImplemented

#CNF_DIR = "/etc/kam/"
CNF_DIR = "/tmp/"
CNF_FILE = os.path.join(CNF_DIR, "kam.conf")

if not os.path.exists(CNF_DIR):
	os.mkdir(CNF_DIR)
elif not os.path.isdir(CNF_DIR):
	print("{0} is not a directory!\n".format(CNF_DIR))
	sys.exit(1)

CNF = configparser.ConfigParser()

if os.path.isfile(CNF_FILE):
	CNF.read(CNF_FILE)

log = FileLog(CNF, "log")

is_debug_enabled = utils.toBool(CNF["global"].get("debug"))
try:
	period = int(CNF["global"].get("period"))
	idle_time = int(CNF["global"].get("idle_time"))
except Exception as ex:
	log.log(traceback.format_exc())
	raise ex

if is_debug_enabled:
	debug = FileLog(CNF, "debug", log)
else:
	debug = None

try:
	cmd = CNF["global"].get("idle_command")
except:
	cmd = None

checks = []
check_plugins_path = "modules/plugins/checks/"
check_plugins_import_path = check_plugins_path.replace("/", ".") + "{0}"
dirs = os.listdir(check_plugins_path)
for d in dirs:
	if d[-3:] == ".py" and d != "__init__.py":
		f = d[:-3]
		import_path = check_plugins_import_path.format(f)
		print("importing {0}".format(import_path))
		module = importlib.import_module(import_path)
		if hasattr(module, "createInstance"):
			checks.append(module.createInstance(CNF, log, debug))

def check():
	for c in checks:
		c.check()

def isAlive():
	for c in checks:
		if c.isAlive():
			return True
	return False

def main():
	idle = time.clock_gettime(time.CLOCK_MONOTONIC) + idle_time * 60
	log.log("[main] It is now {0} seconds, idle time set to {1}\n".format(time.clock_gettime(time.CLOCK_MONOTONIC), idle))
	while True:
		last_check = time.clock_gettime(time.CLOCK_MONOTONIC)
		check()

		now = time.clock_gettime(time.CLOCK_MONOTONIC)

		if isAlive():
			idle = now + idle_time * 60
			log.log("[main] It is now {0} seconds, idle time set to {1}\n".format(now, idle))
		elif debug:
			debug.log("[main] server is dead. It is now {0} seconds, idle time is set to {1}. diff = {2}\n".format(now, idle, (idle - now)))

		if now >= idle and cmd:
			os.system(cmd)

		time_to_sleep = period - (now - last_check)

		time.sleep(time_to_sleep)

if __name__ == "__main__":
	try:
#		pid = os.fork()
#		if pid > 0:
#			sys.exit(0) # we are the first run, we must exit

		main()
	except OSError as e:
		log.log("Fork failed! {0}".format(str(e)))
		sys.exit(1)

