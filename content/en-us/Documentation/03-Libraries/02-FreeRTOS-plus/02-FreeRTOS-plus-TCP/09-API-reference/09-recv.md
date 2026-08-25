---
title: "FreeRTOS_recv()"
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
BaseType_t FreeRTOS_recv( Socket_t xSocket,
                          void *pvBuffer,
                          size_t xBufferLength,
                          BaseType_t xFlags );
```
Receive data from a TCP socket (see [FreeRTOS\_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom) for the UDP equivalent).

The socket must have already been created using a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket), bound to a
port number, and connected to a remote socket.

The socket can be explicitly bound to a port number by calling [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).

The socket can actively connect to a remote socket using [FreeRTOS\_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect).
If FreeRTOS\_connect() is called on a socket that is not bound to a port number, and the value
of [ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigallow_socket_send_without_bind)
is set to 1 in FreeRTOSIPConfig.h, then the TCP/IP stack will automatically bind the socket
to a port number from the private address range.

Alternatively the socket can wait for incoming connections using [FreeRTOS\_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept).

FreeRTOS\_recv() has an optional timeout. The timeout defaults
to [ipconfigSOCK\_DEFAULT\_RECEIVE\_BLOCK\_TIME](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigsock_default_receive_block_time),
and is modified using the FREERTOS\_SO\_RCVTIMEO parameter in a call
to [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt). If the receive operation cannot return received bytes
immediately then the calling RTOS task will be held in the Blocked state (so that other tasks
can execute) until either bytes are received, or the timeout expires.

FreeRTOS-Plus-TCP does not [currently] use all the function parameters. The parameters that are not
used are retained in the function's prototype to ensure consistency with the expected standard Berkeley
sockets API, and to ensure compatibility with future versions of FreeRTOS-Plus-TCP.


**Parameters:**

+ *xSocket*

  The handle of the socket from which data is being read.

+ *pvBuffer*

  The buffer into which received data will be placed.

+ *xBufferLength*

  The size of the buffer (in bytes) pointed to by the pvBuffer parameter - and therefore also the maximum
  number of bytes that will be read.

+ *ulFlags*

  Not currently used. Future FreeRTOS-Plus-TCP versions may implement receive options using the ulFlags
  parameter.


**Returns:**

+ If the receive was successful then the number of bytes received (placed in the buffer pointed to by
  pvBuffer) is returned.

+ If a time out occurred before data could be received then 0 is returned.

+ If there was not enough memory for the socket to be able to create either an Rx or Tx stream
  then -pdFREERTOS\_ERRNO\_ENOMEM is returned.

+ If the socket was closed or got closed then -pdFREERTOS\_ERRNO\_ENOTCONN is returned.

+ If the [socket received a signal](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket), causing the read operation to be aborted,
  then -pdFREERTOS\_ERRNO\_EINTR is returned.

+ If the socket is not valid, is not a TCP socket, or is not bound then -pdFREERTOS\_ERRNO\_EINVAL is returned;

Note that, because FreeRTOS does not implement errno, the behaviour in the presence of an error is
necessarily different to that of recv() functions that are fully compliant with the expected Berkeley
sockets behaviour.


**Example usage:**

See the ["Creating, Configuring and Binding TCP Client and Server Sockets"](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
 section of the FreeRTOS-Plus-TCP networking tutorial pages for examples of how to prepare a TCP socket
 for receiving data.

See the ["Receiving TCP Data"](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/07-Receiving-TCP-data) section of the FreeRTOS-Plus-TCP
networking tutorial pages for examples of receiving data from a TCP socket.
