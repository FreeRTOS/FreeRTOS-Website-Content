---
title: "FreeRTOS_ReleaseUDPPayloadBuffer()"
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
void FreeRTOS_ReleaseUDPPayloadBuffer( void *pvBuffer );
```

FreeRTOS\_ReleaseUDPPayloadBuffer() is used to return to the TCP/IP stack a buffer that was used with 
the zero copy interface.
 
The zero copy interface for transmitting data is described on the [FreeRTOS\_sendto() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto).
 
The zero copy interface for receiving data is described on the [FreeRTOS\_recvfrom() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom).
 
A buffer needs to be returned to the stack if:

1. It is obtained from a call to FreeRTOS\_recvfrom() and the data it contains is no longer required, or

2. It was obtained from a call to [FreeRTOS\_GetUDPPayloadBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/34-FreeRTOS_GetUDPPayloadBuffer) but 
   the buffer could not be passed into the TCP/IP stack (the call to FreeRTOS\_sendto() in which the 
   buffer was used failed).

A buffer can also be re-used rather than returned to the TCP/IP stack.

 
**Parameters:** 

+ *pvBuffer*

  The buffer that is being returned to the TCP/IP stack.


**Example usage:** 

The [FreeRTOS\_sendto() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto) includes an example zero copy send operation that 
demonstrates how to use FreeRTOS\_ReleaseUDPPayloadBuffer() when the send operation fails.
 
The [FreeRTOS\_recvfrom() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom) includes an example that demonstrates how to 
use FreeRTOS\_ReleaseUDPPayloadBuffer() to release a buffer obtained from a call to FreeRTOS\_recvfrom().
 
