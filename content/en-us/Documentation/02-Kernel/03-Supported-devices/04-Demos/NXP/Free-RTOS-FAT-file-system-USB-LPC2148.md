---
title: "FreeRTOS LPC2148 Demo by JC Wren Including FatFS and LPCUSB"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

J.C. Wren has put together a very complete and useful example FreeRTOS application that includes, amongst other things:
* The FatFS [free FAT file system](http://elm-chan.org/fsw/ff/00index_e.html) from ChaN.
* The LPCUSB [free USB stack](http://sourceforge.net/projects/lpcusb) for the LPC214x from Bertrik Sikken.
* A newlib implementation.
* A console command interpreter.
* A GPS NMEA interface.
* Various peripheral drivers including I2C, SPI, UART, ADC, external interrupts, real time clock, GPIO and of course USB.

The source code zip file, which includes all the FreeRTOS, FatFS and LPCUSB source code, can be downloaded directly from [JC Wren](http://jcwren.com/arm)
for both Windows and Linux users.

**Full information, including build and download instructions, can be obtained from the
[application note](http://jcwren.com/arm/xREADME_latest) that accompanies the source code.**

I would like to say thank you to J.C Wren for his fantastic effort, and for sharing it with the FreeRTOS community.
