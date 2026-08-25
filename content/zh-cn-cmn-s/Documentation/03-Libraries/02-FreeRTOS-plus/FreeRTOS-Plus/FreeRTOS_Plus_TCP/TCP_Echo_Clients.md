---
title: TCP Echo 客户端示例（使用单个 RTOS 任务）
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)


并非所有演示项目都包含此示例。如果此示例
则可能需要将
mainCREATE_TCP_ECHO_TASKS_SINGLE 设置为 1，它位于
项目的 main.c 源文件的顶层，从而将示例包含在
构建中。

示例会创建两个 RTOS 任务，将 TCP 回显请求发送到
外部[回显服务器](https://en.wikipedia.org/wiki/Echo_Protocol)
（使用的是标准回显端口（端口 7）），然后等待接收同一
RTOS 任务内的回显应答。[另一个 TCP 回显示例](TCP_Echo_Clients_Separate)
使用来自两个不同 RTOS 任务的同一 TCP 套接字，其中一个 RTOS 任务负责发送
回显请求，另一个 RTOS 任务负责接收回显应答。



必须使用
FreeRTOSConfig.h 中的 configECHO_SERVER_ADDR0 至 configECHO_SERVER_ADDR3 常量配置回显服务器的 IP 地址，
并且回显服务器必须启用，且不能被防火墙阻挡
。[Windows 带有回显服务器](https://technet.microsoft.com/library/cc740058(v=ws.10).aspx）
但默认情况下未启用。也可使用[第三方回显服务器](http://bansky.net/echotool/)
。
