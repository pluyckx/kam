

from modules.plugins.checks.basecheck import BaseCheck
from modules.plugins.log.debuglog import DebugLog

import re, subprocess

class NetworkConnectionsCheck(BaseCheck):
	CONFIG_NAME = "network"
	CONFIG_ITEM_CONNECTIONS = "connections"

	def __init__(self, config, log, debug=None):
		super().__init__()
		self._log = log
		self._debug = debug
		self.loadConfig(config)

	def _run(self):
		netstat_out = subprocess.getoutput("netstat --inet -a | grep ESTABLISHED | awk '{print $5}'")
		connections = netstat_out.split("\n")

		for i in range(0, len(connections)):
			connections[i] = connections[i][:connections[i].find(":")]

		alive = []

		for addr in self._addresses:
			for connection in connections:
				if addr.isIpInNetwork(connection):
					self._alive()
					alive.append((addr, connection))
					if not self._debug:
						break
			
			if not self._debug and len(alive) > 0:
				break

		if len(alive) == 0:
			self._dead()
		else:
			self._alive()

		if self._debug:
                        self._debug.log(DebugLog.TYPE_CHECK, self,\
			                self.CONFIG_ITEM_CONNECTIONS,\
			                alive, "", self.isAlive())


	def loadConfig(self, config):
		self._addresses = []
		err_value = ""

		try:
			addresses = config[self.CONFIG_NAME].get(self.CONFIG_ITEM_CONNECTIONS)

			if addresses:
				addresses = addresses.split(",")
				for address in addresses:
					try:
						addr = NetworkAddress(address)
						self._addresses.append(addr)
					except Exception as ex:
						log.log(str(ex) + "\n")
						err_value += str(s) + ";"
		except KeyError as e:
			err_value += str(e) + ";"

		if len(self._addresses) > 0:
			self._enable()
		else:
			self._disable()

		if self._log:
			self._log.log(self, "Config loaded: enabled={0}; addresses={1}\n".format(self.isEnabled(), self._addresses))

		if self._debug:
                        self._debug.log(DebugLog.TYPE_CONFIG, self,\
			                self.CONFIG_ITEM_CONNECTIONS,\
			                self._addresses, err_value, "")


class NetworkAddress:
	def __init__(self, ip):
		ip = ip.strip()
		slash_pos = ip.find("/")

		if slash_pos == -1:
			raise ValueError("No slash found in network address! Format = a.b.c.d/subnet")

		subnet = ip[slash_pos+1:]

		self._s_ip = ip[:slash_pos]
		self._ip = self._ipToInt(self._s_ip)
		self._subnet = int(subnet)
		self._netmask = 0xFFFFFFFF << (32 - self._subnet)
		self._ip_masked = self._ip & self._netmask

	def getIp(self):
		return self._ip

	def getStrIp(self):
		return self._s_ip

	def getNetmask(self):
		return self._subnet

	def isIpInNetwork(self, s_ip):
		ip = self._ipToInt(s_ip)
		return (ip & self._netmask) == self._ip_masked
		
	def _ipToInt(self, ip):
		pattern = "^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$"

		match = re.search(pattern, ip)
		if match:
			return (int(match.group(1)) << 24) | (int(match.group(2)) << 16) | (int(match.group(3)) << 8) | int(match.group(4))
		else:
			return 0

	def __str__(self):
		return "{0}/{1}".format(self._s_ip, self._subnet)

	def __repr__(self):
		return str(self)

def createInstance(config, log, debug = None):
	return NetworkConnectionsCheck(config, log, debug)
