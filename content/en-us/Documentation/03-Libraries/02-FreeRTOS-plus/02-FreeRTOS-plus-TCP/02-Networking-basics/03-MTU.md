---
title: MTU and MTU Size
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### MTU

MTU stands for [Maximum Transmission Unit](http://en.wikipedia.org/wiki/Maximum_transmission_unit)
and is a characteristic of the hardware (physical layer).
MTU sizes are specified in octets (8-bit values).


### MTU Size

The MTU size defines the maximum size that a packet or frame
sent onto the network or received from the network can be.
If the application sends a small block of data that fits in
one frame then only one frame will be sent onto the network.
If the application sends a block of data that is larger than
the MTU size the data will be split into multiple packets,
each of which will create a frame of less than or equal to
the MTU size.

In FreeRTOS-Plus-TCP the MTU is specified in bytes and set by
the [ipconfigNETWORK\_MTU](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigNETWORK_MTU) setting in
FreeRTOSIPConfig.h. Check the specification for your MAC or
Ethernet hardware to find the correct setting for your system.
Some MAC devices are restricted to 1400.

See also [MSS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/11-MSS).
