---
title: "FreeRTOS_AllEndPointsUp()"
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
BaseType_t FreeRTOS_AllEndPointsUp( const struct xNetworkInterface * pxInterface )
```

Used to test if all endpoints associated with an interface are currently up (connected) or down (disconnected). 
Note that disconnect events come from the network interface driver, so they rely on the network interface 
driver for implementation.


**Parameters:**

+ *pxInterface*

  Interface for which the status of its endpoints has to be checked. If NULL, the function returns whether 
  all the available endpoints regardless of interface are up or not.


**Returns:**

pdTRUE if all endpoints are up (connected). Otherwise pdFALSE.

