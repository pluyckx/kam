#!/usr/bin/python3

import os, sys
import configparser
import time

from modules.log.log import Log
from exceptions.exceptions import KamFunctionNotImplemented
from modules.checkplugins.processor import ProcessorCheck

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

processor.check()
print(processor.isKeepAlive())
time.sleep(5)
processor.check()
print(processor.isKeepAlive())

for i in range(0, 100000000):
	pass

processor.check()
print(processor.isKeepAlive())
