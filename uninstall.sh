#!/bin/bash

if [ -f "bluetooth.service.bk" ] ; then
    sudo cp  bluetooth.service.bk /lib/systemd/system/bluetooth.service
    sudo systemctl daemon-reload
    sudo /etc/init.d/bluetooth start
fi