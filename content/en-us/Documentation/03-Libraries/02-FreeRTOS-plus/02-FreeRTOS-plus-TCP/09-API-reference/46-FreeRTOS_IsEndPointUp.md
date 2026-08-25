---
title: "FreeRTOS_IsEndPointUp()"
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
BaseType_t FreeRTOS_IsEndPointUp( const struct xNetworkEndPoint * pxEndPoint )
```

Used to test if the endpoint (pxEndPoint) is currently up (connected) or down (disconnected). Note that 
disconnect events come from the network interface driver, so they rely on the network interface driver 
for implementation. If pxEndPoint is NULL, the function returns whether all endpoints are up or not.


**Parameters:**

+ *pxEndPoint*

  Endpoint of interest, if NULL status of all endpoints will be checked.


**Returns:**

pdTRUE if the given endpoint (or all endpoints if pxEndPoint is NULL) is up (connected). Otherwise pdFALSE.

