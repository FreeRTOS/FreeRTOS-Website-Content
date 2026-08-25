---
title: "FreeRTOS_IsNetworkUp()"
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
BaseType_t FreeRTOS_IsNetworkUp( void );
```

Used to test if the network is currently up (connected) or down (disconnected). Note that disconnect 
events come from the network interface driver, so rely on the network interface driver for implementation.

 
**Returns:** 

pdTRUE if the network is up (connected). Otherwise pdFALSE.
 
