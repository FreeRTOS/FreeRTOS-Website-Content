---
title: FreeRTOS_AddNetworkInterface()
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
NetworkInterface_t * FreeRTOS_AddNetworkInterface( NetworkInterface_t * pxInterface );
```

FreeRTOS\_AddNetworkInterface() is used to add a new physical Network Interface. The object pointed to by 'pxInterface'
 must continue to exist. Only the Network Interface function 
 [`px${port_name}_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)
 should call this function.

**Parameters:**

*pxInterface*
The address of the new interface. This object must continue to exist even after 
 [`px${port_name}_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)

**Returns:**  

The pointer that points to interface itself.

**Example usage:**  

Examples are provided on the 
[Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) 
page. Search for FreeRTOS\_AddNetworkInterface() on that page to find example source code.

