#!/bin/bash

uid=$(id -u)

if [[ $uid -ne 0 ]]
then
	echo "You must run this script as root!"
	exit 1
fi

echo "Checking if necessary packages are installed"
dpkg -S python3 2>&1 > /dev/null
if [[ $? -eq 0 ]]
then
	python_available=1
else
	python_available=0
fi

dpkg -S python3-psutil 2>&1 > /dev/null
if [[ $? -eq 0 ]]
then
	psutil_available=1
else
	psutil_available=0
fi

if [[ $python_available -eq 0 || $psutil_available -eq 0 ]]
then
	packages=""

	if [[ $python_available -eq 0 ]]
	then
		packages="$packages python3"
	fi

	if [[ $psutils_available -eq 0 ]]
	then
		packages="$packages python3-psutil"
	fi

	echo "Installing necessary packages: $packages"

	apt-get install $packages
fi

echo "Installing monitor.py to /usr/bin/kamd"
cp monitor.py /usr/sbin/kamd

echo "Installing init script to /etc/init.d"
cp kam.init /etc/init.d/kam

echo "Update rc.d"
update-rc.d kam defaults

echo "Start service"
service kam start
