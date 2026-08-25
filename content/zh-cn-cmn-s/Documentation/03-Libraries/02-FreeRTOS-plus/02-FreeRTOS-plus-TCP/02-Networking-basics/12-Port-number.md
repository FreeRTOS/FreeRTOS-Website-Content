---
title: 移植号
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


每个网络节点可以运行多个使用
相同网络接口的应用程序，因此使用相同的 [IP 地址](IP_address.md)。例如，
RTOS 应用程序可以同时运行 TFTP 服务器、回显服务器和 Nabto 客户端，
所有这些设备都使用 [TCP](TCP.md)/[IP](internet_protocol.md) 堆栈。
在同一网络节点上运行
并采用同一 IP 地址的不同应用程序均通过移植号标识。

因此，每个 TCP 或 [UDP](UDP.md) 
数据包的源地址和目标地址都是 IP 地址
和移植号的组合。IP 地址标识网络上的节点，
移植号标识节点中的应用程序
（请参阅[套接字](socket.md)）。

