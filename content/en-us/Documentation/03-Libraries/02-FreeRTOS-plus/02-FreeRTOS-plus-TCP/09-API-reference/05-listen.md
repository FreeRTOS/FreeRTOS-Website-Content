---
title: "FreeRTOS_listen()"
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
BaseType_t FreeRTOS_listen( Socket_t xSocket, BaseType_t xBacklog );
```

Places a TCP socket into a state where it is listening for and can accept incoming connection requests 
from remote sockets.
 
The socket must first have been successfully created by a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket),
and bound to a port using a call to [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).
 
By default a new socket (a child socket) will be created to handle any accepted connections. The new 
socket will be returned by [FreeRTOS\_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept), and can be used immediately. The child 
socket inherits all the properties from the parent socket.
 
Optionally the FREERTOS\_SO\_REUSE\_LISTEN\_SOCKET parameter can be used with a call 
to [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt) to configure the parent socket to handle any accepted connections 
itself - without creating a child socket for this purpose. This is a useful way to save resources when 
the socket will only handle a single connection at a time. For example, if the socket is used to implement 
a telnet server that only permits one simultaneous connection.
 

**Parameters:** 

+ *xSocket*

  The handle of the socket being placed into the Listening state. The socket must have already been 
  created using a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)) and bound to a port number using a call 
  to [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind))  

+ *xBacklog* 

  In the default case where a new socket is created for each new connection the backlog value puts a 
  limit on the number of simultaneously connected clients.  


**Returns:** 

+ If the socket was successfully placed into the listening state then 0 is returned.
 
+ If xSocket is not a valid TCP socket then -pdFREERTOS\_ERRNO\_EOPNOTSUPP is returned.
 
+ If xSocket is not in bound but closed state then -pdFREERTOS\_ERRNO\_EOPNOTSUPP is returned.
 
Note that, because FreeRTOS does not implement errno, the behaviour in the presence of an error is 
necessarily different to that of connect() functions that are fully compliant with the expected Berkeley
sockets behaviour.
 

**Example usage:** 

See the "Creating, configuring and binding a TCP server socket" source code example in 
the ["Creating Configuring and Binding TCP Client and Server Sockets"](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
section of the FreeRTOS-Plus-TCP networking tutorial pages.
 
