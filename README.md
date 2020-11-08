My fork of this project to add a keyboard and mouse emulator to a Raspberry Pi. This fork includes a script designed to open an app or run a shortcut when the keyboard is connected to an iOS device by:

1. Inputting the device passcode (passed as argument 1 to the script).
2. Simulating command+space to open the search window.
3. Inputting a string (passed as argument 2 to the script).
4. Simulating enter to execute.

Thanh Le's original instructions follow.

===

[![Build Status](https://travis-ci.com/quangthanh010290/keyboard_mouse_emulate_on_raspberry.svg?branch=master)](https://travis-ci.com/quangthanh010290/keyboard_mouse_emulate_on_raspberry)

# Make things work first 

## Step 1: Setup 

```
 sudo ./setup.sh
```
 
 
## Step 2: Run the Server

```
sudo ./boot.sh
```


## Step 3.1: Run Keyboard Client (using physical keyboard)

- Need a physical keyboard connected to raspberry PI board

```
./keyboard/kb_client.py
```

## Step 3.2: Run Keyboard Client (no need physical keyboard, send string through dbus)

- Dont need a physical keyboard connected to raspberry PI board

```
./keyboard/send_string.py "hello client, I'm a keyboard"
```

## Step 3.3: Run mouse client (using physical mouse)

- Need a physical mouse connected to raspberry PI board
```
./mouse/mouse_client.py
```

## Step 3.4: Run Mouse client (no need physical mouse, string mouse data through dbus)

- Dont need a physical mouse connected to raspberry PI board
```
./mouse/mouse_emulate.py 0 10 0 0
```

# To understand what I'm doing in the background 
[Make Raspberry Pi3 as an emulator bluetooth keyboard](https://thanhle.me/make-raspberry-pi3-as-an-emulator-bluetooth-keyboard/)

## Keyboard setup demo (old version)

 [![ScreenShot](https://i0.wp.com/thanhle.me/wp-content/uploads/2020/02/bluetooth_mouse_emulate_on_ra%CC%81pberry.jpg)](https://www.youtube.com/watch?v=fFpIvjS4AXs)

## Mouse setup demo (ongoing)
[Emulate Bluetooth mouse with Raspberry Pi](https://thanhle.me/emulate-bluetooth-mouse-with-raspberry-pi/)
[![ScreenShot](https://i0.wp.com/thanhle.me/wp-content/uploads/2020/08/bluetooth_mouse_emulation_on_raspberry.jpg)](https://www.youtube.com/watch?v=fFpIvjS4AXs)
