---
title: eConsiderFrameForProcessing()
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


![](/media/2019/warning_icon.png)
FreeRTOS+UDP was removed from the FreeRTOS kernel download from FreeRTOS V10.1.0. See
the [FreeRTOS+TCP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), which can be configured for UDP only use, as
an alternative.

[[Ethernet Driver Porting API](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/01-Network_interface_functions)]

FreeRTOS\_IP\_Private.h


```c
eFrameProcessingResult_t eConsiderFrameForProcessing( uint8_t *pucEthernetBuffer );
```

Examines a received Ethernet frame to determine if, taking into account
the current state of the IP stack, the Ethernet frame should be processed
or dropped.

If ipconfigETHERNET\_DRIVER\_FILTERS\_FRAME\_TYPES is set to 1 in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration)
then eConsiderFrameForProcessing() should be called by the [network interface port layer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)
to determine whether received Ethernet frames should be sent to the IP
stack for processing. If ipconfigETHERNET\_DRIVER\_FILTERS\_FRAME\_TYPES is
set to 0 in FreeRTOSIPConfig.h then the IP stack will itself call
eConsiderFrameForProcessing(), but only after it has already
received the Ethernet frame from the network interface port layer.

It might not be necessary to call eConsiderFrameForProcessing()
if the embedded Ethernet peripheral hardware is itself configured to filter
Ethernet frames.


**Parameters:**

+ *pucEthernetBuffer*

  A pointer to the start of the Ethernet frame being inspected.


**Returns:**

eProcessBuffer is returned if the Ethernet frame needs processing.
eReleaseBuffer is returned if the Ethernet frame can be dropped (in
which case both the [network buffer descriptor](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers)
that references the Ethernet
frame, and the Ethernet frame itself, must both be returned to the IP stack).


**Example usage:**

Examples are provided on the [Porting FreeRTOS to a Different Microcontroller](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) page.
