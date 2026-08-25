---
title: "FreeRTOS_accept()"
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
Socket_t FreeRTOS_accept( Socket_t xServerSocket,
                           struct freertos_sockaddr *pxAddress,
                           socklen_t *pxAddressLength );
```

Accept a connection on a TCP socket.
 
The socket must first have been successfully created by a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket),
bound to a port using a call to [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind), and placed into the Listening state using 
a call to [FreeRTOS\_listen()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen),
 
By default a new socket (a child socket) will be created to handle any accepted connections. The new 
socket will be returned by [FreeRTOS\_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept), and can be used immediately. The child 
socket inherits all the properties from the parent socket.
 
Optionally the FREERTOS\_SO\_REUSE\_LISTEN\_SOCKET parameter can be used with a call 
to [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt) to configure the parent socket to handle any accepted connections 
itself - without creating a child socket for this purpose. This is a useful way to save resources when 
the socket will only handle a single connection at a time. For example, if the socket is used to implement 
a telnet server that only permits one simultaneous connection.
 
FreeRTOS\_accept() has an optional timeout. The timeout defaults to ipconfigSOCK\_DEFAULT\_RECEIVE\_BLOCK\_TIME, 
and is modified using the FREERTOS\_SO\_RCVTIMEO parameter in a call to FreeRTOS\_setsockopt(). If the 
accept operation does not succeed immediately then the calling RTOS task will be held in the Blocked 
state (so that other RTOS tasks can execute) until either a connection is accepted, or the timeout expires.


 **Parameters:** 

+ *xServerSocket*

  The handle of the listening socket on which new connections are to be accepted.  

+ *pxAddress*

  A pointer to a freertos\_sockaddr structure that will be filled (by FreeRTOS\_accept()) with the IP 
  address and port number of the socket from which a connection was accepted.  

+ *pxAddressLength*

  Not currently used, but should be set to sizeof( struct freertos\_sockaddr ) to ensure future compatibility.  


**Returns:** 

+ If a connection from a remote socket is accepted and a new local socket is created to handle the accepted 
  connection then a handle to the new socket is returned.
 
+ If xServerSocket is not a valid TCP socket then FREERTOS\_INVALID\_SOCKET is returned.
 
+ If xServerSocket is not in the Listening state (see [FreeRTOS\_listen()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen)) then 
  FREERTOS\_INVALID\_SOCKET is returned.
 
+ If a timeout occurs before a connection from a remote socket is accepted then NULL is returned.
 
Note that, because FreeRTOS does not implement errno, the behaviour in the presence of an error is 
necessarily different to that of connect() functions that are fully compliant with the expected Berkeley
sockets behaviour.
 

**Example usage:** 

See the "Creating, configuring and binding a TCP server socket" source code example in 
the ["Creating Configuring and Binding TCP Client and Server Sockets"](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
section of the FreeRTOS-Plus-TCP networking tutorial.
 
