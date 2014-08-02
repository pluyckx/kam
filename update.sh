#!/bin/bash

uid=$(id -u)

if [[ $uid -ne 0 ]]
then
        echo "You must run this script as root!"
        exit 1
fi

service kam stop
cp version /etc/kam/version
cp kam.init /etc/init.d/kam
cp monitor.py /usr/sbin/kamd

chmod +x /etc/init.d/kam

service kam start
