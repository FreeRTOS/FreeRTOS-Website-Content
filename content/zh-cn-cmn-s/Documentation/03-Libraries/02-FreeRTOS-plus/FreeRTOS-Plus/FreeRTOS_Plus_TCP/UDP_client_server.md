---
title: UDP 客户端和服务器简单示例
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


并非所有演示项目都包含此示例。如果此示例
包含在演示项目中，则可能需要将
mainCREATE_SIMPLE_UDP_CLIENT_SERVER_TASKS 设置为 1，
此变量位于项目的 main.c 源文件顶部，以将示例包含在构建中。

此示例中，创建两个 UDP 客户端 RTOS 任务和两个 UDP 服务器 RTOS
任务。客户端与服务器进行通信。一组 RTOS
任务使用标准套接字接口，另一组 RTOS
任务使用零拷贝套接字接口。

这些 RTOS 任务会进行自我检查，如果发现收到的数据和发送的数据有差异，将触发 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
。
由于这些 RTOS 任务使用 UDP，因此可以合理丢包，
如果在网络环境不佳的情况下执行，则可能会触发 configASSERT()
。
