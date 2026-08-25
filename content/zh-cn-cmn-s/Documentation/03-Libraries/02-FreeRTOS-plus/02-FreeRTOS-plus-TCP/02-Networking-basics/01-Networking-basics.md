---
title: 嵌入式 TCP/IP 网络基础知识
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


### 简介

以下网页链接旨在简要介绍
TCP/IP 和 UDP/IP 网络的概念和术语，以及它们与 FreeRTOS-Plus-TCP 实现的关系。
这些网页只是
提供了一个主题的顶层概述，
而这些主题本身就可以成为一个综合性的主题，因此我们也会在一些地方适时提供外部参考链接
。

不要因为相关主题看着比较复杂而退却。FreeRTOS-Plus-TCP
负责实现这些协议。FreeRTOS-Plus-TCP 用户只需
充分了解 [FreeRTOS-Plus-TCP 配置选项](TCP_IP_Configuration.md)，
知道如何使用标 [准伯克利套接字](http://en.wikipedia.org/wiki/Berkeley_sockets)
接口发送和接收数据即可。
本网站提供 [FreeRTOS-Plus-TCP 联网教程](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)，
随附简单的操作示例和 API
引用。

以下链接列出了一些网络术语，
请依次阅读：

* [以太网联网和寻址](ethernet_networking_and_addressing.md)
* [MTU - 最大传输单元](MTU.md)
* [IP 网络](internet_protocol.md)
* [IP 网络寻址](IP_address.md)
* [ARP - 地址解析协议](ARP.md)
* [子网/网络掩码](subnet.md)
* [网关和路由器](router.md)
* [UDP 网络](UDP.md)
* [TCP 网络](TCP.md)
* [MSS - 最大分段大小](MSS.md)
* [端口号](port_number.md)
* [套接字](socket.md)
* [绑定](bind.md)
* [客户端和服务器](client_server.md)
* [静态 IP 地址](static_ip_address.md)
* [DHCP - 动态主机控制协议](DHCP.md)
* [名称解析](name_resolution.md)
* [DNS - 域名服务](DNS.md)
* [LLMNR - 链路本地多播名称解析](LLMNR.md)
* [NBNS - NetBIOS 名称服务](NetBIOS.md)
* [字节顺序和 Endian](endian.md)

