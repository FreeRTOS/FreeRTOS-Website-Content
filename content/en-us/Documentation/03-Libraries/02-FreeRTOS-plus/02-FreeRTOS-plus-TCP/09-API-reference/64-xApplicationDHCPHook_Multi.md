---
title: "xApplicationDHCPHook_Multi()"
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
eDHCPCallbackAnswer_t xApplicationDHCPHook_Multi( eDHCPCallbackPhase_t eDHCPPhase,
                                                  struct xNetworkEndPoint * pxEndPoint,
                                                  IP_Address_t * pxIPAddress 
                                                );
```

`xApplicationDHCPHook_Multi` is an application defined hook (or callback) function that is called by 
the FreeRTOS-Plus-TCP stack to check whether DHCPv4 'Discover' and 'Request' or DHCPv6 'Solicitation' 
and 'Request' messages should be sent to complete the process of getting a dynamic IP-address, or whether 
the device uses the default static IP.

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name). The code in 
an application hook should not call FreeRTOS-Plus-TCP API's that are blocking. That could easily lead to 
a dead-lock.

When an application hook executes, it borrows the task priority and the stack of the IP-task. Therefore, 
we recommend that you keep your application hook short—it may want to wake up some application task 
which will do further processing.


**Parameters:**

+ *eDHCPPhase*

  For DHCPv4, this parameter can be either eDHCPPhasePreRequest or eDHCPPhasePreDiscover when the TCP 
  stack is about to send either a Request or a Discover message, respectively. For DHCPv6, this parameter 
  can be either eDHCPPhasePreRequest or eDHCPPhasePreDiscoverwhen the TCP stack is about to send either 
  a Solicitation or Request message, respectively.

+ *pxEndPoint*

    The end-point currently executes the DHCP(v4 or v6).

+ *pxIPAddress*

  This parameter will contain the default IP address when the parameter eDHCPPhase is eDHCPPhasePreDiscover, 
  otherwise (when eDHCPPhase is eDHCPPhasePreRequest) it will contain the IP address offered by the DHCP server.


**Return value:**

The return value can be one of these enum values:

+ `eDHCPContinue` if the application wants to continue the DHCP transaction.
+ `eDHCPUseDefaults` if the application wants to use the default network parameters.
+ `eDHCPStopNoChanges` in case the DHCP processing must be stopped, while keeping all network parameters 
  as they were before.
 
