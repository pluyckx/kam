#!/usr/bin/python3

import sys, os

missing = []

try:
  import psutil
except:
  missing.append("psutil")


if len(missing) > 0:
  print("Please install the following packages for python3 first:")
  print(", ".join(missing))
  sys.exit(1)

from distutils.core import setup

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
	
packages = []
package_dir = {}
find_packages("kam", packages, package_dir)

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
      data_files=[("/etc/kam", ["kam.conf", "version"])]
)
