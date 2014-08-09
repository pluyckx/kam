#!/usr/bin/python3

import os, sys
import configparser
import time

from modules.log.log import Log
from exceptions.exceptions import KamFunctionNotImplemented
from modules.checkplugins.processor import ProcessorCheck
from modules.checkplugins.networkspeed import NetworkSpeedCheck
from modules.checkplugins.networkconnections import NetworkConnectionsCheck
from modules.checkplugins.processes import ProcessesCheck

def show():
	print("processor={0}\nnetwork={1}\nconnections={2}\nprocesses={3}\n".format(processor.isKeepAlive(), networkspeed.isKeepAlive(), networkconnection.isKeepAlive(), processes.isKeepAlive()))


log = Log("/tmp/test.log")
debug = Log("/tmp/test.debug")

CNF_DIR = "/tmp"
CNF_FILE = os.path.join(CNF_DIR, "kam.ini")

if not os.path.exists(CNF_DIR):
	os.mkdir(CNF_DIR)
elif not os.path.isdir(CNF_DIR):
	log.log("{0} is not a directory!\n".format(CNF_DIR))
	sys.exit(1)

CNF = configparser.ConfigParser()

if os.path.isfile(CNF_FILE):
	CNF.read(CNF_FILE)

processor = ProcessorCheck(CNF, debug)
networkspeed = NetworkSpeedCheck(CNF, debug)
networkconnection = NetworkConnectionsCheck(CNF, log, debug)
processes = ProcessesCheck(CNF, log, debug)


processor.check()
networkspeed.check()
networkconnection.check()
processes.check()
show()
time.sleep(5)
processor.check()
networkspeed.check()
networkconnection.check()
processes.check()
show()

for i in range(0, 100000000):
	pass

processor.check()
networkspeed.check()
networkconnection.check()
processes.check()
show()

