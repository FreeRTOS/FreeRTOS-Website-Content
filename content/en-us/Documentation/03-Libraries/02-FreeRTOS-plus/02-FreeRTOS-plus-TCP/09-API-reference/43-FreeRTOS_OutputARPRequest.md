---
title: "FreeRTOS_OutputARPRequest()"
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
void FreeRTOS_OutputARPRequest( uint32_t ulIPAddress );
```

Forces an [ARP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/06-ARP) request to be sent for a given IP address.
 

**Parameters:** 

+ *ulIPAddress*

  The IP address for which an ARP request will be sent.


**Returns:** 

void
 
