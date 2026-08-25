---
title: DNS
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

DNS 是[域名系统](http://en.wikipedia.org/wiki/Domain_Name_System)的缩写，
是一种[域名解析](name_resolution.md)形式。

DNS 可将静态且
人类易读的文本（而非编码）名称映射到 [IP 地址](IP_address.md)。
域名服务器可将文本域名解析为合适的 IP 地址。
例如，在台式计算机的命令控制台中输入"ping www.freertos.org"，
将显示发送到 IP 地址 195.8.66.1 的 ping 请求
（写入时 IP 地址可能会变化），
因为 DNS 服务器将字符串 "www.freertos.org" 解析为了
IP 地址 195.8.66.1。

如果 [ipconfigUSE_DNS](TCP_IP_Configuration.md#ipconfigUSE_DNS)
在 [FreeRTOSIPConfig.h](TCP_IP_Configuration.md) 中被设置为 1，
则可用 FreeRTOS-Plus-TCP API 函数[FreeRTOS_gethostbyname()](API/gethostbyname.md)
将文本名称解析为 IP 地址。

类似运行 FreeRTOS-Plus-TCP 的节点的 IP 地址，
域名服务器的 IP 地址既可以作为 [FreeRTOS_IPInit()](API/FreeRTOS_IPInit.md) 的参数静态配置，
也可以从 [DHCP](DHCP.md) 服务器进行动态配置。

