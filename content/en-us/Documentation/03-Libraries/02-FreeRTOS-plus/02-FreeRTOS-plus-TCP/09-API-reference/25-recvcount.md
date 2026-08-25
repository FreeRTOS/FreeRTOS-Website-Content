---
title: "FreeRTOS_recvcount()"
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
BaseType_t FreeRTOS_recvcount( Socket_t xSocket );
```

Returns the number of bytes in a TCP socket's Rx stream that are yet to be read.
 

**Parameters:** 

+ *xSocket* 

  The socket being queried.


**Returns:** 

+ If the socket referenced by the xSocket parameter is not a TCP socket then -pdFREERTOS\_ERRNO\_EINVAL 
  is returned.
 
+ If the socket referenced by the xSocket parameter does not yet have an Rx stream then 0 is returned 
  (the Rx stream is not created until it is required).
 
+ In all other cases the returned value is the number of bytes that remain in the socket's Rx stream.
 
