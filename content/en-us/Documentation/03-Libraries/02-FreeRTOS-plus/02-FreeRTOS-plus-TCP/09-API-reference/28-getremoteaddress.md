---
title: "FreeRTOS_GetRemoteAddress()"
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
BaseType_t FreeRTOS_GetRemoteAddress( Socket_t xSocket, struct freertos_sockaddr *pxAddress );
```

Returns the remote IP address and port of a connected TCP socket.
 

**Parameters:** 

+ *xSocket*

  The socket being queried.  

+ *pxAddress*

  A freertos\_sockaddr structure in which the remote address details are returned.  


**Returns:** 

+ If the socket referenced by the xSocket parameter is not a TCP socket then -pdFREERTOS\_ERRNO\_EINVAL is returned.
 
+ In all other cases sizeof( freertos\_sockaddr ) is returned, and pxAddress-\>sin\_addr will be set to 
  the IP address of the remote connected socket, and pxAddress-\>sin\_port will be set to the TCP port
  number of the remote connected socket.
 
