---
title: "FreeRTOS_GetUDPPayloadBuffer()"
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
void *FreeRTOS_GetUDPPayloadBuffer( size_t xRequestedSizeBytes, TickType_t xBlockTimeTicks );
```

Obtains a buffer from the TCP/IP stack for use with the zero copy interface.
 
The zero copy interface for transmitting data is described on the [FreeRTOS\_sendto() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto).
 

**Parameters:** 
 
+ *xRequestedSizeBytes* 
  
  The size of the buffer being requested. The size is specified in bytes.
 
+ *xBlockTimeTicks* 
  
  The maximum time the calling RTOS task is prepared to wait for a buffer if one is not immediately 
  available.
 
  If a buffer is not available then the calling RTOS task will be held in the Blocked state (so other 
  tasks can execute) until either a buffer becomes available or the block time expires.
 
  The block time is specified in ticks. Milliseconds can be converted to ticks by dividing the time 
  in milliseconds by portTICK\_PERIOD\_MS.
 
  To prevent deadlocks the maximum block time is capped to ipconfigMAX\_SEND\_BLOCK\_TIME\_TICKS. 
  ipconfigMAX\_SEND\_BLOCK\_TIME\_TICKS is defined in FreeRTOSIPConfig.h
 
 
**Returns:** 

+ If a buffer was obtained then a pointer to the obtained buffer is returned.
 
+ If a buffer could not be obtained then NULL is returned.
 

**Example usage:** 

The [FreeRTOS\_sendto() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto) contains an example zero copy send operation 
that includes a call to FreeRTOS\_GetUDPPayloadBuffer().
 
