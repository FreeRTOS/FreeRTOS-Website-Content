---
title: "FreeRTOS_inet_ntoa()"
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
void FreeRTOS_inet_ntoa( uint32_t ulIPAddress, uint8_t *pucBuffer )
```

A macro that converts an IP address expressed as a 32-bit number in network byte order
to a string in decimal dot notation (for example "192.168.0.200").
 
The standard Berkeley sockets inet\_ntoa() function returns a pointer to a string that is
normally stored in a global buffer. FreeRTOS\_inet\_ntoa() deviates from
the normal semantics by instead taking the buffer into which the string is written as a
parameter. The deviation is to ensure the macro is re-entrant and thread aware.
 

**Parameters:** 

+ *ulIPAddress*

  An IP address expressed as a 32-bit value in network byte order.  

+ *pucBuffer*

  A pointer to a buffer into which the IP address will be written in decimal dot notation.  


**Example usage:** 

The example on the [FreeRTOS\_recvfrom() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom) demonstrates
FreeRTOS\_inet\_ntoa() being used to print the IP address from which a message was received.
 
The example on the [FreeRTOS\_GetAddressConfiguration() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/32-FreeRTOS_GetAddressConfiguration)
demonstrates FreeRTOS\_inet\_ntoa() being used to print out the network configuration - including the 
IP address and net mask of the node, and the IP addresses of the gateway and DNS server respectively.
