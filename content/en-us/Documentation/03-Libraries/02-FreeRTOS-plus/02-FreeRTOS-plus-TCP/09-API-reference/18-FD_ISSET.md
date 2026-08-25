---
title: "FreeRTOS_FD_ISSET()"
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
BaseType_t FreeRTOS_FD_ISSET( Socket_t xSocket, SocketSet_t xSocketSet );
```

Check if a socket in a socket set has an event bit set. ipconfigSUPPORT\_SELECT\_FUNCTION must be set 
to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSUPPORT_SELECT_FUNCTION) for 
FreeRTOS\_FD\_ISSET() to be available.
 
*Socket Sets* allow an application RTOS task to block on multiple sockets simultaneously.
 
To use a socket set:

1. Create a socket set by calling [FreeRTOS\_CreateSocketSet()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/15-createsocketset).

   A socket set is equivalent to the Berkeley sockets fd\_set type.

2. Add one or more sockets to the set using calls to [FreeRTOS\_FD\_SET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/16-FD_SET).

   FreeRTOS\_FD\_SET() is equivalent to the Berkeley sockets FD\_SET() macro.

3. Call [FreeRTOS\_Select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select) to test the sockets in the set to see if any of the sockets 
   have an event pending.

4. If FreeRTOS\_select() returns a non-zero value then check all sockets in the set using a call 
   to FreeRTOS\_FD\_ISSET() to determine which events are pending.

The event bits of interest are a bitwise OR combination of one or more of the following values:

+ eSELECT\_READ

  For a socket that is reading data, the eSELECT\_READ event will be pending in a socket as long as 
  the socket contains unread data.  For a socket that is listening for new connections, the eSELECT\_READ 
  event will be pended each time a new connection is received.  

+ eSELECT\_WRITE

  The eSELECT\_WRITE event will remain pending as long as the socket has space for writing.  If a TCP 
  socket is actively connecting to a pear the eSELECT\_WRITE event will be triggered as soon as the 
  connection is established.  One the eSELECT\_WRITE event has been pended it should either be disabled, 
  or the caller should write enough data to the socket so as to completely fill up the transmit buffer - 
  otherwise the pending eSELECT\_WRITE event will not be cleared.  

+ eSELECT\_EXCEPT

  The eSELECT\_EXCEPT event will become pending if the socket gets disconnected. 

The [FreeRTOS\_FD\_CLR()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/17-FD_CLR) API functions clears event bits of interest and removes a socket 
from a set.
 

**Parameters:** 

+ *xSocket*

  The socket within the socket set being tested to see if it has any event bits set.  

+ *xSocketSet*

  The socket set to which the socket is being added.  


**Returns:** 

The function returns a bit-mask of the values eSELECT\_READ (1), eSELECT\_WRITE (2) and eSELECT\_EXCEPT (4). 
Only the bits of interest specified using calls to [FreeRTOS\_FD\_SET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/16-FD_SET) will be returned.
 

**Example usage:** 

See the example on the [FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select) documentation page.
