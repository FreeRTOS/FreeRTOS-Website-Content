---
title: vReleaseNetworkBufferAndDescriptor()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[以太网驱动程序移植 API](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/01-Network_interface_functions)]

FreeRTOS_IP_Private.h

NetworkBufferManagement.h


```c
void vReleaseNetworkBufferAndDescriptor( NetworkBufferDescriptor_t * const pxNetworkBuffer );
```

向 TCP/IP
堆栈返回[网络缓冲区描述符](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#network_buffers_and_Ethernet_buffers)，
该描述符是之前从 TCP/IP 堆栈中获得的
（通过调用 [pxGetNetworkBufferWithDescriptor()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/03-pxGetNetworkBufferWithDescriptor) 获得）。

如果网络缓冲区描述符引用了以太网缓冲区，则也会返回以太网缓冲区。

不得从中断服务程序 (ISR) 调用 pxGetNetworkBufferWithDescriptor()。


**参数：**

+ *pxNetworkBuffer*

  指向正在释放的网络缓冲区描述符的指针<br/> （返回到 TCP/IP 堆栈）。


**用法示例：**

在[“将 FreeRTOS 移植到不同的微控制器”](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)页面上提供了示例。
