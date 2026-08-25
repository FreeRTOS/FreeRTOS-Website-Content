---
title: "FreeRTOS_CreateSocketSet()"
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
SocketSet_t FreeRTOS_CreateSocketSet( void );
```

Create a socket set for use with the [FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select) function. ipconfigSUPPORT\_SELECT\_FUNCTION 
must be set to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSUPPORT_SELECT_FUNCTION)
for FreeRTOS\_CreateSocketSet() to be available.
 
*Socket Sets* allow an application RTOS task to block on multiple sockets simultaneously.
 
To use a socket set:

1. Create a socket set by calling FreeRTOS\_CreateSocketSet().

   A socket set is equivalent to the Berkeley sockets fd\_set type.

2. Add one or more sockets to the set using calls to [FreeRTOS\_FD\_SET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/16-FD_SET).

   FreeRTOS\_FD\_SET() is equivalent to the Berkeley sockets FD\_SET() macro.

3. Call [FreeRTOS\_Select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select) to test the sockets in the set to see if any of the sockets 
   have an event pending.

4. If FreeRTOS\_select() returns a non-zero value then check all sockets in the set using a call 
   to [FreeRTOS\_FD\_ISSET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/18-FD_ISSET) to determine which events are pending.

The [FreeRTOS\_FD\_CLR()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/17-FD_CLR) API function is used to remove a socket from a socket set.


**Returns:** 

If the socket set was created then a handle to the created socket set is returned. If the socket set 
was not created (because there was insufficient [FreeRTOS heap memory available](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)) 
then NULL is returned.
 

**Example usage:** 

See the example on the [FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select) documentation page.
