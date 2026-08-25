---
title: ICMPv6
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[ICMPv6](https://en.wikipedia.org/wiki/ICMPv6) 是互联网控制消息协议第 6 版（Internet Control Message Protocol version 6）的缩写。 
它是 
[互联网控制消息协议](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)（ICMP）的 IPv6 实现。 
ICMPv6 协议定义了各种消息类型和格式，用于实现不同的 IPv6 协议， 
如[邻居发现协议](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol)（NDP）。

FreeRTOS+TCP 使用 ICMPv6 消息作为框架，以实现 
RA、[邻居发现协议](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol)（NDP） 
和 ICMPv6 回显 ping 请求/回复。

