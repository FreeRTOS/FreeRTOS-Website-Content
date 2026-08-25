---
title: Legacy Demos with Other Open Source TCP/IP Stacks
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**Note this page pre-dates the introduction of [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) - which is FreeRTOS's
own embedded TCP/IP stack.**

This page lists the legacy FreeRTOS demo projects that include an embedded web server within
a fully preemptive multitasking environment. Some demos use lwIP as the underlying embedded TCP/IP stack and pre-date the introduction
of [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) (FreeRTOS's own scalable TCP/IP stack). The projects vary in age and
therefore also vary in the version of the stacks used. More information
is provided on the stacks directly below. The demos themselves are [listed by microcontroller](#freertos-demos-that-include-tcpip-functionality)
manufacturer below that.

### lwIP

lwIP is also a good stack when used in its intended, memory constrained, environment.
It has a higher throughput than uIP, but also has a larger ROM and RAM footprint.
Although the footprint is larger than uIP it is still smaller than most commercial
TCP/IP offerings. In particular, lwIP saves RAM by making large data buffers by
chaining smaller buffers together.

Most (if not all) the FreeRTOS demos listed here make use of quite an old lwIP version.
There are however contributed demos available in
the [FreeRTOS Interactive forums](http://interactive.freertos.org/) that
use a more up to date lwIP code base. Further lwIP related uploads would be
gratefully received.

On the negative side, lwIP is undeniably quite complex to use at first, but time
invested in its use will pay dividends in future projects.

lwIP is also a moving target because it is constantly being
developed and updated (which is not necessarily a negative thing).


## FreeRTOS demos that include TCP/IP functionality

### Examples for Atmel microcontrollers

1. [AVR32 AT32UC3A lwIP web and TFTP server](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portAVR32#webserverexample):

   This example uses lwIP to create both a simple web and TFTP server on the AVR32 flash microcontroller.

2. [Open source lwIP TCP/IP stack on an AT91SAM7X](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7xlwIP):

 In  cludes a more comprehensive interrupt driven driver for the SAM7X integrated EMAC peripheral.

### Examples for ST microcontrollers

1. [Open source lwIP TCP/IP stack on an STR912 (ARM9)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr912iar):

   This demo includes the lwIP stack, this time targeted at an ARM9 processor.

### Examples using WizNET interfaces

1. [WizNET hardware TCP/IP stack - I2C interface](/webservedemo):

   This example uses a TCP/IP coprocessor to produce an embedded web server through the I2C port!

2. [WizNET hardware TCP/IP stack - memory mapped interface](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/portternee):

   This example uses the same TCP/IP coprocessor, but with a memory mapped interface on a Tern E-Engine
   controller.
