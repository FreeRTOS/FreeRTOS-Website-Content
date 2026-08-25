---
title: STM32L4+ Quick Connect Demo
---

by STMicroelectronics


The STM32L4+ has been configured to work with the AWS Quick Connect demo. This demo uses AWS services 
to take care of the AWS account creation and AWS IoT configuration required to connect your device 
to [AWS IoT](https://aws.amazon.com/iot/). Once connected, messages containing data collected from sensors 
are sent from the device, allowing you to simulate AWS IoT applications.


### To begin the Quick Connect demo:

+ **Step 1:**

  Connect the STM32L4+ Discovery Kit to a computer using a USB 2.0 cable (Micro B). (Check the manufacturer's 
  documentation that came with your board for the correct USB port to use.)


+ **Step 2:**

  Download the Quick Connect setup package for the computer you will use to set up the STM32L4+ board:   

  + Download [quickconnect-st-windows.x64.zip](https://www.st.com/content/dam/AME/2021/mdg/quickconnect-st-windows.x64.zip) 
    for Windows.  

  + Download [quickconnect-st-linux.x64.tar.gz](https://www.st.com/content/dam/AME/2021/mdg/quickconnect-st-linux.x64.tar.gz) 
    for Linux.  

  + Download [quickconnect-st-macos.x64.tar.gz](https://www.st.com/content/dam/AME/2021/mdg/quickconnect-st-macos.x64.tar.gz) 
    for Mac.  

  Note: Mac users may face issues while updating credentials on the device when using the DIS\_L4S5VI (BL4S5IIO01A$CU2) 
  version of the STM32L4+ Discovery Kit. If so, see the troubleshooting section below.

+ **Step 3:**

  For Windows users, download and install the ST-Link USB driver which can be 
  found [here](https://os.mbed.com/teams/ST/wiki/ST-Link-Driver).  

  For Linux users, the currently logged in user should have read and write access to the serial port over 
  USB. On most Linux distributions, this is done by adding the user to dialout group with the following 
  command:   

  ```
  sudo usermod -a -G dialout $USER
  ```

  Make sure you re-login to enable read and write permissions for the serial port.  
  

+ **Step 4:**

  Unzip the Quick Connect archive, and run the file Start\_Quick\_Connect.   

  Note: You may receive warnings while trying to run the application. If so, see the troubleshooting section 
  below.


+ **Step 5:**

  Follow & complete all of the prompts in the command line interface.   

  Note: This board only supports 2.4 GHz wifi connections. The device will disconnect/reconnect several 
  times during the provisioning process, which is normal.

+ **Step 6:**

  When Start\_Quick\_Connect is complete, a file called CLICK-ME.html will be created in the same directory. 
  Double-click CLICK-ME.html to open a custom URL where you can visualize data from the sensors on your 
  STM32L4+ board. 


### Specifications

![](/media/2021/stm32l4.jpeg)   
Built on an STM32L4S5 with ARM® Cortex®-M4 core, the B-L4S5I-IOT01A Discovery Kit IoT Node enables 
development of wide range of connected applications by providing secure, low-power communication, integrated 
multiway sensing, and out-of-the box support for AWS IoT.

**Hardware Architecture**   
ARM

**Network Connectivity**   
Bluetooth LE (BLE), NFC, Sub-GHz, Wi-Fi 2.4 GHz only

**Mounting / Form Factor**   
Embedded

**Operating System**   
FreeRTOS

**Security**   
Firewall, SSL/TLS

**Power**   
USB Powered

[Learn more](https://devices.amazonaws.com/detail/a3G0h0000087pwWEAQ/STM32L4-Discovery-Kit-IoT-Node)


**I/O Interfaces**   
ADC, Arduino, GPIO Isolated, I2C, I2S, JTAG / SWD, Pmod, PWM, SDIO, Sensor / MEMS, SPI, UART, USB


**Environmental**   
Extended


**Programming Language**   
C/C++


**Storage**   
Flash/NVRAM


**Availability**   
APAC, Australia, Canada, China, EMEA, EU, Japan, Korea, LATAM, New Zealand, UK, USA


### Troubleshooting:

#### Permission issues while running the application:

**Windows:**   
After double-clicking the Start\_Quick\_Connect.exe to start the utility, depending on their security 
settings, Windows 10 users may see a pop up windows that says "Windows protected your PC". The workaround 
is to click on the "More info" link in the same window which will then present a "Run anyway" button. 
Click on the "Run anyway" button.  

**Mac:**   
After double-clicking the Start\_Quick\_Connect.exe to start the utility, depending on their security 
settings, Mac users may see a pop up windows that says that "Start\_Quick\_Connect cannot be opened 
because it is from an unidentified developer". The workaround is to right click on the Start\_Quick\_connect 
file in finder app and select the "Open" option. Then click on the "Open" button in the popup that shows up.  


#### Permission denied while building the projects:

`"../../prebuild.sh" "../.."
/bin/sh: ../../prebuild.sh: Permission denied
make[1]: ** [makefile:96: pre-build] Error 126*
*make:* * [makefile:64: all] Error 2
"make all" terminated with exit code 2. Build might be incomplete.`  

**Solution:**   
`cd /Projects/B-L4S5I-IOT01A/Applications/BootLoader\_STSAFE/2\_Images\_SECoreBin
chmod +x STM32CubeIDE/*`
  

#### Build errors: Could not import modules:

**Solutions:**  

1. Ensure you have the following modules installed: pycryptodomex, lief, ecdsa, numpy, argparse. If 
   you are missing any, download them by running  `pip install <module_name>`   
  
2. Ensure python points to version 3.7+ in your environment.  

   If it doesn't, replace `cmd=python` in 
   Projects/B-L4S5I-IOT01A/Applications/BootLoader\_STSAFE/2\_Images\_SECoreBin/STM32CubeIDE/prebuild.sh 
   with `cmd=python**3**` (or appropriate)
   

#### Errors with STM32CubeProgrammer:

`Generating the global elf file (SBSFU and userApp)
fix access path to STM32_Programmer_CLI
../../../../BootLoader_STSAFE/2_Images_SECoreBin/STM32CubeIDE/postbuild.sh: line 96: -ms: command not found`  

**Solution:**  
Add STM32CubeProgrammer to your path by either:   

1. adding the following line to postbuild.sh:  

   `export PATH=$PATH:/Applications/STMicroelectronics/STM32Cube/STM32CubeProgrammer
   /STM32CubeProgrammer.app/Contents/MacOs/bin`  
   

2. permanently adding it to /etc/paths:   

   In a text editor, open /etc/paths. Append `/Applications/STMicroelectronics/STM32Cube/STM32CubeProgrammer
   /STM32CubeProgrammer.app/Contents/MacOs/bin` to the end of the file.    


#### Unable connect to AWS or WiFi:

**Solution:**  

1. Disconnect and reconnect the board to your computer.   

2. Run Start\_Quick\_Connect again.
  

#### Error while provisioning the board with WiFi credentials:

**Solution:**  

1. Disconnect/reconnect the board and try again.   

2. Manually copy/paste the AWS\_Config bin to the device folder and follow the prompts to enter your 
   WiFi SSID and Password. Then run Start\_Quick\_Connect again.
