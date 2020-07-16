[![Build Status](https://travis-ci.com/quangthanh010290/keyboard_mouse_emulate_on_raspberry.svg?branch=master)](https://travis-ci.com/quangthanh010290/keyboard_mouse_emulate_on_raspberry)

# Make things work first 

## Step 1: Setup 

 sudo ./setup.sh
 
## Step 2: Run the Server

sudo ./boot.sh

## Step 3.1: Run Keyboard Client (using physical keyboard)

./keyboard/kb_client.py

## Step 3.2: Run Keyboard Client (no need physical keyboard, send string through dbus)

./keyboard/send_string.py "hello client, I'm a keyboard"

## Step 3.3: Run mouse client (using physical moude)

./mouse/mouse_client.py

## Step 3.4: Run Mouse client (no need physical mouse, string mouse data through dbus)

./mouse/mouse_emulate.py 0 10 0 0

# To understand what I'm doing in the background 
[Make Raspberry Pi3 as an emulator bluetooth keyboard](https://thanhle.me/make-raspberry-pi3-as-an-emulator-bluetooth-keyboard/)

## Video Demo

 [![ScreenShot](https://i0.wp.com/thanhle.me/wp-content/uploads/2020/02/bluetooth_mouse_emulate_on_ra%CC%81pberry.jpg)](https://www.youtube.com/watch?v=fFpIvjS4AXs)
 
 <a href="http://www.youtube.com/watch?feature=player_embedded&v=fFpIvjS4AXs
" target="_blank"><img src="http://img.youtube.com/vi/fFpIvjS4AXs/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
