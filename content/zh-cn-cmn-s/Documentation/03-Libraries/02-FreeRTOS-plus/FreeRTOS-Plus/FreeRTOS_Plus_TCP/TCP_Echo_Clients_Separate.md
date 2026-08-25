---
title: TCP 回显客户端示例（使用多个 RTOS 任务）
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 和 FreeRTOS-Plus-FAT 示例](TCP_FAT_demo_projects#Free_TCPIP_FAT_examples)

并非所有演示项目都包含此示例。如果此示例
包含在演示项目中，则可能需要
在项目的 main.c 源文件顶部将 mainCREATE_TCP_ECHO_TASKS_SEPARATE 设置为 1，
以将示例包含在
构建中。

此示例创建两个使用相同 TCP 套接字的 RTOS 任务。其中一个
RTOS 任务通过标准的回显端口（端口 7），发送 TCP 回显请求至外部[回显服务器](https://en.wikipedia.org/wiki/Echo_Protocol)，
另一个 RTOS 任务侦听
回显回复。[另外还有一个示例](TCP_Echo_Clients)
使用相同的 RTOS 任务发送回显请求和侦听回显
回复。

回显服务器的 IP 地址必须使用
FreeRTOSConfig.h 中的 configECHO_SERVER_ADDR0 至 configECHO_SERVER_ADDR3 常量配置回显服务器的 IP 地址，
并且回显服务器必须启用，且不能被防火墙阻挡
。[Windows 带有回显服务器](https://technet.microsoft.com/library/cc740058(v=ws.10).aspx）
但默认情况下未启用。也可使用[第三方回显服务器](http://bansky.net/echotool/)
。

