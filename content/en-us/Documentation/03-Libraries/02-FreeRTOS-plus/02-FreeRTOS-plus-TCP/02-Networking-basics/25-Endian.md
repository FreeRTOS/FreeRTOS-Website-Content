---
title: "Little Endian, Big Endian"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


Different MCUs store multi byte values, such as a two byte
uint16\_t or a four byte uint32\_t, in different ways. Microcontrollers that
store the most significant byte first are called big endian. Microcontrollers
that store the least significant byte first are called little endian.
The way bytes are stored on the MCU on which FreeRTOS-Plus-TCP is running
is called the *host byte order*.

It is rare for the writer of a non connected application to need to concern
themselves with how their target MCU stores data internally.
If data is written to memory in little endian order, it will be read back
from memory in little endian order - and so the value read back will
match the value originally written.

It is more complicated when MCUs are connected, because there
are no guarantees that all the MCUs on a connected network
will have the same byte order. All the MCUs on the network
have to agree the byte order used to send and receive data in advance.
The byte order used for data in transit is called the *network byte
order*.

In [TCP/IP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)
networks data is sent most significant byte first,
making TCP/IP networks effectively big endian. Therefore,
a little endian MCU sending to a TCP/IP network must swap the
order in which bytes appear within multi byte values before the values
are sent onto the network, and must swap the order in which bytes
appear in multi byte values received from the network before the values
are used. A big endian MCUs does not need to perform any
byte swapping because the endian of the MCU (the host byte
order) matches the agreed endian of the network (the network byte order).

**NOTE:** The byte swapping is performed by the TCP/IP stack - the user
 does not need to swap bytes manually.
