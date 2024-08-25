#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y git tmux bluez bluez-tools bluez-firmware
sudo apt-get install -y python3 python3-dev python3-pip python3-dbus python3-pyudev python3-evdev python3-gi

sudo apt-get install -y libbluetooth-dev
sudo pip3 install PyBluez

sudo cp dbus/org.thanhle.btkbservice.conf /etc/dbus-1/system.d

sudo cp /lib/systemd/system/bluetooth.service ./bluetooth.service.bk
sudo cp bluetooth.service /lib/systemd/system/bluetooth.service
sudo systemctl daemon-reload
sudo /etc/init.d/bluetooth start
