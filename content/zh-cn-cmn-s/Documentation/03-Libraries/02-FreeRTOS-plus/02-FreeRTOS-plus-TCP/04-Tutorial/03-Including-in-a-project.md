---
title: 将 TCP/IP 源文件添加到 RTOS 项目
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

FreeRTOS-Plus-TCP 是开源 TCP/IP 堆栈，因此 
[以源文件的形式提供](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/02-Source-code-organization)， 
可作为 RTOS 应用程序的一部分进行构建。

最好从已知运行正常的标准 FreeRTOS
应用程序（无 TCP/IP 堆栈）开始 ，
然后添加 TCP/IP 源文件。
该应用程序**必须**使用 [heap_4 或 heap_5 内存分配器](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)。
当您确定标准 RTOS
并正确执行时：

1. 向项目中添加以下核心 FreeRTOS-Plus-TCP 源文件：

   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_ARP.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_DHCP.c
   - FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/FreeRTOS_DNS.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_DNS_Cache.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_DNS_Callback.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_DNS_Networking.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_DNS_Parser.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_ICMP.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_IP.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_IP_Timers.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_IP_Utils.c
   - FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/FreeRTOS_Sockets.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_StreamBuffer.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_TCP_IP.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_TCP_Reception.c
   - FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/FreeRTOS_TCP_State_Handling.c
   - FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/FreeRTOS_TCP_Transmission.c
   - FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/FreeRTOS_TCP_Utils.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_TCP_WIN.c
   - FreeRTOS-Plus/FreeRTOS-Plus-TCP/source/FreeRTOS_Tiny_TCP.c
   - FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/FreeRTOS_UDP_IP.c

2. 将网络接口的驱动程序（MAC 或以太网驱动程序）添加到您的项目中
   。实现网络驱动程序的源文件称为 NetworkInterface.c，位于：

   FreeRTOSFreeRTOS-Plus/TCP\_Plus\_/source/portable/NetworkInterface/[microcontroller]/，其中 [microcontroller] 
   是运行 FreeRTOS-Plus-TCP 的微控制器系列。

   提供了为其他芯片[创建网络驱动程序](Embedded_Ethernet_Porting.md)的说明。 

3. 将您选择的[网络缓冲区分配方案e](Embedded_Ethernet_Buffer_Management.md)添加到您的项目中。 
   实现缓冲区分配方案的源文件位于：

   FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/portable/BufferManagement/。

   此时，为简单起见，推荐使用 BufferAllocation_2.c，
   因为它获取 RAM
   的方式是 FreeRTOS 堆。 

   **BufferAllocation_2.c 只能与 [heap_4 及 heap_5 内存分配器](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)**一起使用。 

4. 将下列核心 TCP/IP 目录添加至编译器的包含路径中：

   + FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/include
   + FreeRTOS-Plus/FreeRTOS_Plus_TCP/source/portable/Compiler/[compiler]

   (其中 [compiler] 是使用的编译器）。\*查找芯片专用驱动程序头文件所需的任何目录。 

5. 在项目中添加 FreeRTOSIPConfig.h 头文件， 
   并确保其中包含的常量已为应用程序进行了[适当配置](TCP_IP_Configuration.md)。您可以使用 
   [示例项目](Download_FreeRTOS_Plus_TCP.md)中提供的配置文件作为起点。

   FreeRTOSIPConfig.h 为您的应用程序定制核心 TCP/IP 堆栈。它
   专用于应用程序而非 TCP/IP堆栈，因此应定位
   应用程序目录，而不是 FreeRTOS-Plus-TCP 目录中。

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

