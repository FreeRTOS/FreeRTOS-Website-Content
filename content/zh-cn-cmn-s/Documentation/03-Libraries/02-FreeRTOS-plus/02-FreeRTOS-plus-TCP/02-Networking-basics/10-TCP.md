---
title: TCP
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[以太网数据包](ethernet_networking_and_addressing.md)
可携带 [IP 数据包](internet_protocol.md)，
而 IP 数据包又可以携带 TCP 数据包。

TCP 是 [Transmission Control Protocol](http://en.wikipedia.org/wiki/Transmission_control_protocol)（传输控制协议）的缩写。
TCP 用于在预先建立的连接上发送和接收数据流
。TCP 协议本身负责建立连接，
并确保所有已传输数据都被正确接收。

TCP 比 [UDP](UDP.md) 更可靠，
但是使用起来更复杂，
而且需要更多 RAM。需要使用额外的 RAM，
部分是因为需要保留已发送到网络上的数据包，
直到正确收到数据包（以防需要重新传输数据包），
以及需要将多个数据包之间已分割的数据
汇编成一个可靠的流。

另请参阅 [TCP 套接字](socket.md)。

