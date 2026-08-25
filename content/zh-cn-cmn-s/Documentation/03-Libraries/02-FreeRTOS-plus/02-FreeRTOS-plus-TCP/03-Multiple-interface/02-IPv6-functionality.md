---
title: FreeRTOS-Plus-TCP IPv6 功能
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

**注意**：
该 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 项目 [](https://en.wikipedia.org/wiki/IPv6) 
为目前仅支持 IPv4 的 FreeRTOS-Plus-TCP TCP/IP 堆栈增加了 IPv6 功能。虽然由此产生的双 IPv4 / IPv6 
版本功能齐全，但仍在进行优化、测试范围和文档改进 
以及内存安全检查。在这项工作完成之前， 
代码将作为 [FreeRTOS-Plus-TCP GitHub 存储库](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/labs/ipv6_multi)的一个分支提供。


## 简介

IPv6 功能可作为编译时间选项添加。添加后，IPv6 IP 地址可以 
静态配置，也可以使用路由器广告（RA）（与 SLAAC 一起） 
或 DHCP 第 6 版（DHCPv6）自动配置。

当进行无状态地址自动配置 (SLAAC) 时，设备将首先接收网络前缀的地址 
。然后它将使用一个有效的随机 IP 地址， 
并将测试该地址是否已在局域网中使用。这些地址可以是公共互联网地址，也就是说不需要 NAT， 
只需要 IPv6 网关。

IPv6 功能增加了 3 个新模块：

**FreeRTOS_Routing**   
引入了端点和地址解析的概念。请参阅介绍“多个接口”的页面。 
这些是获取 IPv4 和 IPv6 地址所必需的。

**FreeRTOS_ND**   
邻居检测：可处理所有 ICMPv6 消息。它负责（MAC）地址解析，以及缓存、 
ping 和路由器请求。

**FreeRTOS_DHCPv6**   
它是 DHCPv6 客户端。请注意，它将为每个已启用 DHCP 的端点创建会话。

**FreeRTOS_RA**   
这实现了路由器请求和 SLAAC。IPv6 路由器会广播网络前缀， 
而端点将选择自己的 IP 地址。通过发布邻居请求消息，它可以了解到 
所选地址是否唯一地址。


## 演示

[“如何为 IPv6 设置和运行演示”](ipv6-demo.md)页面提供了有关设置 IPv6 演示的说明


## IPv6 函数

[IPv6 和多接口函数](../IPv6-multi-functions.md)页面提供了 
关于使用 IPv6 和多接口所需的新函数的信息。

