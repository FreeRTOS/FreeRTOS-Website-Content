---
title: vReleaseNetworkBuffer()
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
void vReleaseNetworkBuffer( uint8_t *pucPayloadBuffer );
```

Returns to the TCP/IP stack an [Ethernet buffer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers)
that was previously obtained from the TCP/IP stack.

vReleaseNetworkBuffer() would normally only be used by a zero copy driver
to release buffers that were previously allocated to DMA descriptors.
Normally network buffers are allocated and released along with
descriptors using [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor)
and [vReleaseNetworkBufferAndDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/04-vReleaseNetworkBufferAndDescriptor) respectively.

vReleaseNetworkBuffer() must not be called from an interrupt service routine (ISR).


**Parameters:**

+ *pucPayloadBuffer*

  A pointer to the Ethernet buffer being released (returned to the TCP/IP stack).


**Example usage:**

Examples are provided on the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) page.
