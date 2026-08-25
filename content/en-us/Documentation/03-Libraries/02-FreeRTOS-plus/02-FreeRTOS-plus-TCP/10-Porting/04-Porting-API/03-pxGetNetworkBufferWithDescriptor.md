---
title: pxGetNetworkBufferWithDescriptor()
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
NetworkBufferDescriptor_t *pxGetNetworkBufferWithDescriptor( size_t xRequestedSizeBytes,
                                                TickType_t xBlockTimeTicks );
```

Data that is sent out to the network or received from the network is
stored in a network buffer. A network buffer is basically just a block
of RAM (actually an array of uint8\_t in the source code).

The embedded TCP/IP stack needs to first locate the network buffers, and
once located know how big the network buffers are. Network buffer
descriptors are used for that purpose.

![Embedded network buffers](/media/2018/Ethernet_buffer.png)
**pucPayloadBuffer points to the start of the network buffer.
xDataLength holds the size of the buffer in bytes, excluding the Ethernet CRC bytes.**


More information is provided on the page
that [network buffer descriptor](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers)
describes how to port FreeRTOS-Plus-TCP to new devices.

pxGetNetworkBufferWithDescriptor() Obtains a network buffer and associated network buffer descriptor. If
xRequestedSizeBytes is 0 then a network buffer descriptor is obtained
by itself - without a network buffer.

pxGetNetworkBufferWithDescriptor() must not be called from an interrupt service routine (ISR).

The total number of network buffer descriptors is set
by [ipconfigNUM\_NETWORK\_BUFFER\_DESCRIPTORS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfignum_network_buffer_descriptors).


**Parameters:**

+ *xRequestedSizeBytes*

  The size of the Ethernet buffer to obtain and reference from the returned network buffer descriptor.
  The size is specified in bytes.

  If xRequestedSizeBytes is zero then the returned network buffer descriptor will not reference an Ethernet
  buffer (the reference is set to NULL).

+ *xBlockTimeTicks*

  If a network buffer is not available then the calling RTOS task will be held in the Blocked state (so
  other tasks can execute) until either a network buffer becomes available or the specified block time expires.

  The block time is specified in RTOS ticks. To convert a time specified in milliseconds to a time specified
  in RTOS ticks divide the time specified in milliseconds by portTICK\_PERIOD\_MS.


**Returns:**

Successful calls return a pointer to the obtained network buffer
descriptor. Unsuccessful calls return NULL.


**Example usage:**

Examples are provided on the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) page.
