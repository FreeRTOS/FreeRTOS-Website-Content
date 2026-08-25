---
title: vReleaseNetworkBuffer()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[以太网驱动程序移植 API](../Network_interface_functions.md)]

FreeRTOS_IP_Private.h
   
NetworkBufferManagement.h


```c
void vReleaseNetworkBuffer( uint8_t *pucPayloadBuffer );

```

向 TCP/IP 堆栈返回之前从[](../Embedded_Ethernet_Porting.md#network_buffers_and_Ethernet_buffers)
TCP/IP 堆栈获取的以太网缓冲区。

vReleaseNetworkBuffer() 通常仅由零拷贝驱动程序
用于释放先前分配给 DMA 描述符的缓冲区。
通常，网络缓冲区和描述符一同被分配和释放，
具体做法是分别使用 [pxGetNetworkBufferWithDescriptor()](pxGetNetworkBufferWithDescriptor.md) 
和 [vReleaseNetworkBufferAndDescriptor()](vReleaseNetworkBufferAndDescriptor.md)。

不得从中断服务程序 (ISR) 调用 vReleaseNetworkBuffer()。


**参数：** 

+ *pucPayloadBuffer* 

  指向被释放（返回 TCP/IP 堆栈）的以太网缓冲区的指针。


**用法示例：** 

在[“将 FreeRTOS 移植到不同的微控制器”](../Embedded_Ethernet_Porting.md)页面上提供了示例。


