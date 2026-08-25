---
title: FreeRTOS-Plus-UDP API
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

![](/media/2019/warning_icon.png)
FreeRTOS+UDP was removed from the FreeRTOS kernel download from FreeRTOS V10.1.0. See
the [FreeRTOS+TCP stack](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), which can be configured for UDP only use, as an
alternative.

The following functions are provided for use by the [Ethernet interface port layer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting).

* [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor)
* [vReleaseNetworkBufferAndDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/04-vReleaseNetworkBufferAndDescriptor)
* [pucGetNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/05-pucGetNetworkBuffer)
* [vReleaseNetworkBuffer()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/06-vReleaseNetworkBuffer)
* [eConsiderFrameForProcessing()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/07-eConsiderFrameForProcessing)
* [xSendEventStructToIPTask()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/08-xSendEventStructToIPTask)
