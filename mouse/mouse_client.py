#!/usr/bin/python3

import dbus
import dbus.service
import dbus.mainloop.glib
import time
import evdev
from evdev import *
import logging
from logging import debug, info, warning, error
import os
import sys
from select import select
import pyudev
import re

logging.basicConfig(level=logging.DEBUG)


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
        print("Disconnected %s", dev)

    @staticmethod
    def set_leds_all(ledvalue):
        for dev in InputDevice.inputs:
            dev.set_leds(ledvalue)

    @staticmethod
    def grab(on):
        if on:
            for dev in InputDevice.inputs:
                dev.device.grab()
        else:
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
        self.state = [0, 0, 0, 0]
        self.x = 0
        self.y = 0
        self.z = 0
        self.change = False
        self.last = 0
        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object(
            'org.thanhle.btkbservice', '/org/thanhle/btkbservice')
        self.iface = dbus.Interface(self.btkservice, 'org.thanhle.btkbservice')
        self.mouse_delay = 20 / 1000
        self.mouse_speed = 1

    def send_current(self, ir):
        try:
            self.iface.send_mouse(0, bytes(ir))
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
            self.state[1] = min(127, max(-127, int(self.x * speed))) & 255
            self.state[2] = min(127, max(-127, int(self.y * speed))) & 255
            self.state[3] = min(127, max(-127, self.z)) & 255
            self.x = 0
            self.y = 0
            self.z = 0
            self.change = False
            self.send_current(self.state)
        if event.type == ecodes.EV_KEY:
            debug("Key event %s %d", ecodes.BTN[event.code], event.value)
            self.change = True
            if event.code >= 272 and event.code <= 276 and event.value < 2:
                button_no = event.code - 272
                if event.value == 1:
                    self.state[0] |= 1 << button_no
                else:
                    self.state[0] &= ~(1 << button_no)
        if event.type == ecodes.EV_REL:
            if event.code == 0:
                self.x += event.value
            if event.code == 1:
                self.y += event.value
            if event.code == 8:
                self.z += event.value

    def get_info(self):
        print("hello")

    def set_leds(self, ledvalue):
        pass


if __name__ == "__main__":
    InputDevice.init()
    while True:
        desctiptors = [*InputDevice.inputs, InputDevice.monitor]
        r = select(desctiptors, [], [])
        for i in InputDevice.inputs:
            try:
                for event in i.device.read():
                    i.change_state(event)
            except OSError as err:
                warning(err)
