---
title: UDP
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[以太网数据包](ethernet_networking_and_addressing.md)
可携带 [IP 数据包](internet_protocol.md)，
而 IP 数据包又可以携带 UDP 数据包。

UDP 是 [User Datagram Protocol](http://en.wikipedia.org/wiki/User_Datagram_Protocol)（用户数据报协议）的缩写。
UDP 用于发送和接收称为
数据报的无连接数据包。与 [TCP](TCP.md) 数据包不同，
因为不需要在发送或接收数据之前
与另一个网络节点建立连接，这些数据包被认为是无连接的。

UDP 协议不包括确认传输的数据是否
到达了预期接收方的方法。如果需要确认，
则必须由应用程序本身提供。例如，
应用程序可能会非常简单地使用单独的 UDP 数据包
将接收到的数据回显到发送方，告知发送方数据已收到。

与 TCP 相比，UDP 更快、更简单，并且需要的 RAM 更少。

另请参阅 [UDP 套接字](socket.md)。

