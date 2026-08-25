---
title: pxGetNetworkBufferWithDescriptor()
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
NetworkBufferDescriptor_t *pxGetNetworkBufferWithDescriptor( size_t xRequestedSizeBytes,
                                                TickType_t xBlockTimeTicks );
```

发送到网络或从网络接收的数据
存储在网络缓冲区中。网络缓冲区基本上只是一个
RAM 块（实际是源代码中的 uint8_t 数组）。

嵌入式 TCP/IP 堆栈需要首先定位网络缓冲区，
一旦定位就能知道网络缓冲区的大小。网络缓冲区
描述符即用于此目的。

![嵌入式网络缓冲区](/media/2018/Ethernet_buffer.png)   
**pucPayloadBuffer 指向网络缓冲区的起点。
xDataLength 保存缓冲区的大小（以字节为单位，不包括以太网 CRC 字节）。** 


更多信息请参阅 
[网络缓冲区描述符](../Embedded_Ethernet_Porting.md#network_buffers_and_Ethernet_buffers)
说明如何将 FreeRTOS-Plus-TCP 移植到新设备的页面。

pxGetNetworkBufferWithDescriptor() 获取网络缓冲区和关联的网络缓冲区描述符。如果
xRequestedSizeBytes 为 0，则自行获取网络缓冲区描述符，
而没有网络缓冲区。

不得从中断服务程序 (ISR) 调用 pxGetNetworkBufferWithDescriptor()。

网络缓冲区描述符的总数由 
[ipconfigNUM_NETWORK_BUFFER_DESCRIPTORS](../TCP_IP_Configuration.md#ipconfignum_network_buffer_descriptors) 设置。


**参数：** 

+ *xRequestedSizeBytes* 

  从返回的网络缓冲区描述符中获取和引用的以太网缓冲区的大小。 
  大小以字节为单位。

  如果 xRequestedSizeBytes 为零，则返回的网络缓冲区描述符将不引用以太网缓冲区 
  （引用设置为 NULL）。

+ *xBlockTimeTicks* 

  如果网络缓冲区不可用，则调用 RTOS 任务将处于阻塞状态（以便其他任务可以执行）， 
  直到网络缓冲区可用或规定阻塞时间到期。

  规定阻塞时间时以 RTOS 滴答为单位。要将以毫秒为单位的时间转换为 
  以 RTOS 滴答为单位的时间，请将以毫秒为单位的时间除以 portTICK_PERIOD_MS。


**返回：** 

若调用成功，则返回指向已获取的网络缓冲区描述符的指针
。若调用失败，则返回 NULL。


**用法示例：** 

在[“将 FreeRTOS 移植到不同的微控制器”](../Embedded_Ethernet_Porting.md)页面上提供了示例。

