

def toBool(value):
	if isinstance(value, str):
		try:
			s_as_int = int(value)
		except:
			s_as_int = None

		true_list = [ "true", "True", "yes", "Yes" ]
		false_list = [ "false", "False", "no", "No" ]

		if value in true_list or (s_as_int != None and s_as_int):
			return True
		elif value in false_list or (s_as_int != None and not s_as_int):
			return False
	elif isinstance(value, int):
		return value != 0
	elif isinstance(value, float):
		return value != 0.0
	else:
		return False
