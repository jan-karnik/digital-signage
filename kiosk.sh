#!/bin/bash

# Give Pi a breather so it can connect to networks etc
xrandr -o left

sleep 5

# sudo mount -t cifs //192.168.40.27/Smartboard /home/johnny/nas -o username="$1",password="$2",vers=2.0
# sleep 2

# Disable screensaver
xset s noblank
xset s off
xset -dpms

# Stop the mouse pointer from displaying on the screen
unclutter -idle 0.5 -root &

# Make sure no popups or warning bars show up
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/johnny/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/johnny/.config/chromium/Default/Preferences

echo > logs.txt

python -m pip install -r requirements.txt

python server.py /home/johnny/nas &>> logs.txt &

sleep 2

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:8081


# Run python script in the background
# nohup python myscript.py > /dev/null 2>&1 &
# python myscript.py 


