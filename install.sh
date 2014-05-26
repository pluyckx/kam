#!/bin/bash

uid=$(id -u)

if [[ $uid -ne 0 ]]
then
	echo "You must run this script as root!"
	exit 1
fi

cp monitor.py /usr/sbin/kamd
cp kam /etc/init.d/

update-rc.d kam defaults
service kam start
