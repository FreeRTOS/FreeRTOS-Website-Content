---
title: "FreeRTOS_SignalSocket()"
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
BaseType_t FreeRTOS_SignalSocket( Socket_t xSocket );

BaseType_t FreeRTOS_SignalSocketFromISR( Socket_t xSocket,
                                         BaseType_t *pxHigherPriorityTaskWoken );
```

Used to send a signal to a socket, the result of which is that any task blocked on a read from the 
socket will leave the Blocked state (abort the blocking operation), with the task's read 
operation ([FreeRTOS\_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv) or [FreeRTOS\_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom)) returning -pdFREERTOS\_ERRNO\_EINTR.
 
If the socket is part of a socket set (SocketSet\_t), the call to [FreeRTOS\_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select)
using that socket set, will also get interrupted and return eSELECT\_INTR.
 
FreeRTOS\_SignalSocketFromISR() is a version of FreeRTOS\_SignalSocket() that can be used from an interrupt 
service routine (ISR).
 

[ipconfigSUPPORT\_SIGNALS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSUPPORT_SIGNALS) must be set to 1 in 
FreeRTOSIPConfig.h for FreeRTOS\_SignalSocket() to be available.
 

**Parameters:** 

 
+ *xSocket* 
  
  The socket to which the signal is being sent.


+ *pxHigherPriorityTaskWoken* 
  
  \[FreeRTOS\_SignalSocketFromISR() only.\]
 
  `pxHigherPriorityTaskWoken` must be initialised to 0.
 
  FreeRTOS\_SignalSocketFromISR() will set *pxHigherPriorityTaskWoken to pdTRUE if sending the signal 
  to the socket caused a task to unblock, and the unblocked task has a priority higher than the
  currently running task.
 
  If FreeRTOS\_SignalSocket() sets this value to pdTRUE then a context switch should be requested before 
  the interrupt is exited. The name of the macro used to request a context switch from an ISR is dependent 
  on the port, and will be called either portYIELD\_FROM\_ISR() or portEND\_SWITCHING\_ISR(). Refer to the 
  documentation and examples provided for the port in use.
 
 
**Returns:** 

If xSocket is not a valid socket then -pdFREERTOS\_ERRNO\_EINVAL is returned. Otherwise 0 is returned.
 
