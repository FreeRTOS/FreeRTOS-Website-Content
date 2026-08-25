---
title: "FreeRTOS_GetGatewayAddress()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_IP.h

```c
uint32_t FreeRTOS_GetGatewayAddress( void );
```


**Returns:** 

Returns the IP address of the [gateway](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/08-Router) in network byte order.  [FreeRTOS\_inet\_ntoa()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/20-inet_ntoa)
can be used to convert the IP address into a more easily readable decimal dot notation ASCII string.
 
