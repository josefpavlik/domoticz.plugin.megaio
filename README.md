# domoticz.plugin.megaio
Domoticz plugin for MegaIO 8 relay board on raspberry

INSTALL:
* cd ~/domoticz/plugins
* git clone https://github.com/josefpavlik/domoticz.plugin.megaio.git
* sudo apt install python3-rpi.gpio python3-smbus 
* sudo service domoticz restart

SETUP:
Go to the Hardware menu and create new hardware of type "Raspberry MegaIO". Set the board id. 
Devices will be created automatically.

