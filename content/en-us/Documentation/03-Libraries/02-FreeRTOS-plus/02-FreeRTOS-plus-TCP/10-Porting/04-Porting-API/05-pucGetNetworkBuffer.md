---
title: pucGetNetworkBuffer()
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
uint8_t *pucGetNetworkBuffer( size_t *pxRequestedSizeBytes );
```

Data that is sent out to the network or received from the network is stored in
a [network buffer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers). A network buffer
is basically just a block of RAM (actually an array of uint8\_t in the source code).

The embedded TCP/IP stack needs to first locate the network buffers, and
once located know how big the network buffers are. Network buffer
descriptors are used for that purpose.

Whereas [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor) obtains a network
buffer descriptor that can (optionally) reference an Ethernet buffer,
pucGetNetworkBuffer() just obtains the Ethernet buffer itself and would
normally only be used allocate buffers to DMA descriptors in zero copy
drivers.

pucGetNetworkBuffer() must not be called from an interrupt service routine (ISR).


**Parameters:**

+ *xRequestedSizeBytes*

  The size of the Ethernet buffer to obtain. The size is specified in bytes.


**Returns:**

Successful calls return a pointer to the obtained Ethernet buffer.
Unsuccessful calls return NULL.


**Example usage:**

Examples are provided on the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) page.
