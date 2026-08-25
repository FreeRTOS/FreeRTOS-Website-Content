---
title: "使用 FreeRTOS_select() 的示例"
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
mainCREATE_SELECT_UDP_SERVER_TASKS 设置为 1，它位于
项目的 main.c 源文件的顶层，从而将示例包含在
构建中。

示例创建了两个 RTOS 任务，演示如何使用 [FreeRTOS_select()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/14-select)。
一个 RTOS 任务创建了许多套接字，使用 [FreeRTOS_FD_SET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/16-FD_SET) 添加到集合中，
而另一个 RTOS 任务将数据发送到该集合的随机套接字中，
便于第一个 RTOS 任务进行接收和验证。

这些 RTOS 任务会进行自我检查，如果发现收到的数据和发送的数据有差异，将触发 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
失败
。由于这些 RTOS 任务使用 UDP，因此可以合法地丢包，
如果在不完善的网络环境下执行数据包，
则可能导致 configASSERT() 失败。
