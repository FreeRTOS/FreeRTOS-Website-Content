---
title: 网络套接字
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


从概念上讲，[套接字](http://en.wikipedia.org/wiki/Network_socket)
是指通信端点，[伯克利套接字](https://en.wikipedia.org/wiki/Berkeley_sockets)
API 是跨平台标准 API，用于创建、配置、
读取、写入或以其他方式管理套接字。

套接字通过网络节点的 [IP 地址](IP_address.md)
和网络节点内的[端口号](port_number.md)
予以标识。

如果网络节点想要将 [UDP](UDP.md) 数据发送到网络上，
则首先应创建
套接字，然后将数据发送到该套接字。如果网络节点想要
接收 UDP 数据，则首先应在发送数据的节点已知的地址上创建套接字，
然后从该套接字读取数据。

如果网络节点想要将 [TCP](TCP.md) 数据发送到网络上，
则首先应
创建套接字，将该套接字连接到远程节点上的套接字，
然后将数据发送到该套接字。如果网络节点想要接收
TCP 数据，则首先应创建套接字，然后在该套接字上监听
传入连接。接收到连接后，网络节点可以
创建新的套接字来处理连接（可选），然后
然后在新套接字上接收数据，并让原始套接字监听更多
传入连接。

由此可见，任何一个网络节点均可同时参与多个
网络对话，套接字可用于
各唯一对话的两端。

套接字还可用于发送和接收广播和多播
通信，两者都属于一对多通信。

API 函数 [FreeRTOS_socket()](API/socket.md)
用于创建套接字。

[FreeRTOS-Plus-TCP 联网教程](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
演示了如何使用套接字。

