---
title: "ulApplicationGetNextSequenceNumber()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_sockets.h

```c
uint32_t ulApplicationGetNextSequenceNumber( uint32_t ulSourceAddress,
                                             uint16_t usSourcePort,
                                             uint32_t ulDestinationAddress,
                                             uint16_t usDestinationPort );
```

ulApplicationGetNextSequenceNumber is an application defined hook (or callback) function that is called 
by the FreeRTOS-Plus-TCP stack to get a difficult to predict sequence number for the 4-value address 
tuple for a TCP connection.

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name).


**Parameters:**

+ *ulSourceAddress*
  
  The IPv4 address of the device.
 
+ *usSourcePort*
  
  The port number of the device to which the TCP socket is bound.
 
+ *ulDestinationAddress*
  
  The IPv4 address of the peer.
 
+ *usDestinationPort*
  
  The port of the peer to which the TCP connection is being made.
  

**Return value:** 

A 32-bit hard to predict number should be returned by this hook to be used as the initial sequence number 
for the TCP connection.
