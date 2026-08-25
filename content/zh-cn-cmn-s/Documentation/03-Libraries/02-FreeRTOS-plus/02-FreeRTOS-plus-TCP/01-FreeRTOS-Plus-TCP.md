---
title: FreeRTOS-Plus-TCP
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

适用于 FreeRTOS 且线程安全的开源 TCP/IP 堆栈

另请参阅 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction/) 项目，该项目新增了对 [IPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/03-Multiple-interface/02-IPv6-functionality/) 
以及[多个网络接口和多个端点](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/03-Multiple-interface/01-Mulitple-interfaces/)的支持 
（针对当前版本的 FreeRTOS-Plus-TCP）。

FreeRTOS-Plus-TCP v3.0.0 提高了 
[FreeRTOS-Plus-TCP](https://github.com/freertos/freertos-plus-tcp) 库的稳健性、安全性和模块化程度。
请点击[此处](/Community/Blogs/2022/the-freertos-plus-tcp-library-is-now-more-robust-and-secure/)了解更多信息。



FreeRTOS-Plus-TCP 是适用于 FreeRTOS 的可扩展且线程安全的开源 TCP/IP 堆栈。

FreeRTOS-Plus-TCP 提供广为熟知且基于标准的 Berkeley 套接字接口，
简单易用，便于快速学习。高级用户还可以使用替代回调接口。

FreeRTOS-Plus-TCP 的功能和 RAM 占用空间完全可扩展，因此 FreeRTOS-Plus-TCP 
既适用于低吞吐量的小型微控制器，也适用于高吞吐量的大型微处理器。

请参阅树形菜单（左侧）中的 FreeRTOS-Plus-TCP 部分， 
获取 [FreeRTOS-Plus-TCP 网络教程](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial/)、[移植指南](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/01-FreeRTOS_TCP_Porting/)、[API 文档](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs) 
以及[免费 TCP/IP 源代码下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)链接。

[![RTOS、TCP、FAT](/media/2018/0.png)](https://www.youtube.com/v/gZt5G5pWUv4?autoplay=1&rel=0&enablejsapi=1&playerapiid=ytplayer "RTOS、TCP")  
*使用 Filezilla 将大文件和小文件通过 FTP 传输到运行 FreeRTOS-Plus-TCP 和 [**FreeRTOS-Plus-FAT**] 的 66MHz MCU 上(/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT/)*


**功能**
+ Berkeley 套接字 API
+ 可选支持 TCP 滑动窗口
+ 完全可重入和线程安全 API
+ 包含 [ARP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/06-ARP/)、[DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP/)、[DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/20-DNS)、[LLMNR](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/22-LLMNR)、[NBNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/23-NetBIOS) 
+ 免费 ARP
+ 静态、DHCP 和自动 IP 地址分配
+ 也可仅用作 UDP 堆栈
+ 可选回调接口
+ 可选分段传出数据包

**Berkeley 套接字 API**
+ [FreeRTOS_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/02-socket/)
+ [FreeRTOS_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt/)
+ [FreeRTOS_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind/)
+ [FreeRTOS_listen()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen/)
+ [FreeRTOS_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect/)
+ [FreeRTOS_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept/)
+ [FreeRTOS_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send/) / [FreeRTOS_sendto()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto/)
+ [FreeRTOS_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv/) / [FreeRTOS_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom/)
+ 等。

**代码大小（通过 ARM Cortex-M GCC 生成的示例）**
| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| ---- | --------------------- | --------------------- |
| FreeRTOS_ARP.c | 1.6K | 1.4K |
| FreeRTOS_DHCP.c | 1.9K | 1.6K |
| FreeRTOS_DNS.c | 0.4K | 0.4K |
| FreeRTOS_DNS_Cache.c | 0.7K | 0.6K |
| FreeRTOS_DNS_Callback.c | 0.4K | 0.3K |
| FreeRTOS_DNS_Networking.c | 0.2K | 0.2K |
| FreeRTOS_DNS_Parser.c | 0.7K | 0.5K |
| FreeRTOS_ICMP.c | 0.2K | 0.2K |
| FreeRTOS_IP.c | 4.3K | 4.0K |
| FreeRTOS_IP_Timers.c | 0.6K | 0.6K |
| FreeRTOS_IP_Utils.c | 1.7K | 1.5K |
| FreeRTOS_Sockets.c | 6.5K | 5.3K |
| FreeRTOS_Stream_Buffer.c | 0.5K | 0.4K |
| FreeRTOS_TCP_IP.c | 1.5K | 1.1K |
| FreeRTOS_TCP_Reception.c | 0.8K | 0.6K |
| FreeRTOS_State_Handling.c | 2.1K | 1.7K |
| FreeRTOS_Transmission.c | 2.1K | 1.9K |
| FreeRTOS_TCP_Utils.c | 0.2K | 0.2K |
| FreeRTOS_TCP_WIN.c | 2.1K | 1.9K |
| FreeRTOS_Tiny_TCP .c | 0.0K | 0.0K |
| FreeRTOS_UDP_IP.c | 0.5K | 0.4K |
| **总估算** | **28.8K** | **24.8K** |

