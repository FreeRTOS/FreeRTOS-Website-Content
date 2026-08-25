---
title: 与其他开源 TCP/IP 堆栈一起使用的旧版演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**请注意，本页发布时间早于 [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，即 FreeRTOS 自带的
的嵌入式 TCP/IP 堆栈。**

本页列出了旧版 FreeRTOS 演示项目，其中包括一个完全抢占式多任务环境中的嵌入式 web
服务器。有些演示使用 lwIP 作为底层嵌入式 TCP/IP 堆栈——并且早于
[FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)（FreeRTOS 自带的可扩展 TCP/IP 堆栈）的推出。这些项目的开发时长不一样，
因此，所使用的堆栈版本也不尽相同。如需了解更多信息，
请直接参考下方提供的堆栈。演示本身是[按照以下微控制器](#包含freertos-ip-功能的-tcp演示)
制造商列出的。

### lwIP

当在其预期的、内存受限的环境中使用时， lwIP 协议栈也是一个不错的选择。
相较于 uIP，它的吞吐量更高，但同时 ROM 和 RAM 占用空间也更大。
尽管占用空间比 uIP 大，但也仍然比大多数商业
TCP/IP 产品要小。特别是，LwIP 通过将较小的缓冲区链接在一起来创建较大的数据缓冲区，从而节省 RAM
。

这里列出的大部分（如果不是全部）FreeRTOS 演示使用的 LwIP 版本非常旧 。
然而，也有人在
[FreeRTOS 互动论坛](http://interactive.freertos.org/)贡献了有关如何使用最新
LWIP 代码库的相关演示。欢迎大家上传投稿 lwIP
相关内容！

另一方面， lwIP 一开始操作起来的确比较复杂，
但只要投入时间使用就会在将来的项目中有所回报。

lwIP 也是一个移动式目标，因为它在不断
更新换代（这不一定是一件坏事情）。


## 包含FreeRTOS /IP 功能的 TCP演示

### Atmel 微控制器示例

1. [AVR32 AT32UC3A lwIP web 和 TFTP 服务器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portAVR32#webserverexample)：

   此示例使用 lwIP 在 AVR32 闪存微控制器上创建简单的 web 和 TFTP 服务器。

2. [在 AT91SAM7X 上运行开源 lwIP TCP/IP 堆栈](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7xlwIP)：

 包括  用于 SAM7X 集成 EMAC 外设的更全面的中断驱动式驱动程序。

### ST 微控制器示例

1. [STR912 (ARM9) 上的开源 lwIP TCP/IP 堆栈](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr912iar)：

   此演示包括使用 lwIP 堆栈，此次是针对 ARM9 处理器。

### 使用 WizNET 接口的示例

1. [WizNET 硬件 TCP/IP 堆栈—— I2C 接口](/webservedemo)：

   此示例中，TCP/IP 协处理器通过 I2C 端口生成嵌入式 web 服务器。

2. [WizNET 硬件 TCP/IP 堆栈——内存映射接口](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/portternee)：

   此示例中，使用相同的 TCP/IP 协处理器，但在 Tern E-Engine 控制器上使用内存映射接口
   。
