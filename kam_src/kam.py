#!/usr/bin/python3

import os, sys
import configparser
import traceback
import time
import subprocess

import utils.utils as utils

from modules.plugins.log.filelog import FileLog
from modules.exceptions.exceptions import KamFunctionNotImplemented
from modules.plugins.checks.processor import ProcessorCheck
from modules.plugins.checks.networkspeed import NetworkSpeedCheck
from modules.plugins.checks.networkconnections import NetworkConnectionsCheck
from modules.plugins.checks.processes import ProcessesCheck
from modules.plugins.checks.kick import KickCheck

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

processor = ProcessorCheck(CNF, log, debug)
networkspeed = NetworkSpeedCheck(CNF, log, debug)
networkconnection = NetworkConnectionsCheck(CNF, log, debug)
processes = ProcessesCheck(CNF, log, debug)
kick = KickCheck(CNF, log, debug)

checks = [ processor, networkspeed, networkconnection, processes, kick ]

def check():
	processor.check()
	networkspeed.check()
	networkconnection.check()
	processes.check()
	kick.check()

def isAlive():
	return processor.isAlive() or networkspeed.isAlive() or networkconnection.isAlive() or processes.isAlive() or kick.isAlive()

def show():
	print("processor={0}\nnetworkspeed={1}\nnetworkconnection={2}\nprocesses={3}\nkick={4}\n".format(processor.isAlive(), networkspeed.isAlive(), networkconnection.isAlive(), processes.isAlive(), kick.isAlive()))

idle = time.clock_gettime(time.CLOCK_MONOTONIC) + idle_time * 60
log.log("[main] It is now {0} seconds, idle time set to {1}\n".format(time.clock_gettime(time.CLOCK_MONOTONIC), idle))
while True:
	last_check = time.clock_gettime(time.CLOCK_MONOTONIC)
	check()
	show()

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
