# Digital Signage

Simple application that loops through images and videos.

Python server with Flask that serves HTML files that can be opened up with a chromium browser in `--kiosk` mode (e.g. on a Raspberry Pi) and display a slideshow to users.


## TODO
- [ ] Add a script for mounting and unmounting drives
- [ ] export variable with DISPLAY=:0

### Working with newly created [linux system service](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)


Enable the service to start at boot automatically:
`sudo systemctl enable <name>.service`

Start the service manually without restarting the raspberry Pi:
`sudo systemctl start <name>.service`

Check the status of a service:
`sudo systemctl status <name>.service`


### Reading

How to mount and unmount volumes to Raspberry Pi automatically after boot - https://raspberrytips.com/mount-usb-drive-raspberry-pi/

