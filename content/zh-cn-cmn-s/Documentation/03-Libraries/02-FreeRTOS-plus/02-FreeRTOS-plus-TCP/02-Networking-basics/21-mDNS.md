---
title: mDNS
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

mDNS 是[多播域名系统（Multicast Domain Name System）](https://en.wikipedia.org/wiki/Multicast_DNS)的缩写， 
是一种[域名解析](name_resolution)形式。

mDNS 是 [DNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/20-DNS) 服务的一种变体， 
是一种[域名解析](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution)形式。当 mDNS 客户端 
需要解析一个主机名时，它会发送 [IP 多播](https://en.wikipedia.org/wiki/IP_multicast)查询消息， 
要求拥有该名称的主机表明自己的身份。

mDNS 消息是使用以下寻址方式发送的多播 UDP 数据包：

+ [IPv4 地址](https://en.wikipedia.org/wiki/IPv4_address) 224.0.0.251 
  或 [IPv6 地址](https://en.wikipedia.org/wiki/IPv6_address) ff02::fb
+ [UDP 端口](https://en.wikipedia.org/wiki/UDP_port) 5353
+ 使用[以太网帧](https://en.wikipedia.org/wiki/Ethernet_frame)时， 
  [标准 IP 多播 MAC 地址](https://en.wikipedia.org/wiki/Multicast_address#Ethernet) 
  为 01:00:5E:00:00:FB（[IPv4](https://en.wikipedia.org/wiki/IPv4)）或 33:33:00:00:00:FB 
  （[IPv6](https://en.wikipedia.org/wiki/IPv6)）。

如果 [ipconfigUSE_DNS](TCP_IP_Configuration#ipconfigUSE_DNS) 
和 [ipconfigUSE_MDNS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_MDNS) 
在 [FreeRTOSIPConfig.h](TCP_IP_Configuration) 中设置为 1，那么 FreeRTOS-Plus-TCP API 
函数 [FreeRTOS_gethostbyname()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/19-gethostbyname) 
可用于将文本名称解析为 IP 地址（前提是主机名带有后缀 “.local”）。

