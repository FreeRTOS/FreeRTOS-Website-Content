---
title: "FreeRTOS_issocketconnected()"
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
BaseType_t FreeRTOS_issocketconnected( Socket_t xSocket );
```

Tests to see if a socket is connected.
 

**Parameters:** 

+ *xSocket* 

  The socket being queried.


**Returns:** 

+ If the socket referenced by the xSocket parameter is not a TCP socket then -pdFREERTOS\_ERRNO\_EINVAL is returned.
 
+ If the socket is in the Established or a FIN wait state then pdTRUE is returned. Otherwise pdFALSE is returned;
 
