# MagaIO
#
# Author: Josef Pavlik, 2020
# based on HTML.py example
#
# todo:
# megaio 0 awrite 2000
# 
# megaio 0 aread 7
#
"""
<plugin key="MegaIO" name="Raspberry MegaIO" author="Josef" version="0.1" externallink="">
    <description>
    MegaIO 8 relay board on raspberry
    </description>
    <params>
        <param field="Mode1" label="board number" width="75px" default="0"/>
        <param field="Mode6" label="Debug" width="75px">
          <options>
              <option label="True" value="Debug"/>
              <option label="False" value="Normal"  default="true" />
          </options>
      </param>
    </params>
</plugin>
"""
import Domoticz
import os
import subprocess
import re
import megaio

class BasePlugin:
    board = 0
    running = 0
    debug = 0
    inp_state = 0
    inp_diff = 0


# megaio sometimes returns wrong value. Read more time.
    def get_opto_in_safe(self, a):
        r=a
        a^=self.inp_state
        c=a
        a&=self.inp_diff
        self.inp_state^=a
        self.inp_diff=c
        return self.inp_state

    def set_relay(self,Unit, val):
#        command="megaio "+self.board+" rwrite " + str(Unit) + " "+(val and "on" or "off") 
#        if (self.debug): Domoticz.Log("set_relay exec "+command)
        if self.debug: Domoticz.Log("set_relay "+str(Unit)+" to "+str(val))
#        os.system(command)
        megaio.set_relay(self.board, Unit, int(val))
    
    def __init__(self):
        return

    def connection(self):
        return 
      
    def onStart(self):        
        self.board=int(Parameters["Mode1"])
        self.debug=Parameters["Mode6"]=="Debug"
        Domoticz.Log("onStart - Plugin is starting, debug="+str(self.debug))
        for x in range(1, 9):
            if (x not in Devices): Domoticz.Device(Name="Relay_"+str(x), Unit=x, TypeName="Switch", Used=1).Create()
            if (x+8 not in Devices): Domoticz.Device(Name="Input_"+str(x), Unit=x+8, TypeName="Switch", Used=1).Create()
            self.set_relay(x, Devices[x].nValue)
        Domoticz.Heartbeat(3)
        self.running=1
        self.inp_state=megaio.get_opto_in(self.board)

    def onStop(self):
        Domoticz.Log("onStop - Plugin is stopping.")

    def onConnect(self, Connection, Status, Description):
        return

    def onMessage(self, Connection, Data):
        return
      
    def onCommand(self, Unit, Command, Level, Hue):
        self.set_relay(Unit, Command=="On")
        val=Command=="On" and "1" or "0"
        if (Unit in Devices): Devices[Unit].Update(int(val),val)

    def onDisconnect(self, Connection):
        unused=0

    def onHeartbeat(self):
        if self.running:
          val=megaio.get_relays(self.board)
          a=megaio.get_opto_in(self.board)
          inp=self.get_opto_in_safe(a)
          if (self.debug): Domoticz.Log("read relays -> %02x, raw -> %02x, inputs -> %02x" % (val,a,inp))
          for Unit in range(1,9):
            val1=(val >> (Unit-1)) & 1
            inp1=(inp >> (Unit-1)) & 1
            if (Unit in Devices): Devices[Unit].Update(int(val1),str(val1))
            if (Unit+8 in Devices): Devices[Unit+8].Update(int(inp1),str(val1))

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

