---
title: "DHCP (IPv4)"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


DHCP 指[动态主机控制协议](http://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol)。

[静态 IP 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/16-Static-IP-address)
在应用程序开发过程中非常有用，但在产品部署过程中并不实用，因为：

* 它们需要硬编码在可执行二进制文件或外部闪存中。

* 如果不事先了解产品部署的网络环境，就不能 
  为产品预先分配 IP 地址。

* 我们事先并不知道网络上会有多少个节点， 
  也不知道在同一时间可能有多少个节点处于活跃状态。

DHCP 提供了一种替代静态 IPv4 地址分配的方案。DHCP 服务器存在于本地网络中， 
用于为同一网络中的节点动态分配 IP 地址。当启用网络的产品启动时， 
它会联系 DHCP 服务器请求其 IP 地址，这样就无需静态配置 
每个节点。

如果 [ipconfigUSE_DHCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp) 和 [ipconfigUSE_IPv4](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/17-DHCP-IPv4) 
在 [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration) 中设置为 1，那么 FreeRTOS-Plus-TCP 将尝试 
从 DHCP 服务器获取 IP 地址，只有在无法联系到 DHCP 服务器的情况下， 
才会恢复使用静态 IP 地址（AutoIP 也在路线图上）。

运行 FreeRTOS-Plus-TCP 的设备可以将其主机名注册到 DHCP 服务器。请参阅 
[ipconfigDHCP_REGISTER_HOSTNAME](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigDHCP_REGISTER_HOSTNAME) 配置 
常量了解更多信息。

专家用户可以使用[应用程序 DHCP 钩子](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfiguse_dhcp_HOOK)
（或“回调”）函数来影响 DHCP 进程。

此外，有关 IPv6 地址的动态分配，请参阅 [DHCPv6](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/18-DHCPv6)。

