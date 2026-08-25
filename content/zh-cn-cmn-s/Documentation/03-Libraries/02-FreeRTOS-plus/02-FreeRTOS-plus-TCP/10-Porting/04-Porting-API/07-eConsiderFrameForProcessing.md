---
title: eConsiderFrameForProcessing()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


自 FreeRTOS V10.1.0 开始，![](/media/2019/warning_icon.png)   
FreeRTOS+UDP 已从 FreeRTOS 内核下载包中移除。请参阅 
[FreeRTOS+TCP 堆栈](../../FreeRTOS_Plus_TCP/index.md)，此堆栈只能配置用于 UDP 作为 
替代方案。

[[以太网驱动程序移植 API](../Network_interface_functions.md)]

FreeRTOS_IP_Private.h


```c
eFrameProcessingResult_t eConsiderFrameForProcessing( uint8_t *pucEthernetBuffer );

```

检查接收的以太网帧，
考虑到 IP 堆栈的当前状态，判断该以太网帧是否应被处理
或丢弃。

如果在 [FreeRTOSIPConfig.h](../UDP_IP_Configuration.md) 中将 ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES 设置为 1，
则 eConsiderFrameForProcessing() 应由[网络接口移植层](../Embedded_Ethernet_Porting.md)调用，
以确定是否应将收到的以太网帧发送到 IP
堆栈进行处理。如果将 ipconfigETHERNET_DRIVER_FILTERS_FRAME_TYPES
在 FreeRTOSIPConfig.h 中设置为 0，则 IP 堆栈会自行调用
eConsiderFrameForProcessing()，但只有在它已经
从网络接口移植层接收到以太网帧以后。

如果嵌入式以太网外设硬件本身配置为过滤以太网帧，则不一定需要调用 eConsiderFrameForProcessing 
函数
。


**参数：** 

+ *pucEthernetBuffer* 

  指向所检查以太网帧的起始位置的指针。


**返回：** 

如果以太网帧需要处理，则返回 eProcessBuffer。
如果以太网帧可以丢弃，则返回 eReleaseBuffer
(在这种情况下，引用以太网帧的[网络缓冲区描述符](../Embedded_Ethernet_Porting.md#network_buffers_and_Ethernet_buffers)
和
以太网帧本身都必须返回到 IP 堆栈中）。


**用法示例：** 

在[“将 FreeRTOS 移植到不同的微控制器”](../Embedded_Ethernet_Porting.md)页面上提供了示例。


