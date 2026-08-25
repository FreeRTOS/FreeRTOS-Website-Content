---
title: "FreeRTOS_SetNetmask()"
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
void FreeRTOS_SetNetmask( uint32_t ulNetmask );
```

This function can be used to update the IPv4 subnet mask used by the FreeRTOS-Plus-TCP device after the 
TCP stack has already been initialized with a call to [FreeRTOS\_IPInit()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/30-FreeRTOS_IPInit).


**Parameters:**

+ *`ulNetmask`*

  The 32-bit IPv4 netmask, in network endian order, which the device should 
  use. [FreeRTOS\_htonl](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/23-htons_ntohs_htonl_ntohl)<br/> can be used to get the network endian representation 
  of the 32-bit IP netmask.


**Caution:**

This function is not thread safe and should be used with the `taskENTER_CRITICAL/taskEXIT_CRITICAL` 
pair. A call to this function should be made only when there is no active connection (either UDP or 
TCP), or else that connection might be severed.


**Example usage:**

See the [FreeRTOS\_SetIPAddress](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/50-FreeRTOS_SetIPAddress) page for an example.
