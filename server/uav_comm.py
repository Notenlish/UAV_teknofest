
import time
from typing import Any

import commands
from async_client import TCPClient

# using this to just get rid of syntax errors
Script = ""
cs = ""

takeoff_throttle =  1700

class CommandToFunction:
    def __init__(self) -> None:
        self.cmd2func: dict[int, Any] = {
            1 : lambda: 0,
        }
    
    def setup_rc(self, data):
        for chan in range(1,  9):
            Script.SendRC(chan,  1500, False)
        Script.SendRC(3, Script.GetParam('RC3_MIN'), True)
        Script.Sleep(5000)
    
    def arm_motors(self, data):
        Script.ChangeMode("STABILIZE")
        Script.SendRC(5,  1750, True)
        Script.SendRC(3,  1000, True)
        Script.SendRC(4,  2000, True)
        Script.WaitFor('ARMING MOTORS',  20000)
        Script.SendRC(4,  1500, True)

    def wait_altitude(self, data):
        alt_min=data["alt_min"]
        alt_max=data["alt_max"]
        timeout=data["timeout"]

        tstart = time.time()
        while time.time() < tstart + timeout:
            if cs.alt >= alt_min and cs.alt <= alt_max:
                return True
        return False
    
    def takeoff(self, data):
        alt_min=data["alt_min"]
        Script.ChangeMode("STABILIZE")
        Script.SendRC(5,  1750, True)
        Script.SendRC(3, takeoff_throttle, True)
        if cs.alt < alt_min:
            if self.wait_altitude(alt_min, alt_min +  0.5):
                Script.ChangeMode("AltHold")
                Script.SendRC(5,  1000, True)
                Script.SendRC(3,  1450, True)

    def hover(self, data):
        hover_throttle=data["hover_throttle"]
        Script.SendRC(3, hover_throttle, True)
        Script.Sleep(3000)

    def land(self, data):
        Script.ChangeMode("LAND")
        Script.SendRC(5,  1300, True)
        Script.WaitFor('LAND',  5000)
        self.wait_altitude(-5,  1)

    def disarm_motors(self, data):
        Script.ChangeMode("STABILIZE")
        Script.WaitFor('STABILIZE',  5000)
        Script.SendRC(3,  1000, True)
        Script.SendRC(4,  1000, True)
        Script.WaitFor('DISARMING MOTORS',  15000)
        Script.SendRC(4,  1500, True)

    def init(self):
        self.cmd2func = {
            commands.COMMANDS.ARM_MOTORS : self.arm_motors,
            commands.COMMANDS.DISARM_MOTORS: self.disarm_motors,
            commands.COMMANDS.HOVER : self.hover,
            commands.COMMANDS.LAND : self.land,
            commands.COMMANDS.SETUP_RC : self.setup_rc,
            commands.COMMANDS.WAIT_ALT : self.wait_altitude,
        }



class UAVCommunication:
    def __init__(self) -> None:
        self.client = TCPClient()
        self.cmd_converter = commands.CommandConverter()
        self.cmd2func_m = CommandToFunction()
        self.cmd2func_m.init()
        self.client.cmd2func = self.cmd2func_m.cmd2func
        self.client.run()
    
    
