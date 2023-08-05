    # -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 13:33:19 2019

@author: lockhart
"""

class confGlobal:
    """
    With the configuration parameters fro the cmb serial interface.
    """
    def __init__(self):    

        self.bit_rate = 115200  #bit rate for the communication
        self.board_id = "000" # Board identifier to discover.
        self.board_description = "Nano 33 BLE"
        self.board_vid_pid = "VID:PID=2341:805A"
        self.timeout = 1 #timeout in seconds.
        self.port = "AUTO" #Port where the cmb is connected
        
        #Acknowledge
        self.ACKNOWLEDGE = 'OK'
        
        #Indexes limits for the board and modules
        self.amntArduinoIO = 9
        self.amntModules = 5
        self.indexModules = [x for x in range(0,5)]
        self.indexArduinoIO = [x for x in range(2,11)]
        self.indexModuleIO = [x for x in range(0,5)]
        self.DigitalValues = [0,1]
        self.indexArduinoA = [x for x in range(0,7)]
        self.indexValves = [x for x in range(0, 50)]

