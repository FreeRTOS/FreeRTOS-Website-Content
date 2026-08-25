---
title: FreeRTOS_MatchingEndpoint()
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Ethernet Driver Porting API](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/01-Network_interface_functions)]


FreeRTOS\_Routing.h


```c
NetworkEndPoint_t * FreeRTOS_MatchingEndpoint( const NetworkInterface_t * pxNetworkInterface,
                                               const uint8_t * pucEthernetBuffer );
```

FreeRTOS\_MatchingEndpoint() is used to find out the best matching end-point given an incoming Ethernet packet.

**Parameters:**

*pxInterface*
The interface on which the packet was received.
*pucEthernetBuffer*
The Ethernet packet that was just received.

**Returns:**  

The end-point that should handle the incoming Ethernet packet.

**Example usage:**  

Examples are provided on the 
 [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) page. 
 Search for FreeRTOS\_MatchingEndpoint() on that page to find example source code.
