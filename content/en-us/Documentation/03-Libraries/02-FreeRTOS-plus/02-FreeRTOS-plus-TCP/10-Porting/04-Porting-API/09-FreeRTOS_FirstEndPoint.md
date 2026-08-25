---
title: FreeRTOS_FirstEndPoint()
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
NetworkEndPoint_t * FreeRTOS_FirstEndPoint( const NetworkInterface_t * pxInterface );
```

FreeRTOS\_FirstEndPoint() is used to find the first end-point bound to a given interface. If given interface is NULL 
 then it returns first end-point foy any interface.

**Parameters:**

*pxInterface*
The address of the new interface. This object must continue to exist even after 
 [`px${port_name}_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#pxport_name_FillInterfaceDescriptor).

**Returns:**  

The first end-point that is found to the interface, or NULL when the interface doesn't have any end-point yet.

**Example usage:**  

Examples are provided on the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)
 page. Search for FreeRTOS\_FirstEndPoint() on that page to find example source code.
