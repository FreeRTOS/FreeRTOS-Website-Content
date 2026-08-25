---
title: "xApplicationDNSQueryHook_Multi()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_sockets.h

**Note**: this hook needs to be defined only when ipconfigUSE_NBNS or ipconfigUSE_LLMNR is set to 1 
in the FreeRTOSIPConfig.h file.

```c
BaseType_t xApplicationDNSQueryHook_Multi( struct xNetworkEndPoint * pxEndPoint,
                                           const char * pcName );
```

`xApplicationDNSQueryHook_Multi` is an application defined hook (or callback) function that is called 
by the FreeRTOS-Plus-TCP stack to check whether the LLMNR or NBNS name received is the same as the one 
device is looking for.

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name). The code 
in an application hook should not call FreeRTOS-Plus-TCP API's that are blocking. That could easily 
lead to a dead-lock.

When an application hook executes, it borrows the task priority and the stack of the IP-task. Therefore, 
we recommend that you keep application hooks short—it may want to wakeup some application task which 
will do further processing.


**Parameters:**

+ *pxEndPoint*

  The pxEndPoint represents the end-point for which `xApplicationDNSQueryHook_Multi` is called.

+ *pcName*

  The name received by the TCP/IP stack.


**Return value:**

If the value in pcName matches the name of the device, then pdTRUE should be returned by the hook. 
Otherwise, a pdFALSE should be returned.
 
