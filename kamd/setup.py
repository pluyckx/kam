from setuptools import setup, find_packages

setup(
	name = "kamd",
	version = "2.0.0",
	author = "Philip Luyckx",
	author_email = "philip.luyckx@gmail.com",
	description = ("An application that keeps the computer alive when in use"),
	license = "GPLv2",
	keywords = "kam keep alive monitor",
	url = "",
	packages = find_packages(),
	data_files = [
		("/usr/share/doc/kamd/", [ "etc/kam/settings.py", "etc/kam/version" ]), # add systemd and upstart files
		("/usr/sbin", [ "bin/kamd.py" ])
	],
	include_package_data=True,
)
