#!/usr/bin/python3
#
# YAPTB Bluetooth keyboard emulation service
# keyboard copy client.
# Reads local key events and forwards them to the btk_server DBUS service
#
# Adapted from www.linuxuser.co.uk/tutorials/emulate-a-bluetooth-keyboard-with-the-raspberry-pi
#
#
import os  # used to all external commands
import sys  # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import evdev  # used to get input from the keyboard
from evdev import *
import pyudev
import re
import logging
from logging import debug, info, warning, error
import errno
import os
import sys
import dbus
import time
import evdev
from evdev import ecodes
from select import select
import logging
from logging import debug, info, warning, error
import pyudev
import re
import functools
import errno
import socket
from configparser import ConfigParser

logging.basicConfig(level=logging.DEBUG)

class BluetoothDevice:
    by_index = {}
    by_addr = {}
    current = 0
    connecting_sockets = []
    mouse_delay = 20 / 1000
    mouse_speed = 1

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object(
            'org.yaptb.btkbservice', '/org/yaptb/btkbservice')
        self.iface = self.bus.Interface(btkservice, 'org.yaptb.btkbservice')
        self.mouse_delay = 20 / 1000
        self.mouse_speed = 1

    def __str__(self):
        return "%s%d: %s %s" % ('*' if BluetoothDevice.current == self.index else ' ', self.index, self.addr, self.state)

    def send_input(self, ir):
        try:
            print("send")
            self.iface.send(0, bytes(ir))
        except OSError as err:
            error(err)

    @staticmethod
    def mouse_delay():
        return BluetoothDevice.mouse_delay

    @staticmethod
    def mouse_speed():
        return BluetoothDevice.mouse_speed

    @staticmethod
    def send_current(ir):
        BluetoothDevice.send_input(0, ir)

    @staticmethod
    def set_current():
        BluetoothDevice.send_input([0xA2, 2, 0, 0, 0, 0])


class InputDevice():
    inputs = []

    @staticmethod
    def init():
        context = pyudev.Context()
        devs = context.list_devices(subsystem="input")
        InputDevice.monitor = pyudev.Monitor.from_netlink(context)
        InputDevice.monitor.filter_by(subsystem='input')
        InputDevice.monitor.start()
        for d in [*devs]:
            InputDevice.add_device(d)

    @staticmethod
    def add_device(dev):
        if dev.device_node == None or not re.match(".*/event\\d+", dev.device_node):
            return
        try:
            if "ID_INPUT_MOUSE" in dev.properties:
                print("detected mouse: " + dev.device_node)
                InputDevice.inputs.append(MouseInput(dev.device_node))
        except OSError:
            error("Failed to connect to %s", dev.device_node)

    @staticmethod
    def remove_device(dev):
        if dev.device_node == None or not re.match(".*/event\\d+", dev.device_node):
            return
        InputDevice.inputs = list(
            filter(lambda i: i.device_node != dev.device_node, InputDevice.inputs))
        info("Disconnected %s", dev)

    @staticmethod
    def set_leds_all(ledvalue):
        for dev in InputDevice.inputs:
            dev.set_leds(ledvalue)

    @staticmethod
    def grab(on):
        if on:
            debug("Grabbing all input devices")
            for dev in InputDevice.inputs:
                dev.device.grab()
        else:
            debug("Releasing all input devices")
            for dev in InputDevice.inputs:
                dev.device.ungrab()

    def __init__(self, device_node):
        self.device_node = device_node
        self.device = evdev.InputDevice(device_node)
        self.device.grab()
        info("Connected %s", self)

    def fileno(self):
        return self.device.fd

    def __str__(self):
        return "%s@%s (%s)" % (self.__class__.__name__, self.device_node, self.device.name)


class MouseInput(InputDevice):
    def __init__(self, device_node):
        super().__init__(device_node)
        self.state = [0xA1, 2, 0, 0, 0, 0]
        self.x = 0
        self.y = 0
        self.z = 0
        self.change = False
        self.last = 0

    def send_current(self, ir):
        try:
            print("send")
            self.iface.send(0, bytes(ir))
        except OSError as err:
            error(err)
    def change_state(self, event):
        if event.type == ecodes.EV_SYN:
            current = time.monotonic()
            diff = 20/1000
            if current - self.last < diff and not self.change:
                return
            self.last = current
            speed = 1
            self.state[3] = min(127, max(-127, int(self.x * speed))) & 255
            self.state[4] = min(127, max(-127, int(self.y * speed))) & 255
            self.state[5] = min(127, max(-127, self.z)) & 255
            self.x = 0
            self.y = 0
            self.z = 0
            self.change = False
            BluetoothDevice.send_current(self.state)
        if event.type == ecodes.EV_KEY:
            debug("Key event %s %d", ecodes.BTN[event.code], event.value)
            self.change = True
            if event.code >= 272 and event.code <= 276 and event.value < 2:
                button_no = event.code - 272
                if event.value == 1:
                    self.state[2] |= 1 << button_no
                else:
                    self.state[2] &= ~(1 << button_no)
        if event.type == ecodes.EV_REL:
            if event.code == 0:
                self.x += event.value
            if event.code == 1:
                self.y += event.value
            if event.code == 8:
                self.z += event.value

    def set_leds(self, ledvalue):
        pass


def event_loop():
    while True:
        for i in InputDevice.inputs:
            try:
                for event in i.device.read():
                    i.change_state(event)
            except OSError as err:
                if err.errno == errno.ENODEV:
                    InputDevice.remove_device(i)
                    warning(err)


if __name__ == "__main__":
    state = [0xA1, 2, 0, 0, 0, 0]
    x = 0
    y = 0
    z = 0
    change = False
    last = 0
    bus = dbus.SystemBus()
    btkservice = bus.get_object(
        'org.yaptb.btkbservice', '/org/yaptb/btkbservice')
    iface = bus.Interface(btkservice, 'org.yaptb.btkbservice')
    mouse_delay = 20 / 1000
    mouse_speed = 1
    context = pyudev.Context()
    devs = context.list_devices(subsystem="input")
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='input')
    monitor.start()
    for dev in [*devs]:
        if dev.device_node == None or not re.match(".*/event\\d+", dev.device_node):
            continue
        try:
            if "ID_INPUT_MOUSE" in dev.properties:

        except OSError:
            error("Failed to connect to %s", dev.device_node)
