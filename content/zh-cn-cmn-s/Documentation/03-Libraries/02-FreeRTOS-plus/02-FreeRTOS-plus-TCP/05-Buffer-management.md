---
title: 网络缓冲区分配方案
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

及其对 CPU 负载和吞吐量性能的影响

![](/media/2019/warning_icon.png)
自 FreeRTOS V10.1.0 开始，FreeRTOS+UDP 已从 FreeRTOS 内核下载包中移除。请参阅 
[FreeRTOS+TCP 堆栈](../FreeRTOS_Plus_TCP/index.md)，此堆栈可配置为仅使用 UDP，作为 
替代方案。


### 要点总结

- FreeRTOS-Plus-UDP 具有非常高效的零拷贝架构。根据 
  [嵌入式以太网外围设备驱动程序](Embedded_Ethernet_Porting.md#creating_a_zero_copy_network_port_layer)的实现
  以及用户选择的 API 调用语义，以太网数据包可以通过引用 
  从接收 DMA 缓冲区传递，通过堆栈，一路回传至传输 DMA 缓冲区。

- 影响性能的因素：

  1. **可重入性**

     FreeRTOS-Plus-UDP 具有完全可重入性和线程感知特征，这意味着 
     所有 RTOS 任务可同时安全使用 IP 堆栈。然而，这种灵活性是以牺牲一些时间效率为代价的， 
     这是因必须进行消息传递和上下文切换 
     以确保序列化访问 IP 堆栈（以受控方式进行，防止数据损坏）所致。 

  2. **缓冲区分配**

     嵌入式以太网（或其他嵌入式网络）外围设备接收的数据放置在 
     IP 堆栈预分配的缓冲区中。用户发送消息时，消息内容 
     放置在 IP 堆栈分配的缓冲区中。不同的缓冲区分配方案适用于 
     不同的嵌入式应用程序。FreeRTOS-Plus-UDP 目前包含两种缓冲区分配方案， 
     每种方案在简单性、RAM 使用效率和性能之间有着不同的权衡取舍。本页 
     描述了这两种方案。


### 缓冲区分配方案

实现缓冲区分配方案的 C 源文件位于 
FreeRTOS-Plus/FreeRTOS-Plus-UDP/portable/BufferManagement 目录中。一次只能使用一种方案。


#### 方案 1：由 BufferAllocation_1.c 实现

+ *描述* 

  + [以太网缓冲区描述符](Embedded_Ethernet_Porting.md#network_buffers_and_Ethernet_buffers) 
    由 IP 堆栈（在编译时）静态分配。  

  + 以太网缓冲区由嵌入式以太网外围设备驱动程序（在编译时）静态分配。
     这可确保缓冲区根据特定以太网硬件的要求进行对齐。

+ *属性*  

  + 运行时性能高。
  + 可以从中断中分配和释放以太网缓冲区，
    从而提高嵌入式以太网外围设备驱动程序的效率。
  + RAM 使用效率低：所有缓冲区大小相同，因此 BufferAllocation_1.c 不适合
    某些 RAM 受限的嵌入式系统。
  + 与由 BufferAllocation_2 实现的方案相比，此方案在配置和调整上更复杂。
  + 更容易实现嵌入式以太网
    外围设备 DMA 提出的特殊缓冲区对齐要求。
  + 需要网络接口驱动程序的支持（请参阅上文的要点*描述*部分）。

+ *用法*       

  + 利用 ipconfigNUM_NETWORK_BUFFERS 常量（在 [FreeRTOSIPConfig.h](UDP_IP_Configuration.md) 中定义）
    定义可用缓冲区的总数。
  + 利用 ipconfigNETWORK_MTU 常量（在 [FreeRTOSIPConfig.h](UDP_IP_Configuration.md) 中定义） 
    定义每个以太网帧的大小（总大小为定义的 MTU 大小加上 
    以太网标头所需的字节数）。


#### 方案 2：由 BufferAllocation_2.c 实现

+ *描述* 

  + [以太网缓冲区描述符](Embedded_Ethernet_Porting.md#network_buffers_and_Ethernet_buffers) 
    由 IP 堆栈（在编译时）静态分配。如此一来，用户可以限制 
    任意时间的以太网帧总数，以防止内存耗尽。
  + 根据需要动态分配和释放所需大小的以太网缓冲区。

+ *属性*  

  + 与 BufferAllocation_1.c 实现的方案相比，
    动态分配会导致运行时性能降低。
  + 无法从中断中分配和释放以太网缓冲区，因此需要在嵌入式以太网外围设备驱动程序中使用
    延迟中断处理任务。
  + RAM 使用效率很高：精确分配所需大小的 RAM，因此 BufferAllocation_2.c 特别适合
    RAM 受限的小型嵌入式系统。
  + 与由 BufferAllocation_1 实现的方案相比，此方案在配置和调整上更简单。


+ *用法*       

  + 利用 ipconfigNUM_NETWORK_BUFFERS 常量（在 [FreeRTOSIPConfig.h](UDP_IP_Configuration.md) 中定义） 
    定义可用网络缓冲区描述符的总数。这些描述符包含指向 
    以太网缓冲区的指针，但实际上并不包含缓冲区本身。缓冲区是按需分配的。
  + 从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)中分配以太网缓冲区。为避免内存碎片问题， 
    BufferAllocation_2.c 只有与合并了 
    堆内存空闲块的内存分配方案（合并算法）一起使用时才可靠。heap_4.c 中实现的 FreeRTOS 内存分配方案 
    是合适的。
  + 由于堆内存不足而导致分配网络缓冲区的尝试失败时，
    IP 堆栈将能够恢复正常。但是，这种失败会导致 malloc 失败钩子函数被调用
    （如果 configUSE_MALLOC_FAILED_HOOK 在 FreeRTOSConfig.h 中设置为 1）。

