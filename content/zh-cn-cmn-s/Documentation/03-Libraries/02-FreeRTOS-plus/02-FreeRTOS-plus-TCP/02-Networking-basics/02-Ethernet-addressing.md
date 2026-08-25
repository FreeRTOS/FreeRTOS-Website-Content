---
title: 以太网地址和网络
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


### 以太网网络

数据以[以太网帧](http://en.wikipedia.org/wiki/Ethernet_frame)的形式在本地以太网网络中传输。


### 以太网地址

以太网帧用于在网络的节点之间移动
数据。以太网帧中的数据可能只是
原始数据，但通常与其他协议相关联，
例如[互联网协议l](internet_protocol.md) (IP)，
该协议可进一步携带其他的协议，例如 [UDP](UDP.md) 或 [TCP](TCP.md)。

同一以太网上的不同节点由其 
[MAC 地址](http://en.wikipedia.org/wiki/MAC_address)（硬件地址）标识。
MAC 地址通常被写成由冒号分隔的 6 个八位元组
（ 8 位值）。例如 00:12:34:56:78:90。
本地以太网上的每个节点必须具有唯一的 MAC 地址。

