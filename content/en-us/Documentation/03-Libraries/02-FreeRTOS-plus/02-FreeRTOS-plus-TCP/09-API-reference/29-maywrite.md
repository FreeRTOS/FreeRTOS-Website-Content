---
title: "FreeRTOS_maywrite()"
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
BaseType_t FreeRTOS_maywrite( Socket_t xSocket );
```

Returns the number of bytes that can be added to a TCP socket's Tx stream before the Tx stream is full.
 

**Parameters:** 

+ *xSocket*

  The socket being queried.


**Returns:** 

+ If the socket referenced by the xSocket parameter is not a TCP socket then -pdFREERTOS\_ERRNO\_EINVAL is returned.
 
+ If the socket is not in a state that allows data to be sent (for example it is in the Listening state or 
  is in the process of being shut down) then -1 is returned.
 
+ If the socket is in the Established state the returned value is the number of bytes that can be added 
  to the socket's Tx stream.
 
