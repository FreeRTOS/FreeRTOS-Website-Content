---
title: 静态 IP 地址
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

请注意，每个网络节点都有一个 [IP 地址](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/05-IP-address)。如果 IP 地址为“静态”， 
则此为预分配地址，从不发生变化。

在 FreeRTOS-Plus-TCP API 中，在 
调用 [FreeRTOS_IPInit_Multi](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/31-FreeRTOS_IPInit_Multi) 之前， 
需要添加 IPv4 地址 
（通过 [FreeRTOS_FillEndPoint](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/64-FreeRTOS_FillEndPoint)）作为端点，或添加 IPv6 地址 
（通过 [FreeRTOS_FillEndPoint_IPv6](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/65-FreeRTOS_FillEndPoint_IPv6)） 
作为其参数之一。如果 
[ipconfigUSE_DHCP](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_DHCP) 
或 [ipconfigUSE_DHCPv6](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_DHCPv6) 
设置为 0 或者 [ipconfigUSE_DHCP](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_DHCP) 
或 [ipconfigUSE_DHCPv6](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_DHCPv6) 
设置为 1，但无法联系上 [DHCP 服务器](/DHCP-IPv4)，则端点/IP 地址将被用作静态 IP 地址。

