---
title: "pcApplicationHostnameHook()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_sockets.h
  
**Note**: this hook needs to be defined only when `ipconfigDHCP_REGISTER_HOSTNAME` is set to 1 in the FreeRTOSIPConfig.h file.
  
```c
const char * pcApplicationHostnameHook( void );
```
eApplicationHostnameHook is an application defined hook (or callback) function that is called by the 
FreeRTOS-Plus-TCP stack when an IP-address is requested from a DHCP server. This allows the device to 
register its hostname with the DHCP server.

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name). The code in 
an application hook should not call FreeRTOS-Plus-TCP API's that are blocking. That could easily lead to a 
dead-lock.

When an application hook executes, it borrows the task priority and the stack of the IP-task. Therefore, 
we recommend that you keep application hooks short--it may want to wakeup some application task which will 
do further processing.


**Return value:** 

A NULL terminated hostname which the device can send to register with the DHCP server. The maximum length 
of the hostname can be 32 characters.
