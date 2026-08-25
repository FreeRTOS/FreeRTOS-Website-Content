---
title: UDP 回显客户端示例
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
mainCREATE_UDP_ECHO_TASKS 设置为 1，它位于
项目的 main.c 源文件的顶层，从而将示例包含在
构建中。

示例会创建两个 RTOS 任务，将 UDP 回显请求发送到外部
[回显服务器](https://en.wikipedia.org/wiki/Echo_Protocol)，
使用的是标准回显端口（端口 7）。一个 RTOS 任务使用
标准套接字接口，其他 RTOS 任务使用零拷贝
套接字接口。

必须
使用 FreeRTOSConfig.h 中的 configECHO_SERVER_ADDR0 至 configECHO_SERVER_ADDR3 常量配置回显服务器的 IP 地址，
并且回显服务器必须启用，且不能被防火墙阻挡
。[Windows 带有回显服务器](https://technet.microsoft.com/library/cc740058(v=ws.10).aspx）
但默认情况下未启用。也可使用[第三方回显服务器](http://bansky.net/echotool/)
。

这些 RTOS 任务会进行自我检查，如果发现收到的数据和发送的数据有差异，将触发 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
失败。
由于这些 RTOS 任务使用 UDP，因此可以合法地丢包，
如果在不完善的网络环境下执行，可能造成 configASSERT() 失败
。

