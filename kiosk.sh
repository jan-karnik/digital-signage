#!/bin/bash

# Give Pi a breather so it can connect to networks etc
sleep 5

# Disable screensaver
xset s noblank
xset s off
xset -dpms

# Stop the mouse pointer from displaying on the screen
unclutter -idle 0.5 -root &

# Make sure no popups or warning bars show up
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/johnny/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/johnny/.config/chromium/Default/Preferences


python -m pip install -r requirements.txt

python /home/johnny/digital-signage/server.py /mnt/usb/nas &>> logs.txt &

sleep 2

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:8081 &


# Activate the virtual environment
# source /path/to/venv/bin/activate

# Run python script in the background
# nohup python myscript.py > /dev/null 2>&1 &
# python myscript.py 


