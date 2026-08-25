---
title: "FreeRTOS_shutdown()"
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
BaseType_t FreeRTOS_shutdown( Socket_t xSocket, BaseType_t xHow );
```

Disable reads and writes on a connected TCP socket. A connected TCP socket must be gracefully shut down before it can be
closed.


**Parameters:**


+ *xSocket*

  The socket being shut down.


+ *xHow*

  Must be set to FREERTOS\_SHUT\_RDWR.

  FreeRTOS-Plus-TCP does not currently use the xHow parameter as it always shuts down both reads and
  writes. xHow is included to ensure the function prototype conforms to the expected Berkeley sockets
  standard, and for compatibility with future FreeRTOS-Plus-TCP versions which may accept other parameter
  values.


**Returns:**

+ If the shutdown request was successful then 0 is returned. The shutdown being complete is indicated
  by [FreeRTOS\_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv) calls on the socket resulting in -pdFREERTOS\_ERRNO\_EINVAL being returned.

+ If xSocket is not a valid TCP socket then -pdFREERTOS\_ERRNO\_EOPNOTSUPP is returned.

+ If xSocket is a valid TCP socket but the socket is not connected to a remote socket
  then -pdFREERTOS\_ERRNO\_EOPNOTSUPP is returned.

Note that, because FreeRTOS does not implement errno, the behaviour in the presence of an error is
necessarily different to that of connect() functions that are fully compliant with the expected Berkeley
sockets behaviour.


**Example usage:**

The source code examples on both the [Sending TCP Data](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/06-Sending-TCP-data) and the [Receiving TCP Data](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/07-Receiving-TCP-data) pages demonstrate a connected
socket being shut down then closed.
