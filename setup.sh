sudo apt-get install python-gobject bluez bluez-tools
sudo apt-get install bluez-firmware python-bluez python-dev python-pip -y
sudo pip install evdev
sudo apt install git python3-dbus python3-pyudev python3-evdev
sudo apt-get install python-dbus  -y
sudo apt-get install python-gtk2 -y
sudo apt-get install git-core -y
sudo apt-get install tmux -y
sudo cp dbus/org.yaptb.btkbservice.conf /etc/dbus-1/system.d
sudo cp /lib/systemd/system/bluetooth.service ./bluetooth.service.bk
sudo cp bluetooth.service /lib/systemd/system/bluetooth.service
