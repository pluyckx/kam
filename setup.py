#!/usr/bin/python3

import sys, os, shutil
from distutils.core import setup, Command
from distutils.command.install import install
import subprocess

class UpdateInit(install):
	def run(self):
		if os.path.exists("/etc/kam/kam.conf"):
			shutil.copyfile("/etc/kam/kam.conf", "/etc/kam/kam.conf.back")

		if not os.path.exists("/etc/kam"):
			os.mkdir("/etc/kam")

		shutil.copyfile("kam.conf", "/etc/kam/kam.conf")
		shutil.copyfile("version", "/etc/kam/version")

		super().run()

		if has_bin("update-rc.d"):
			print("Update-rc.d")
			subprocess.call(["update-rc.d", "kam", "defaults"])

		if has_bin("systemctl"):
			print("Update systemd")
			subprocess.call(["systemctl", "enable", "kam.service"])


def check_version():
	(major, minor, _, _, _) = sys.version_info

	if major != 3:
		print("This script needs python3!")
		sys.exit(1)


def check_psutil():
	missing = []

	try:
		import psutil
	except:
		missing.append("psutil")


	if len(missing) > 0:
		print("Please install the following packages for python3 first:")
		print(", ".join(missing))
		sys.exit(1)

def find_packages(relative_dir, packages, package_dir):
	abs_dir = os.path.abspath(relative_dir)
	init_file = os.path.join(abs_dir, "__init__.py")
	if os.path.isfile(init_file):
		packages.append(relative_dir)
		package_dir[relative_dir.replace("/", ".")] = relative_dir

	for f in os.listdir(abs_dir):
		if os.path.isdir(os.path.join(abs_dir, f)):
			print("checking {0}".format(f))
			find_packages(os.path.join(relative_dir, f), packages, package_dir)

def has_bin(bin_name):
	ret = subprocess.call(["locate", bin_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	
	return True if ret == 0 else False


def main():
	check_version()
	check_psutil()

	packages = []
	package_dir = {}
	find_packages("kam", packages, package_dir)

	install = UpdateInit

	setup(name="kam",
	      version="1.0.0",
	      description="Keep the machine alive on activity",
	      url="http://github.com/pluyckx/kam",
	      author="Philip Luyckx",
	      author_email="philip.luyckx+kam@gmail.com",
	      license="GPLV2",
	      packages=packages,
	      package_dir=package_dir,
	      scripts=["kam/bin/kamd"],
	      data_files=[
	                  ("/etc/kam", ["kam.conf", "version"]),
	                  ("/etc/init.d", ["kam/init/kam"]),
	                  ("/lib/systemd/system", ["kam/init/kam.service"])
	      ],
	      cmdclass = { 'install': install }
	)

if __name__ == "__main__":
	main()
	sys.exit(0)
