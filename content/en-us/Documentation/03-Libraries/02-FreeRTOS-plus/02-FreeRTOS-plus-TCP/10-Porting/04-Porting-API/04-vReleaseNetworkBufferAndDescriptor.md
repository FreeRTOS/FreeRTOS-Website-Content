---
title: vReleaseNetworkBufferAndDescriptor()
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[Ethernet Driver Porting API](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/01-Network_interface_functions)]

FreeRTOS\_IP\_Private.h

NetworkBufferManagement.h


```c
void vReleaseNetworkBufferAndDescriptor( NetworkBufferDescriptor_t * const pxNetworkBuffer );
```

Returns to the TCP/IP stack
a [network buffer descriptor](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers)
that was previously obtained from the TCP/IP stack by a call
to [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor).

If the network buffer descriptor references an Ethernet buffer then the Ethernet buffer is also returned.

pxGetNetworkBufferWithDescriptor() must not be called from an interrupt service routine (ISR).


**Parameters:**

+ *pxNetworkBuffer*

  A pointer to the network buffer descriptor being released<br/> (returned to the TCP/IP stack).


**Example usage:**

Examples are provided on the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) page.
