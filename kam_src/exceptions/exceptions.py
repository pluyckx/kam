
class KamException(Exception):
	def __init__(self, msg):
		self._msg = msg

	def __str__(self):
		return self._msg

class KamFunctionNotImplemented(KamException):
	def __init__(self, msg):
		super().__init__(msg)

