---
title: "FreeRTOS_connect()"
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
BaseType_t FreeRTOS_connect( Socket_t xClientSocket,
                             struct freertos_sockaddr *pxAddress,
                             socklen_t xAddressLength );
```

[Connect a TCP socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/06-Sending-TCP-data) to a remote socket.

The socket must first have been successfully created by a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket),
and optionally bound to a port using a call to [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).


If FreeRTOS\_connect() is called on a socket that is not bound to a port
number, and the value of [ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigallow_socket_send_without_bind)
is set to 1 in FreeRTOSIPConfig.h, then the TCP/IP stack will automatically bind the socket
to a port number from the private address range.

FreeRTOS\_connect() has an optional timeout. The timeout defaults to
ipconfigSOCK\_DEFAULT\_RECEIVE\_BLOCK\_TIME, and is modified using the
FREERTOS\_SO\_RCVTIMEO parameter in a call to FreeRTOS\_setsockopt(). If
the connect operation does not succeed immediately then the calling RTOS task
will be held in the Blocked state (so that other tasks can execute) until
either the connect request is successful, or the timeout expires.


**Parameters:**

+ *xSocket*

  The handle of the socket being bound. The socket must have already been created (see [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)).

+ *pxAddress*

  A pointer to a freertos\_sockaddr structure that contains the destination IP address and port number (the remote socket
  the local socket is attempting to connect to).

+ *xAddressLength*

  Not currently used, but should be set to sizeof( struct freertos\_sockaddr ) to ensure future compatibility.


**Returns:**

+ If the connect operation succeeded then 0 is returned.

+ If xSocket is not a valid TCP socket then -pdFREERTOS\_ERRNO\_EBADF is returned.

+ If xSocket was already connected before FreeRTOS\_connect() was called
  then -pdFREERTOS\_ERRNO\_EISCONN is returned.

+ If xSocket is not in a state that allows a connect operation then either
  -pdFREERTOS\_ERRNO\_EINPROGRESS or -pdFREERTOS\_ERRNO\_EAGAIN is returned.

+ If the socket has a read block time of zero and the connect operation
  cannot succeed immediately then -pdFREERTOS\_ERRNO\_EWOULDBLOCK is returned.

+ If the connect attempt times out then -pdFREERTOS\_ERRNO\_ETIMEDOUT is
  returned.

Note that, because FreeRTOS does not implement errno, the behaviour in the presence of an error is
necessarily different to that of connect() functions that are fully compliant with the expected Berkeley
sockets behaviour.


**Example usage:**

See the [Sending TCP Data](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/06-Sending-TCP-data) section of the FreeRTOS-Plus-TCP networking tutorial pages.
