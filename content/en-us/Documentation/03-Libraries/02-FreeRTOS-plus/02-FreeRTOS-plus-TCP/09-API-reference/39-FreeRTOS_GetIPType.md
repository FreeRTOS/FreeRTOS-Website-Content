---
title: "FreeRTOS_GetIPType()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_Sockets.h

```c
BaseType_t FreeRTOS_GetIPType( ConstSocket_t xSocket );
```

Get the version of IP- either 'ipTYPE_IPv4' or 'ipTYPE\_IPv6'.


**Parameters:**

+ *xSocket*

  The socket to be checked.


**Returns:**

Either ipTYPE_IPv4 or ipTYPE_IPv6.

