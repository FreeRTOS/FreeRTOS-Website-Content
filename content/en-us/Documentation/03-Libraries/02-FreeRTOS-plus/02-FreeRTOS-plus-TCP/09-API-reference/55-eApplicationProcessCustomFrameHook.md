---
title: "eApplicationProcessCustomFrameHook()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]


FreeRTOS\_sockets.h
  
**Note**: this hook needs to be defined only when `ipconfigPROCESS_CUSTOM_ETHERNET_FRAMES` is set to 1 
in the FreeRTOSIPConfig.h file.
  

```c
eFrameProcessingResult_t eApplicationProcessCustomFrameHook( NetworkBufferDescriptor_t * const pxNetworkBuffer );
```

eApplicationProcessCustomFrameHook is an application defined hook (or *callback*) function that is called 
by the FreeRTOS-Plus-TCP stack when the stack receives a frame which is not handled by the stack which 
is anything except an ARP frame or an IP packet. 

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name). The code in 
an application hook should not call FreeRTOS-Plus-TCP API's that are blocking. That could easily lead to a 
dead-lock.

When an application hook executes, it borrows the task priority and the stack of the IP-task. Therefore, 
we recommend that you keep application hooks short--it may want to wakeup some application task which 
will do further processing.


**Parameters:** 

+ *pxNetworkBuffer*

  The network buffer containing the unsupported frame.


**Return value:** 

The returned value must be of the type `eFrameProcessingResult_t`. If the frame is to be released then 
eReleaseBuffer should be returned and the network stack will take care of clean-up. If anything else is 
returned, then the user/application must release the network buffer by 
calling [vReleaseNetworkBufferAndDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/04-vReleaseNetworkBufferAndDescriptor).
