---
title: pucGetNetworkBuffer()
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
uint8_t *pucGetNetworkBuffer( size_t *pxRequestedSizeBytes );

```

发送到网络或从网络接收的数据存储在 
[网络缓冲区](../Embedded_Ethernet_Porting.md#network_buffers_and_Ethernet_buffers)。网络缓冲区 
基本上就是一个 RAM 块（实际是源代码中的 uint8_t 数组）。

嵌入式 TCP/IP 堆栈需要首先定位网络缓冲区，
一旦定位就能知道网络缓冲区的大小。网络缓冲区
描述符可用于实现此目的。

而 [pxGetNetworkBufferWithDescriptor()](pxGetNetworkBufferWithDescriptor.md) 获取一个
可以（选择性地）引用以太网缓冲区的网络缓冲区描述符，
pucGetNetworkBuffer() 只获取以太网缓冲区本身，
通常仅用于将缓冲区分配给零拷贝驱动程序中的 DMA
。

不得从中断服务程序 (ISR) 调用 pucGetNetworkBuffer()。
 
  
**参数：** 

+ *xRequestedSizeBytes* 

  要获取的以太网缓冲区的大小。大小以字节为单位。


**返回：** 

若调用成功，则返回指向已获取的以太网缓冲区的指针。
若调用失败，则返回 NULL。


**用法示例：** 

在[“将 FreeRTOS 移植到不同的微控制器”](../Embedded_Ethernet_Porting.md)页面上提供了示例。

