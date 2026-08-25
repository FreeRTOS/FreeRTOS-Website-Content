---
title: "FreeRTOS_GetMACAddress()"
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
const uint8_t * FreeRTOS_GetMACAddress( void );
```


**Returns:** 

Returns a pointer to the MAC address use by the NIC expressed as six separate bytes, with each byte 
in a consecutive memory location.
