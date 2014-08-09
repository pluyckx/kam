

from modules.plugins.checks.basecheck import BaseCheck

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

		alive = False

		for addr in self._addresses:
			for connection in connections:
				if addr.isIpInNetwork(connection):
					self._alive()
					alive = (addr, connection)
					break
			
			if alive:
				break

		if not alive:
			self._dead()

		if self._debug:
			self._debug.log("[NetworkConnections] Found addresses: {0}\n".format(connections))
			if alive:
				self._debug.log("[NetworkConnection] {0} in {1} --> {2}\n".format(alive[1], alive[0], True))
			else:
				self._debug.log("[NetworkConnection] No addresses in {0}\n".format(self._addresses))


	def loadConfig(self, config):
		self._addresses = []

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
		except KeyError:
			pass

		if len(self._addresses) > 0:
			self._enable()
		else:
			self._disable()

		if self._log:
			self._log.log("[NetworkConnections] Config loaded: enabled={0}; addresses={1}\n".format(self.isEnabled(), self._addresses))


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

