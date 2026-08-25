---
title: FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS-Plus-FAT 是一个 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 项目。虽然功能齐全， 
相当成熟，但它是收购过来的产品（不是我们自己编写的），因此不一定 
符合我们的生产代码或测试标准。它可从  
GitHub 上的 [Lab-Project-FreeRTOS-FAT](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-FAT) 存储库获得。


## 简介

[\![](/media/2018/video_still_tcp_fat_190K.jpg)](TCP-IP_In_190K_RAM_Video.md)   
*展示许多标准 RTOS TCP/IP 和 FAT
文件系统演示（[下文所示 ](#功能)）在
低于 190K 字节的 RAM* 中同时运行的视频

FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 配备预配置演示项目，
使得中间件组件可以直接构建和运行
。下方链接
描述了如何查找、使用这些演示项目。

[使用 FreeRTOS Windows 移植的演示](examples_FreeRTOS_simulator.md)提供完全免费而且
功能丰富的环境，用于评估和开发 FreeRTOS-Plus-TCP 和
FreeRTOS-Plus-FAT 应用程序，使用免费工具，无需购买任何特殊
硬件。


### 目标特定预配置项目

- [Windows 演示](examples_FreeRTOS_simulator.md)：使用免费工具
- [Xilinx Zynq dual core ARM Cortex-A9 演示](TCPIP_FAT_Examples_Xilinx_Zynq.md)
- [Atmel SAM4E ARM Cortex-M4F 演示](TCPIP_FAT_Examples_Atmel_SAM4E.md)
- [ST STM32F4 ARM Cortex-M4F 演示](TCP-IP_FAT_Examples_ST_STM32F407.md)（仅使用内部 RAM！）


### 功能

预配置演示项目运行多个示例。有关各示例的描述以及
在构建中包含示例的说明，请参见下方链接。
并非所有演示项目都囊括了所有示例，但
使用了 FreeRTOS Windows 移植[(examples_FreeRTOS_simulator.md)的]演示项目中包含所有示例。

可用示例

- FreeRTOS-Plus-TCP UDP 套接字示例
  1.  [使用 UDP 套接字的命令行界面](UDP_CLI.md)
  2.  [与基础版 UDP 服务器通信的基础版 UDP 客户端（标准和零拷贝）](UDP_client_server.md)
  3.  [使用 FreeRTOS_select()](using_select.md)
  4.  [UDP 回显客户端](UDP_Echo_Clients.md)
  5.  [将 FreeRTOS-Plus-TCP 日志消息发送到 UDP 移植](UDP_Logging.md)
- FreeRTOS-Plus-TCP TCP 套接字示例
  1.  [TCP 回显客户端（在同一 RTOS 任务中执行的 Rx 和 Tx）](TCP_Echo_Clients.md)
  2.  [TCP 回显客户端（在不同 RTOS 任务中执行的 Rx 和 Tx）](TCP_Echo_Clients_Separate.md)
  3.  [TCP 回显服务器](TCP_Echo_Server.md)
- FreeRTOS-Plus-TCP、FreeRTOS-Plus-FAT Web (HTTP) 和 FTP 示例
  1.  [FTP 服务器](FTP_Server.md)
  2.  [HTTP 网络服务器](HTTP_web_Server.md)
- FreeRTOS-Plus-FAT
  1.  [创建和验证一组示例文件](../FreeRTOS_Plus_FAT/creating_and_verifying_files.md)
  2.  [基础 stdio API 测试](../FreeRTOS_Plus_FAT/basic_stdio_API_tests.md)
  3.  [创建磁盘](../FreeRTOS_Plus_FAT/creating_a_disk.md)
  4.  [文件系统命令行接口](../FreeRTOS_Plus_FAT/file_related_cli_commands.md)

![记录免费 RTOS TCP/IP 堆栈](/media/2018/udp_logging_output.jpg)生成的消息
*[UDP 日志记录示例](UDP_Logging.md)*产生的输出

