---
title: "vApplicationPingReplyHook()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_IP.h

```c
void vApplicationPingReplyHook( ePingReplyStatus_t eStatus, uint16_t usIdentifier );
```

vApplicationPingReplyHook() is an application defined hook (or *callback*) function that is called by 
the TCP/IP stack when the stack receives a reply to an ICMP echo (ping) request that was generated using
the [FreeRTOS\_SendPingRequest()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/36-FreeRTOS_SendPingRequest) function.
 
Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name).
 

**Parameters:** 

+ *eStatus* 
  
  eStatus will be set (by the TCP/IP stack) to one of the following values:
 
  + eSuccess
   
    The echo reply was received correctly.
  
  + eInvalidChecksum
   
    The data received in the echo reply matched that sent in the echo request, but the reply had an 
    incorrect checksum.
  
  + eInvalidData
   
    The data received in the echo reply did not match that sent in the echo request.
  
+ *usIdentifier* 
  
  The identifier received in the echo reply.
 
  Each echo request has a unique identifier to allow replies to be matched to the requests. The 
  FreeRTOS\_SendPingRequest() function returns the identifier of the outgoing echo request it generated.
 
 
**Example usage:** 

The example on the [FreeRTOS\_SendPingRequest()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/36-FreeRTOS_SendPingRequest) documentation page includes 
an example implementation of vApplicationPingReplyHook().
