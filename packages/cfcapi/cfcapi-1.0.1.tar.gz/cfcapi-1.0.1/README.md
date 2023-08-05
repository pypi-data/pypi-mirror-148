[//]: # (1 Project's title)
# cfcapi

[//]: # (2 Project description)
`Python` API to interact with the Caonabo Fluidic Controller (CFC).
The CFC is a board that allows one to control a total of 50 valves to manipulate the flow of chemicals.
It is composed of five valve modules and one control module. Each valve module is composed of the following peripherals:

- Darlington open collector transistor outputs with flyback protection diodes for controlling valves (10)
- Input / output TTL (5.0V) digital ports (5)
- Module indicator LED (1)

From the 10 valve outputs of each valve module, 6 of them (from index 0 to 5) can drive valves of up to 0.5A,
the remaining 4 (6 to 9) can handle up to 1A. All of them can handle up to 50V.

The control module is built around an Arduino Nano 33 BLE module and is composed of the following peripherals:
- Input / output CMOS (3.3V) digital ports (10)
- Analog (0V to 3.3V) inputs  (7)
- Module indicator RGB LED (1)

This API allows the manipulation of all these peripherals in `Python`. For more information regarding the CFC hardware please visit its [repository](https://github.imec.be/dna-storage/cfc).

[//]: # (3 Table of contents)
## Table of contents <a name="table-contents"></a>

1. [Installation and package dependencies](#installation)
2. [How to use the package](#use)
    + [2.1 Instantiation, initiation and closing comunication to the board.](#instantiation)
    + [2.2 Working with digital Input/Ouput (IO) ports and analog ports.](#io)
    + [2.3 Working with valves.](#valves)
3. [API reference guide](#reference)
4. [Contributors](#contributors)
5. [License](#license) 

[//]: # (4 Package dependencies)
## 1 Installation and package dependencies <a name="installation"></a>

This packager requires the previous installation of the following packages:
- [pyserial 3.5 (or newer)](https://pypi.org/project/pyserial/)

Afer installing the dependencies, the package can be installed from the Python package index (`PyPI`) repository.

In Windows:

```PowerShell
C:\> pip install --user cfcapi
```

or in Linux:

```bash
$ pip install --user cfcapi
```

As an alternative, the cfcapi package (inside the `src/` folder) can be download and copied into the the main folder of the project where it will be used.

[//]: # (5 How to use the package)
## 2 How to use the package <a name="use"></a>

### 2.1 Instantiation, initiation and closing communication to the board. <a name="instantiation"></a>

First, the module must be imported:

```python
>>> from cfcapi import board
```

Once imported the cfc class inside the module must be instantatiated to gain control to an specific CFC board.
Hence, the port where the CFC board is connected, as well as the ID of the board, must be specified.
For the port, the name of the port can be given such as `"COM1"` or `"AUTO"` can be used.
Sometimes, `"AUTO"` might not work due to conflict with some USB devices. 
If this happens, the port will have to be passed manually. An example instantiations can be as folows:

```python
>>> cfc = board.cfc(port="AUTO", board_id="000")
```

Once initiated, the following output will appear in the console:

>    Caonabo Fluidic Controller (CFC) with correct ID initiated in port: COM26.  
>    CFC Modules addresses: \['2', '3', '4', '5', '6'\]

The last line identifies the addresses of the 5 different valve modules (from 0 to 4),
and should agree with the physical address configured for each module with the DIP switches.
If this does not match, communication with that module will fail. 
To test that the communication to each module works the the `testModule()` method can be used.
For example:

```python
>>> cfc.testModules()
```

The *Module indicator LEDs* of each module will turn on for 0.5s sequentially from module 0 to module 4.
If the communication to any of the module fails, the respective LED will not be turned on.
The first thing to check while debugging a possible problem is the that the physical address (set with the DIP switch)
matches with that of the firmware (the one shown when instantiating or when using the method `getAddress()`).

At the end, the instance must be properly closed to avoid leaving the serial ports open. This is done by using the `close()` method:

```python
>>> cfc.close()
```

### 2.2 Working with digital input/ouput (IO) ports and analog ports. <a name="io"></a>

For working the IO ports, they first have to be configured.
By default, the digital ports of the modules (pin 10 to 14 of pin header) are configured as *inputs*.
The index for addressing the IOs of the modules is from 0 to 4 linked to physical pins 10 to 14.
The IOs of the Arduino module (D2 to D10) are also initiated as *inputs*.
The indexes to address the IOs from the Arduino module runs from 2 to 10.

**To configure** the IO ports, the method `confIO(mode_list, module)` must be used.
The first parameter required is a list of integers that represents whether the pin will act as an input (0) or an output (1).
The amount of elements in the list should match the amount of IOs in the port to be configured (*i.e.*, 5 for the valve modules and 9 for the Arduino module).
The second parameter is the module: for valve modules a value between `0` to `4` (integer) can be used,
and for the Arduino module the `"A"` character must be used.
By default (*i.e.*, if no module value is passed) the Arduino module is selected.
To configure the first three (0, 1 and 2) IO ports of module 0 as outputs, and the last two (3 and 4) as inputs the following example can be used:

```python
>>> cfc.confIO(mode_list=[1, 1, 1, 0, 0], module=0)
```

To configure all the IOs of the Arduino module (D2 to D10) as outputs, the following example can be used:

```python
>>> cfc.confIO(mode_list=[1, 1, 1, 1, 1, 1, 1, 1, 1], module="A")
```

Once configured, the IO port can be **writen** by using the method `writeIO(ioNumber, value, module)`,
or **read** using the method `readIO(ioNumber, module)`.
The parameter `ioNumber` is the number identifying the IO (from 0 to 4 for valve modules and from 2 to 10 for Arduino module).
The value parameter (only for writing) specify whether the IO port will be 1 (5V for valve modules and 3.3V for Arduino module) or 0 (GND for all modules).
Finally, the module parameter (0 to 4 or "A") will identify the module to which the IO belongs.
For example, to write 1 to IO 0 of module 0 you can use:

```python
>>> cfc.writeIO(ioNumber=0, value=1, module=0)
```

and to read from IO D9 of the Arduino module can use:

```python
>>> cfc.readIO(ioNumber=9, module="A")` or `>>> cfc.readIO(ioNumber=9)
```

The **analog** ports in the Arduino module (A0 to A6) can be **read** using the method `analogRead(aNumber)`.
The `aNumber` parmeter is simply the number of the analog port to be read (from `0` to `6`).
The method returns a value between 0 and 1023, proportional to the voltage in the respective port (from 0 to 3.3v).

### 2.3 Working with valves. <a name="valves"></a>

To **set a valve** output the method `setValve(valve)` must be used, and to **to clear a valve** the method `clearValve(valve)` must be used.
The `valve` parameter is value from `0` to `49` identifiying the valve.
The first digit in the number identifies the module and second digit identifies the valve.
For example, valve `45` is valve with index `5` on module with index `4`.
Similarly, valve `3` (same as `03`) identifies the valve with index `3` in module with index `0`.
For example, setting and clearing valve 3 of module 2 can be done with:

```python
>>> cfc.setValve(23)
```

and


```python
>>> cfc.clearValve(23)
```

Additionally, the valves can be **activated with a pulse** with the method `pulse(valve, tON, tOFF, periods)`.
The `valve` parameter is the same as for the previous methods, where `tON` and `tOFF` are use to specify
the amount of time (in seconds) that the valve will remain on and off, respectively. Parameter `tOFF` is set to `0`.
The last parameter `periods` is use to define how many times the cycle `tON` and `tOF` must be repeated.
By default, `periods` is set to 1.
If it is desired to set on valve 23 for one second the following code can be used:

```python
>>> cfc.pulse(valve=23, tON=1, tOFF=0, periods=1)
```

or

```python
>>> cfc.pulse(valve=23, tON=1)
```
 
[//]: # (6 API Reference Guide)
## 3 API Reference Guide <a name="reference"></a>

|    | Method | Description | Parameters | Returns | Example |
| -- |--------|-------------|------------|---------|---------|
| 00 | getID | Returns the ID of the CFC board. | NA | ID (string) | `cfc.getID()` |
| 01 |getAddress | Returns the address of the modules configured in the firmware. | NA | addresses (list of strings) | `cfc.getAddress()` |
| 02 |rgbLED | Set status of the RGB LED in the Arduino nano 33 BLE board ON (1) or OFF (0). | r, g, b (int) | NA | `cfc.rgbLED(0,1,0)` |
| 03 |confIO | Configures the IO ports available in either the arduino or the valve modules. | mode_list (str), module="A" (str or int) | NA | `cfc.confIO("11100",0)` |
| 04 |writeIO | Write to the IO ports of the Arduino or the valve modules. | ioNumber (int), value (int - 0 or 1), module="A" (int of str) | NA | `cfc.writeIO(3,1,"A")` |
| 05 |readIO | Read the digital ports of the Arduino, or the valve modules. | ioNumber (int), module="A" (int of str) |  value (int - 0 or 1) | `cfc.readIO(3,"A")` |
| 06 |analogRead | Read the analog ports of the Arduino. *Z<sub>IN</sub>* is 10<sup>8</sup> *ohm*. | aNumber (int) | value (int - 0 to 1023) | `cfc.analogRead(2)` |
| 07 |moduleLED | Manipulate the LEDs in the different valve modules of the CFC. |module, value (int) | NA | `cfc.moduleLED(0,1)` |
| 08 |setValve | Set a valve on the CFC. The value can go from 0 to 49. | valve (int) | NA | `cfc.setValve(15)` |
| 09 |clearValve | Clear a valve on the CFC. The value can go from 0 to 49. | valve (int) | NA | `cfc.clearValve(15)` |
| 10 |pulse | Create a tren of pulses activating one of the valves. | valve, tON, tOFF=0, periods=1 (int) | NA | `cfc.pulse(15,1,0,1)` |
| 11 |testModules | Activate the LED on the modules sequentially. The LED remains ON for t seconds. | t=0.5 (float) | NA | `cfc.testModules()` |
| 12 | discoverPort | Discover the USB port to which the CFC is connected. | NA | port (str) | `cfc.discoverPort()` |
| 13 | com | Start serial communication with the CFC. Runs once during instantiation. | port="NA" (str), bit_rate="NA" (str or int), board_id="NA" (str), timeout="NA" (Str or float) | NA | `cfc.com("COM4",115200, "000", 1)` |
| 14 | write | Write string of characters to the CFC through the serial bus. | string (str) | response (str) | `cfc.write("ID?")` |
| 15 | read | Read string of characters from the CFC through the serial bus. | NA | response (str) | `cfc.read()` |
| 16 | acknowledgeWrite | Check for the acknowledgement response from the CFC after writing a command that does not require a return from the CFC.| NA | NA | `cfc.acknowledgeWrite()` |
| 17 |close | Method to close the communication to the CFC. | NA | NA | `cfc.close()` |
| 18 |open | Method to open communication to the CFC. | NA | NA | `cfc.open()` |

[//]: # (7 Contributors)
## 4 Contributors <a name="contributors"></a>
- [César Javier Lockhart de la Rosa (lockhart@imec.be)](https://github.imec.be/lockhart)
- [Kherim Willems (kherim.willems@imec.be)](https://github.imec.be/willemsk)
- [Naghmeh Fatemi (naghmeh.fatemi.ext@imec.be)](https://github.imec.be/fatemi94)

[//]: # (8-License)
## 5 License <a name="license"></a>

Copyright (c) 2022 [César J. Lockhart de la Rosa (lockhart@imec.be)](https://github.imec.be/lockhart)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
