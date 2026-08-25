---
title: 路由器和网关
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


### 路由器

[网络掩码](subnet.md)用于将 [IP 地址](IP_address.md)
细分为提供路由信息的字节和提供本地地址信息的字节。
如果目标 IP 地址与子网掩码进行按位与操作的结果与本地 IP 地址与子网掩码进行按位与操作的结果**不**匹配， 
则这两个 IP 地址**不**在同一个网络上。
在这种情况下，发送到目标地址的数据包无法直接发送，
而必须发送到路由器进行智能
网际路由。


### 网关

网关地址是路由器的 IP 地址-
路由器是通往其他（远程）网络的网关。

FreeRTOS-Plus-TCP 确定 [IP 数据包](internet_protocol.md)
是否可以直接发送，或者需要发送到路由器。
FreeRTOS-Plus-TCP 用户只需提供网关地址。与 IP 地址一样，
网关的 IP 地址既可以作为 [FreeRTOS_IPInit()](API/FreeRTOS_IPInit.md) 的参数静态配置，
也可以从 [DHCP](DHCP.md) 服务器进行动态配置。

