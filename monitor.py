#!/usr/bin/python3

import os, sys
import psutil
import configparser
import subprocess
from datetime import datetime, timedelta

CNF_DIR = "/etc/pl_sys_mon"
CNF_FILE = os.path.join(CNF_DIR, "config.cnf")

LOG_FILE = "/var/log/pl_sys_monitor.log"


def log(msg):
	global LOG_FILE

	content = []	

	if os.path.exists(LOG_FILE):
		with open(LOG_FILE, "r") as log:
			for line in log:
				content.append(line.strip("\n"))

	msg = "On " + str(datetime.now()) + "\n" + msg

	new_lines = msg.split("\n")
	new_content = content + new_lines
	if len(new_content) < 200:
		print("Write {0}".format(len(new_content)))
		with open(LOG_FILE, "a") as log:
			log.write(msg)
	else:
		start = len(new_content) - 150
		print("Write {0} lines".format(len(new_content) - start))
		with open(LOG_FILE, "w") as log:
			log.write("\n".join(new_content[start:]))

if not os.path.exists(CNF_DIR):
	os.mkdir(CNF_DIR)
elif not os.path.isdir(CNF_DIR):
	log("{0} is not a directory!\n".format(CNF_DIR))
	sys.exit(1)

CNF = configparser.ConfigParser()
if os.path.isfile(CNF_FILE):
	log("Reading config file {0}\n".format(CNF_FILE))
	CNF.read(CNF_FILE)

def checkConfig(config):
	edited = False

	if not 'general' in config:
		config['general'] = {}

	if not 'cpu' in config:
		config['cpu'] = {}

	if not 'processes' in config:
		config['processes'] = {}

	if not 'network' in config:
		config['network'] = {}

	if not "idle" in config:
		config['idle'] = {}

	if not "total_load" in config['cpu']:
		if "per_cpu_load" in config['cpu']:
			config['cpu']['total_load'] = str(float(config['cpu']['per_cpu_load']) * os.cpu_count())
		else:
			config["cpu"]["total_load"] = str(10)
		edited = True

	if not "per_cpu_load" in config['cpu']:
		config['cpu']['per_cpu_load'] = str(float(config['cpu']['total_load']) / os.cpu_count())
		edited = True


	if not "period" in config['general']:
		config['general']['period'] = str(10)
		edited = True

	if not "idle_time" in config['general']:
		config['general']['idle_time'] = str(15)
		edited = True


	if not "download_speed" in config['network']:
		config['network']['download_speed'] = str(10 * 1024)
		edited = True

	if not "upload_speed" in config['network']:
		config['network']['upload_speed'] = str(10 * 1024)
		edited = True


	if not "processes" in config['processes']:
		config['processes']['processes'] = ""
		edited = True
	else:
		processes = config['processes']['processes'].split(";")
		if len(processes) > 0:
			for p in processes:
				if not (p + "_min") in config['processes']:
					config['processes'][p + "_min"] = str(1)
					edited = True

	if not "cmd" in config['idle']:
		config['idle']['cmd'] = ""
		edited = True

	if edited:
		global CNF_FILE

		log("Generating default config file {0}\n".format(CNF_FILE))
		with open(CNF_FILE, "w") as configfile:
			config.write(configfile)


def checkCpu(config):
	total_cpu_threshold = float(config['cpu'].get("total_load"))
	per_cpu_threshold = float(config['cpu'].get("per_cpu_load"))
	time_span = int(config['general'].get("period"))

	per_cpu = psutil.cpu_percent(time_span, True)
	total_cpu = 0
	per_cpu_alive = False
	for cpu in per_cpu:
		total_cpu += cpu
		if cpu >= per_cpu_threshold:
			per_cpu_alive = True

	return (total_cpu >= total_cpu_threshold or per_cpu_alive, per_cpu)

def checkNetwork(config, prev_recv, prev_send):
	dl_threshold = float(config['network'].get("download_speed", 10)) * 1024
	up_threshold = float(config['network'].get("upload_speed", 10)) * 1024
	time_span = int(config['general'].get("period", 5))

	network = psutil.net_io_counters(True)
	network_dl = 0
	network_up = 0

	for k in network:
		if k != "lo":
			network_dl += network[k].bytes_recv
			network_up += network[k].bytes_sent

	dl = (network_dl - prev_recv) / time_span
	up = (network_up - prev_send) / time_span

	return (dl >= dl_threshold and up >= up_threshold, network_dl, network_up, dl / 1024, up / 1024)

def checkProcesses(config):
	s_processes = config['processes'].get("processes", "").strip()
	if s_processes:
		tmp_processes = s_processes.split(";")
		processes = {}
		for p in tmp_processes:
			p_data = {}
			p_data['count'] = 0
			p_data['min'] = int(config['processes'].get(p.strip() + "_min", 1))
			processes[p.strip()] = p_data

		for p in psutil.process_iter():
			if p.name in processes:
				p_data = processes[p.name]
				p_data['count'] += 1
				if p_data['count'] >= p_data['min']:
					return (True, p.name, p_data) 

	return (False, None, None)

def main():
	global CNF

	shutdown = False

	checkConfig(CNF)

	idle_time = int(CNF['general'].get("idle_time", 1))
	current_shutdown_time = datetime.now() + timedelta(minutes=idle_time)

	dl = 0
	up = 0

	(_, dl, up, _, _) = checkNetwork(CNF, dl, up)

	while datetime.now() < current_shutdown_time:
		(cpu_alive, cpu) = checkCpu(CNF)
		(net_alive, dl, up, dl_speed, up_speed) = checkNetwork(CNF, dl, up)
		(process_alive, process, p_data) = checkProcesses(CNF)

		shutdown = not (cpu_alive or net_alive or process_alive)
		if not shutdown:
			current_shutdown_time = datetime.now() + timedelta(minutes=idle_time)
			msg = "Delay shutdown until {0}\n".format(current_shutdown_time)
			msg += "Checks:\n"
			msg += "  cpu [{0}]: {1}\n".format(cpu_alive, cpu)
			msg += "  network [{0}]: dl {1}, up {2}\n".format(net_alive, dl_speed, up_speed)
			msg += "  process [{0}]: {1}\n".format(process_alive, process)
			log(msg)

	cmd = CNF['idle'].get("cmd", "")
	if cmd:
		log("Executing idle command: {0}\n".format(cmd))
		subprocess.call([ "sh", "-c", cmd ])
	else:
		log("No idle command specified\n")

	log("End script\n")

if __name__ == "__main__":
	main()
