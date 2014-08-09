#!/bin/sh

uid=$(id -u)

if [ $uid -ne 0 ]
then
	echo "You must run this script as root!"
	exit 1
fi

echo "Checking if necessary packages are installed"
dpkg -S python3 2>&1 > /dev/null
if [ $? -eq 0 ]
then
	python_available=1
else
	python_available=0
fi

dpkg -S python3-psutil 2>&1 > /dev/null
if [ $? -eq 0 ]
then
	psutil_available=1
else
	psutil_available=0
fi

if [ $python_available -eq 0 || $psutil_available -eq 0 ]
then
	packages=""

	if [ $python_available -eq 0 ]
	then
		packages="$packages python3"
	fi

	if [ $psutils_available -eq 0 ]
	then
		packages="$packages python3-psutil"
	fi

	echo "Installing necessary packages: $packages"

	apt-get install $packages
fi

echo "Installing kam to /usr/lib/kam"
echo "Creating directory /usr/lib/kam"
mkdir /usr/lib/kam

echo "Copying necesarry files to /usr/lib/kam"
cp -r kam_src/* /usr/lib/kam

echo "Creating link from /usr/bin/kam to /usr/lib/kam/kam.py"
ln -s /usr/lib/kam/kam.py /usr/bin/kam

echo "Installing init script to /etc/init.d"
cp kam.init /etc/init.d/kam

echo "Update rc.d"
update-rc.d kam defaults

echo "Start service"
service kam start
