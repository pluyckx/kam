
import re

## Convert a text to a size.
#
# This function accepts units like B, kB, kiB, MB, MiB etc up to T(i)B. If no
# unit is used, B is default.
#
# \param txt A size as string
# \return (converted, number, unit) A tuple of the converted value to bytes, the non converted number and the unit.
#          If converted is None, this means the unit is unknown. When txt is an empty string, (0, 0, "B") is returned
def getTextAsSize(txt):
	regexp = "^([0-9]+)[ ]*([a-zA-Z]*)$"
	ret = 0
	number = 0
	unit = "B"

	txt = txt.strip()

	if len(txt) > 0:
		res = re.search(regexp, txt)

		number = int(res.group(1))
		unit = res.group(2)

		ret = convertSize(number, unit)

	return (ret, number, unit)

def convertSize(number, unit="B"):
	ret = number

	if unit == "kB":
		ret *= 1000
	elif unit == "kiB":
		ret *= 1024
	elif unit == "MB":
		ret *= 1000 * 1000
	elif unit == "MiB":
		ret *= 1024 * 1024
	elif unit == "GB":
		ret *= 1000 * 1000 * 1000
	elif unit == "GiB":
		ret *= 1024 * 1024 * 1024
	elif unit == "TB":
		ret *= 1000 * 1000 * 1000 * 1000
	elif unit == "TiB":
		ret *= 1024 * 1024 * 1024 * 1024
	elif (len(unit) > 0) and (unit != "B"):
		ret = None

	return ret
