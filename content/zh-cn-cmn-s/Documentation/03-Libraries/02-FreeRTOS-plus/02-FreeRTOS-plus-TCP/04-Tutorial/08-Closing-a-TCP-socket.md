---
title: 停止并关闭 TCP 套接字
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

**未**连接的 TCP 套接字可以使用 [FreeRTOS_closesocket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/13-close)
API 函数关闭。

**已**连接的 TCP 套接字应在
停止连接后关闭。要正常关闭套接字，请首先
调用 [FreeRTOS_shutdown()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/12-shutdown)，
然后等待套接字上的读取尝试返回 -pdFREERTOS_ERRNO_EINVAL，表示
套接字已断开连接。

在[发送 TCP 数据](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/06-Sending-TCP-data)
和[接收 TCP 数据](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/07-Receiving-TCP-data)页面上的源代码示例演示了如何停止并关闭
已连接的套接字。

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

