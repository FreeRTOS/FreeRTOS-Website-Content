---
title: ARP
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


ARP 代表[地址解析协议](http://en.wikipedia.org/wiki/Address_Resolution_Protocol)。

[IP 数据包](internet_protocol.md)
在 [IP 地址](IP_address.md)之间发送，但封装这些数据包的[以太网帧](ethernet_networking_and_addressing.md)
则在
MAC（硬件）地址之间发送。因此，
在将 IP 数据包发送到以太网网络之前，必须知道目标 IP 地址的 MAC 地址
。

地址解析协议
(ARP) 用于获取 MAC 地址信息。FreeRTOS-Plus-TCP
（像大多数 IP 堆栈那样）将 IP 地址到 MAC 地址的映射
存储在 ARP 表（有时称为 ARP 缓存）中。ARP
由 TCP/IP 堆栈自动处理。

