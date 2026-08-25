---
title: "FreeRTOS_send()"
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
BaseType_t FreeRTOS_send( Socket_t xSocket,
                          const void *pvBuffer,
                          size_t xDataLength,
                          BaseType_t xFlags );
```

Send data to a TCP socket (see [FreeRTOS\_sendto()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto) for the UDP equivalent).

The socket must have already been created using a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket),
bound to a port number, and connected to a remote socket.

The socket can be explicitly bound to a port number by calling [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).

The socket can actively connect to a remote socket using [FreeRTOS\_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect).
If FreeRTOS\_connect() is called on a socket that is not bound to a port number, and the value
of [ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigallow_socket_send_without_bind)
is set to 1 in FreeRTOSIPConfig.h, then the TCP/IP stack will automatically bind the socket to a port
number from the private address range.

Alternatively the socket can wait for incoming connections using [FreeRTOS\_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept).

FreeRTOS\_send() has an optional timeout. The timeout defaults
to [ipconfigSOCK\_DEFAULT\_SEND\_BLOCK\_TIME](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME),
and is modified using the FREERTOS\_SO\_SNDTIMEO parameter in a call to [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt).
If the send operation cannot queue the bytes for transmission immediately then the calling RTOS task
will be held in the Blocked state (so that other tasks can execute) until either the bytes can be queued
for sending, or the timeout expires.

FreeRTOS-Plus-TCP does not [currently] use all the function parameters. The parameters that are not used
are retained in the function's prototype to ensure consistency with the expected standard Berkeley sockets
API, and to ensure compatibility with future versions of FreeRTOS-Plus-TCP.


**Parameters:**

+ *xSocket*

  The handle of the socket to which data is being sent. The socket must have already been created and
  bound to a port number (see [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) and [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind)).


+ *pvBuffer*

  Points to the source of the data being transmitted.


+ *xDataLength*

  The number of bytes to send.


+ *xFlags*

  Not currently used. Future FreeRTOS-Plus-TCP versions may implement send options using the ulFlags
  parameter.


**Returns:**

+ If the send was successful then the number of bytes queued for sending is returned (note this may be
  fewer bytes than the number requested by the xTotalDataLength parameter).

+ If no data could be sent because the socket was closed or got closed then -pdFREERTOS\_ERRNO\_ENOTCONN
  is returned.

+ If no data could be sent because there was insufficient memory then -pdFREERTOS\_ERRNO\_ENOMEM is returned.

+ If no data could be sent because xSocket was not a valid TCP socket then -pdFREERTOS\_ERRNO\_EINVAL
  is returned.

+ If a timeout occurred before any data could be sent then -pdFREERTOS\_ERRNO\_ENOSPC is returned.

Note that, because FreeRTOS does not implement errno, the behaviour in the presence of an error is
necessarily different to that of send() functions that are fully compliant with the expected Berkeley
sockets behaviour.


**Example usage:**

See the ["Creating, Configuring and Binding TCP Client and Server Sockets"](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
 section of the FreeRTOS-Plus-TCP networking tutorial pages for examples of how to prepare a TCP socket
 for sending data.

See the ["Sending TCP Data"](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/06-Sending-TCP-data) section of the FreeRTOS-Plus-TCP
networking tutorial pages for examples of sending data to a TCP socket.
