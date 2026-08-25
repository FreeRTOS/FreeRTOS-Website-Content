---
title: "xApplicationDHCPHook()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_sockets.h
  
***Note**: this hook needs to be defined only when `ipconfigUSE_DHCP_HOOK` is set to 1 in the FreeRTOSIPConfig.h file.*
  
```c
eDHCPCallbackAnswer_t xApplicationDHCPHook( eDHCPCallbackPhase_t eDHCPPhase,uint32_t ulIPAddress );
```

xApplicationDHCPHook is an application defined hook (or callback) function that is called by the 
FreeRTOS-Plus-TCP stack to check whether DHCP 'Discover' and 'Request' messages should be sent to complete 
the process of getting a dynamic IP-address or whether the device use the default static IP.

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name). The code in 
an application hook should not call FreeRTOS-Plus-TCP API's that are blocking. That could easily lead to 
a dead-lock.

When an application hook executes, it borrows the task priority and the stack of the IP-task. Therefore, 
we recommend that you keep application hooks short--it may want to wakeup some application task which 
will do further processing.


**Parameters:**

+ *eDHCPPhase*
  
  This parameter can be either eDHCPPhasePreRequest or eDHCPPhasePreDiscover when the TCP stack is about 
  to send either a Request or a Discover message, respectively.
  
+ *ulIPAddress*
  
  This parameter will contain the default IP address when the parameter eDHCPPhase is eDHCPPhasePreDiscover, 
  otherwise (when eDHCPPhase is eDHCPPhasePreRequest) it will contain the IP address offered by the DHCP 
  server.


**Return value:** 

The return value can have these enum values: 

* `eDHCPContinue` if the application wants to continue the DHCP transaction.
* `eDHCPUseDefaults` if the application wants to use the default network parameters.
* `eDHCPStopNoChanges` in case the DHCP processing must be stopped, while keeping all
  network parameters as they were before.
