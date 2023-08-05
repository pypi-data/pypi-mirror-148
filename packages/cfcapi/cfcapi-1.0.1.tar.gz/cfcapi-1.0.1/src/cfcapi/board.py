# -*- coding: utf-8 -*-
"""
******************************************************************************
Created on Thu Apr 22 15:34:53 2022
api_cfc.py: Api to control the Caonabo Driving Board for DNA synthesis.

Version:
    V1.0.0: Initial release.

author = César J. Lockhart de la Rosa
copyright = Copyright 2022, imec
license = GPL
email = lockhart@imec.be, cesar@lockhart-borremans.com
status = Released
******************************************************************************
"""

import serial
import serial.tools.list_ports as ls_ports
import cfcapi.config as config
import time

# Python conventional header

class cfc:
    """
    Class for interfacing the Caonabo Driving Board (CDB).
    """
    def __init__(self, port="NA", board_id="NA",
                 board_description="NA",
                 conf=config.confGlobal()):
        
        self.conf = conf
        
        if board_id == "NA" :
            self.board_id = self.conf.board_id
        else:
            self.board_id = "ID:" + board_id
            self.conf.board_id = board_id
            
        self.board_id_ok = False
        

        if board_description == "NA" :
            self.board_description = self.conf.board_description
        else:
            self.board_description = board_description

        if port != "NA" :
            self.conf.port = port           
        

        if self.conf.port == "AUTO":
            self.discoverPort()
        else:
            self.com()
            
        self.addrModules = self.getAddress()
        print("CFC Modules addresses: {0}".format(self.addrModules))
            
        
    def discoverPort(self):
        port_list = list(ls_ports.comports())
        
        port_name=[]
        
        for p in port_list:
            
            if self.conf.board_vid_pid in p.hwid: #It is an arduino 33 BLE
                port_name.append(p.device)
        
        for p in port_name:
            try:
                self.com(port=p, bit_rate=self.conf.bit_rate,
                board_id=self.board_id, timeout=self.conf.timeout)
                portOpen = True
            except:
                portOpen = False

            if not self.board_id_ok:
                if portOpen:
                    self.serial.close()
            else:
                self.conf.port = p
                break
             
    def com(self, port='NA', bit_rate='NA', board_id="NA", timeout="NA"):
        
        #Taking default values if nothing is specified.
        if port == "NA":
            port = self.conf.port
            
        if bit_rate == "NA":
            bit_rate = self.conf.bit_rate
            
        if board_id == "NA":
            board_id = self.conf.board_id
        
        if timeout == "NA":
            timeout = self.conf.timeout
            
        # Starting serial communication
        self.serial = serial.Serial(port=port, baudrate=bit_rate,
                                    timeout=timeout)
        
        # Getting ID and verifying that right board is connected.
        time.sleep(1)
        
        id_hw = self.getID().split("_")
        
        board_version = id_hw[0]
        firmware_version = id_hw[1]
        board_id_hw = id_hw[2]
        
        if (board_id == board_id_hw) and ("CFC" in board_version):
            print("Caonabo Fluidic Controller (CFC) with correct ID" + 
                  " initiated in port: {0}.".format(port))
            self.board_id_ok = True
            self.board_version = board_version
            self.firmware_version = firmware_version
        
        else:
            self.board_id_ok = False
        

    def write(self, string):
        response = self.serial.write(string.encode('utf-8'))
        return response
    
    def read(self):
        return self.serial.readline().decode('utf-8')[0:-2]

    def acknowledgeWrite(self):
        """
        Check that a write call was performed correctly. 

        Raises
        ------
        ValueError
            If the read does not return the correct acknowledgment string.
        """

        if  self.read() != self.conf.ACKNOWLEDGE:
            raise ValueError('Could not acknowledge the write command.')

#*****************************************************************************
#Core methods to manipulate the CFC
#*****************************************************************************
    def getID(self):
        """
        Method to get the board id.
        """
        
        s_cmd = 'ID?\n'
        self.write(s_cmd)
        return self.read()
    
    def getAddress(self):
        """
        Method for obtaining the address configured for the firmware of the 
        different modules (must match the phisical DIP-Switches).

        Returns
        -------
        addr : list
            list of strings with the address of the different modules.

        """
        addr = []
        
        s_cmd = 'GMA\n'
        self.write(s_cmd)
        
        value = self.read()
        
        while (value != self.conf.ACKNOWLEDGE):
            addr.append(value)
            value = self.read()
        
        return addr
    
    def rgbLED(self, r,g,b):
        """
        Method to set the status of the RGB LED in the Arduino nano 33 BLE
        board.

        Parameters
        ----------
        r : int
            Status of the red LED (0 for off 1 for ON).
        
        g : int
            Status of the red LED (0 for off 1 for ON).
        
        b : int
            Status of the red LED (0 for off 1 for ON).
            
        """
        data = "{0}{1}{2}".format(r,g,b)
        s_cmd = 'LED' + data + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def confIO(self, mode_list, module="A"):
        """
        Method to configure the IO ports available in either the arduino or the
        valve modules.

        Parameters
        ----------
        module : int (or str for arduino)
            Identify the module. The valve modules can be identified with
            integers from 0 to 4. For the Arduino (default) "A" must be passed.
            
        mode_list : list or str
            List or string with the values for configuring the ports. It must
            have 9 elements for the Arduino and 5 elments for the valve
            modules. The values are 0 for input and 1 for output.
        """
        
        #in case of Arduino module
        if type(module) == str:
            if module.upper() == "A":
                cmd = "CIO"
               
                #exception for not passing the right amoung or elements  
                aPorts = self.conf.amntArduinoIO
                if  len(mode_list) != aPorts:
                    
                    msg = "The amount of ports to be configure is "\
                          "different to the available digital ports"\
                          "({0}) in the Arduino module.".format(aPorts)
                    
                    raise ValueError(msg)

                data = ""
                for element in mode_list:
                    data = data + str(element)
            else:
                msg = "Non existing module as string: {0}".format(module)
                raise ValueError(msg)
        
        #In case it is for one of the valve modules
        else:
            cmd = "CMP"
            
            #Exception for module with not defined indexes
            indexModules = self.conf.indexModules
            if module not in indexModules:
                msg = "Not a valid index for Module. "\
                      "valid indexes are: {0}".format(indexModules)
                raise ValueError(msg)

            #exception for not passing the right amoung or elements  
            mPorts = len(self.conf.indexModuleIO)
            if  len(mode_list) != mPorts:
                
                msg = "The amount of ports to be configure is "\
                      "different to the available digital ports"\
                      "({0}) in the specified module.".format(mPorts)
                
                raise ValueError(msg)                
            
            data = str(module)
            for element in mode_list:
                data = data + str(element)
        
        s_cmd = cmd + data + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
    
    def writeIO(self, ioNumber, value, module="A"):
        """
        Method to write to the digital ports of the Arduino, or the valve
        modules. 

        Parameters
        ----------
        ioNumber : int
            Number of the index for the IO to be activated. normally from
            2 to 10 in the arduino module or from 0 to 4 in the valve modules.
        
        value : int
            Value to be written. 0 for GND and 1 for VCC.
            
        module : int or str, optional
            To identify the module to be written. for the arduino "A" must be
            specified, for the the valve modules an integer number from
            0 to 4. The default is "A".

        """
        
        #exception for wrong IO value (must be 0 [GND] or 1 [VCC])  
        goodValues = self.conf.DigitalValues
        if  value not in goodValues:
            
            msg = "IO value not a valid value. "\
                  "Posible values are ({0}) as integer".format(goodValues)
            
            raise ValueError(msg)
        
        #in case of Arduino module
        if type(module) == str:
            if module.upper() == "A":
                cmd = "WIO"
               
                #exception for wrong IO number  
                iArdIO = self.conf.indexArduinoIO
                if  ioNumber not in iArdIO:
            
                    msg = "IO number not a valid index for an Arduino "\
                          "digital IO ({0})".format(iArdIO)
                    
                    raise ValueError(msg)
                    
                data = "{0}".format(ioNumber).zfill(2) + str(value)
            else:
                msg = "Non existing module as string: {0}".format(module)
                raise ValueError(msg)
        
        #In case it is for one of the valve modules
        else:
            cmd = "WMP"
            
            #Exception for module with not defined indexes
            indexModules = self.conf.indexModules
            if module not in indexModules:
                msg = "Not a valid index for Module. "\
                      "valid indexes are: {0}".format(indexModules)
                raise ValueError(msg)
            
            #exception for wrong IO number 
            iModIO = self.conf.indexModuleIO
            if  ioNumber not in iModIO:
                
                msg = "IO number not a valid index for a valve module "\
                      "digital IO ({0})".format(iModIO)
                      
                raise ValueError(msg)              
            
            data = str(module)+str(ioNumber)+str(value)
        
        s_cmd = cmd + data + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()

    def readIO(self, ioNumber, module="A"):
        """
        Method to read the digital ports of the Arduino, or the valve
        modules. 

        Parameters
        ----------
        ioNumber : int
            Number of the index for the IO to be read. normally from
            2 to 10 in the arduino module or from 0 to 4 in the valve modules.
            
        module : int or str, optional
            To identify the module to be read. for the arduino "A" must be
            specified, for the the valve modules an integer number from
            0 to 4. The default is "A".
        
        Return
        ------
        value : int
            Return 0 for ground and 1 for vcc. (REMEMBER THE ARDUINO MODULE
            WORK WITH 3.3V LOGIC NOT 5.0V!!!!!)
        """
        
        #in case of Arduino module
        if type(module) == str:
            if module.upper() == "A":
                cmd = "RIO"
               
                #exception for wrong IO number  
                iArdIO = self.conf.indexArduinoIO
                if  ioNumber not in iArdIO:
            
                    msg = "IO number not a valid index for an Arduino "\
                          "digital IO ({0})".format(iArdIO)
                    
                    raise ValueError(msg)
                    
                data = "{0}".format(ioNumber).zfill(2)
            else:
                msg = "Non existing module as string: {0}".format(module)
                raise ValueError(msg)
        
        #In case it is for one of the valve modules
        else:
            cmd = "RMP"
            
            #Exception for module with not defined indexes
            indexModules = self.conf.indexModules
            if module not in indexModules:
                msg = "Not a valid index for Module. "\
                      "valid indexes are: {0}".format(indexModules)
                raise ValueError(msg)
            
            #exception for wrong IO number 
            iModIO = self.conf.indexModuleIO
            if  ioNumber not in iModIO:
                
                msg = "IO number not a valid index for a valve module "\
                      "digital IO ({0})".format(iModIO)
                      
                raise ValueError(msg)              
            
            data = str(module)+str(ioNumber)
        
        s_cmd = cmd + data + '\n'    
        self.write(s_cmd)
        return int(self.read())
        
    def analogRead(self, aNumber):
        """
        Method to read the analog ports of the Arduino. REMEMBER ARDUINO
        ANALOG PORTS ARE 3.3V MAX!!!!! IF HIGHER POTENTIALS NEED TO BE
        MEASURED A POTENTIAL DIVIDER IS REQUIRED. The input impedance of the 
        analog pins is 100Mohms.

        Parameters
        ----------
        aNumber : int
            Analog port number (normally from 0 to 6).
        
        Return
        ------
        value : int
            Return 0 for 0.0V and 1023 for 3.3V. Potentials in between will
            change the the returned value proportionally.
        """
        
        #exception for wrong A number  
        iArdA = self.conf.indexArduinoA
        if  aNumber not in iArdA:
    
            msg = "Analog pin number not a valid index for an Arduino "\
                  "analog pin ({0})".format(iArdA)
            
            raise ValueError(msg)
            
        data = "{0}".format(aNumber)
        
        s_cmd = 'AAR' + data + '\n'    
        self.write(s_cmd)
        return int(self.read())
    
    def moduleLED(self, module, value):
        """
        Method to manipulate the LEDs in the different valve modules of the 
        CFC. the Values can be 1 for ON state and 0 for Off state.

        Parameters
        ----------
        module : int
            Module wich LED we want to manipulate.
            
        value : int
            0 or 1 for turning the Led OFF or ON respectively.
        """
        
        
        #exception for wrong IO value (must be 0 [GND] or 1 [VCC])  
        goodValues = self.conf.DigitalValues
        if  value not in goodValues:
            
            msg = "LED value not a valid value. "\
                  "Posible values are ({0}) as integer".format(goodValues)
            
            raise ValueError(msg)
        
        #Exception for module with not defined indexes
        indexModules = self.conf.indexModules
        if module not in indexModules:
            msg = "Not a valid index for a Module. "\
                  "valid indexes are: {0}".format(indexModules)
            raise ValueError(msg)
        
        data = str(module)+str(value)
        s_cmd = 'LDM' + data + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
        
    
    def setValve(self, valve):
        """
        Method to set a valve on the CFC. the value can go from 0 to 49.
        basically the tens identify the module and the units the valve inside
        the module. Thus valve 0 (same as 00) is the valve 0 of the module 0.
        valve 49 on the other hand is the the valve 9 of the module 4.

        Parameters
        ----------
        valve : int
            Value from 0 to 49 identifying the valve.

        """
        
        #Exception for valve index ouside of allowed range
        indexValves = self.conf.indexValves
        if valve not in indexValves:
            msg = "Not a valid index for a valve. "\
                  "valid indexes are: {0}".format(indexValves)
            raise ValueError(msg)
        
        data = "{0}".format(valve).zfill(2)    
        s_cmd = 'SMV' + data + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()

    def clearValve(self, valve):
        """
        Method to clear a valve on the CFC. the value can go from 0 to 49.
        basically the tens identify the module and the units the valve inside
        the module. Thus valve 0 (same as 00) is the valve 0 of the module 0.
        valve 49 on the other hand is the the valve 9 of the module 4.

        Parameters
        ----------
        valve : int
            Value from 0 to 49 identifying the valve.

        """
        
        #Exception for valve index ouside of allowed range
        indexValves = self.conf.indexValves
        if valve not in indexValves:
            msg = "Not a valid index for a valve. "\
                  "valid indexes are: {0}".format(indexValves)
            raise ValueError(msg)
        
        data = "{0}".format(valve).zfill(2)    
        s_cmd = 'CMV' + data + '\n'    
        self.write(s_cmd)
        self.acknowledgeWrite()
        
#*****************************************************************************
#Secondary methods (one layer up)
#*****************************************************************************
    
    def pulse(self, valve, tON, tOFF=0, periods=1):
        """
        Method to create a tren of pulses activating one of the valves. 
        As the default for tOFF is 0 and for periods is 1 tha means that if
        a valve and tON is pecified the resulting behaviour is that of a timed
        ON of the valve and then it goes off.

        Parameters
        ----------
        valve : int
            Index of the valve, from 0 to 49.
        tON : float
            Time for the valve to remain ON in seconds.
        tOFF : float, optional
            Time for the valve to remain OFF in seconds. The default is 0.
        periods : int, optional
            How many time will the signal be repeated. The default is 1.

        """
        
        for cycle in range(periods):
            self.setValve(valve)
            time.sleep(tON)
            self.clearValve(valve)
            time.sleep(tOFF)
            
            #To print progress
            print("\rPeriod: {0}".format(cycle+1), end="")
    
    def testModules(self,t=0.5):
        """
        Method to test communication to all the modules by sweeping through
        the LEDs.
        
        Parameters
        ----------
        t : float
            Time that each module will remain ON in seconds. default is 0.5
        """
        
        list_iModules = self.conf.indexModules
        
        for module in list_iModules:
            self.moduleLED(module, 1)
            time.sleep(t)
            self.moduleLED(module, 0)
        
            
    
            

#*****************************************************************************
#General methods
#*****************************************************************************

    def close(self):
        """Close the serial port."""
        self.serial.close()
    
    def open(self):
        """Open the serial port."""
        self.serial.open()

        
        
        
        
     