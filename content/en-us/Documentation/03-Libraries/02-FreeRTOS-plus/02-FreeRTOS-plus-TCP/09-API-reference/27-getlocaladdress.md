---
title: "FreeRTOS_GetLocalAddress()"
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
size_t FreeRTOS_GetLocalAddress( ConstSocket_t xSocket, 
                                 struct freertos_sockaddr * pxAddress );
```

Returns the local IP address and the port of a bound socket.
 

**Parameters:** 


+ *xSocket*

  The socket being queried.  

+ *pxAddress*

  A freertos\_sockaddr structure in which the local address details are returned.  


**Returns:** 

Always returns sizeof( freertos\_sockaddr ).
 
