---
title: ESP32c3 Quick Connect Demo 
---

by Espressif

The ESP32-C3 has been configured to work with the AWS Quick Connect demo. This demo uses AWS services to 
take care of the AWS account creation and AWS IoT configuration required to connect your device 
to [AWS IoT](https://aws.amazon.com/iot/). Once connected, messages containing data collected from sensors 
are sent from the device, allowing you to simulate AWS IoT applications.


### To begin the Quick Connect demo:

+ **Step 1:**

  Connect the ESP32-C3 to a computer using a USB 2.0 cable (Micro B). 

+ **Step 2:**

  Download the Quick Connect setup package for the computer you will use to set up the ESP32-C3 board:   

  + Download [QuickConnect\_Espressif-ESP32C3\_windows.x64.zip](https://github.com/espressif/aws-quickconnect/raw/main/bin/QuickConnect_Espressif-ESP32C3_windows.x64.zip) 
    for Windows   

  + Download [QuickConnect\_Espressif-ESP32C3\_macos.x64.tar.gz](https://github.com/espressif/aws-quickconnect/raw/main/bin/QuickConnect_Espressif-ESP32C3_macos.x64.tar.gz) 
    for Mac   

  + Download [QuickConnect\_Espressif-ESP32C3\_linux.x64.tar.gz](https://github.com/espressif/aws-quickconnect/raw/main/bin/QuickConnect_Espressif-ESP32C3_linux.x64.tar.gz) 
    for Linux   


+ **Step 3:**

  For Windows users, download and install the USB to UART Virtual Com Port driver which can be 
  found [here](https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip).  

  For Linux users, the currently logged user should have read and write access to the serial port over 
  USB. On most Linux distributions, this is done by adding the user to dialout group with the following 
  command: 

  ```c
  sudo usermod -a -G dialout $USER
  ```
  Make sure you re-login to enable read and write permissions for the serial port.  
  

+ **Step 4:**

  Unzip the Quick Connect archive, and run the file Start\_Quick\_Connect.  

  Note: You may receive warnings while trying to run the application. If so, see the troubleshooting section 
  below.


+ **Step 5:**

  Follow & complete all of the prompts in the command line interface.
  Note: This board only supports 2.4 GHz wifi connections.


+ **Step 6:**

  When Start\_Quick\_Connect is complete, a file called CLICK-ME.html will be created in the same directory. 
  Double-click CLICK-ME.html to open a custom URL where you can visualize data from the sensors on your 
  ESP32-C3 board. 


### Specifications

![](/media/2021/ESP32-C3.png)   
ESP32-C3-DevKitC-02 is an entry-level development board based on 
the [ESP32-C3-WROOM-02](https://www.espressif.com/sites/default/files/documentation/esp32-c3-wroom-02_datasheet_en.pdf), 
a general-purpose module with 4 MB SPI flash. This board integrates complete Wi-Fi and Bluetooth LE functions. 
Meant for simple and secure connectivity applications, the ESP32-C3 is a single-core, 32-bit, RISC-V-based MCU 
with 400KB of SRAM, which is capable of running at 160MHz. It has integrated 2.4 GHz Wi-Fi and Bluetooth 5 (LE) 
with a long-range support. It has 22 programmable GPIOs with support for ADC, SPI, UART, I2C, I2S, RMT, TWAI, and PWM.


**Hardware Architecture**   
RISC-V

**Network Connectivity**   
Bluetooth LE (BLE), Sub-GHz, Wi-Fi 2.4 GHz only

**Mounting / Form Factor**   
Embedded

**Operating System**   
FreeRTOS

**Security**   
Secure boot, flash encryption, digital signature and HMAC peripheral

**Power**   
USB Powered

[Learn more](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitc-02.html)

**I/O Interfaces**   
Programmable GPIOs, SPI, UART, USB, I2C, I2S, PWM, JTAG, GDMA, TWAI, ADC

**Environmental**   
Extended

**Programming Language**   
C/C++

**Storage**   
Flash/SRAM


### Troubleshooting:

#### Permission issues while running the application:

**Windows:**   
After double-clicking the Quick Connect executable, depending on your security settings, you may see 
a pop up window that says "Windows protected your PC". Click on the "More info" link to see a "Run anyway" 
button. Click on the "Run anyway" button.  

**Mac:**   
After double-clicking the Quick Connect executable, depending on your security settings, you may see 
a pop up window that says "Start\_Quick\_Connect cannot be opened because it is from an unidentified 
developer". Right click on the Start\_Quick\_Connect file in the Finder app and select the "Open" option. 
Then click on the "Open" button in the popup that shows up.  
