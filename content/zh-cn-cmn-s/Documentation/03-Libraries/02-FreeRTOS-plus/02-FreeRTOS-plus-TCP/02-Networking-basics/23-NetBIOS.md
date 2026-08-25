---
title: NBNS
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


NBNS（有时称为 WINS ）是 [NetBIO Name Service](http://wiki.wireshark.org/NetBIOS/NBNS) 的缩写，
这是用于[名称解析](name_resolution.md)的协议。

NBNS 执行与 [LLMNR](LLMNR.md) 相同的函数，
但使用 [UDP](UDP.md) 广播数据包
而非组播数据包。浏览器通常只在尝试使用 LLMNR 失败后，
才尝试使用 NBNS。

[ipconfigUSE_NBNS](TCP_IP_Configuration.md#ipconfigUSE_LLMNR)
必须在 FreeRTOSIPConfig.h 中设置为 1 才能
启用 NBNS。与 LLMNR 一样，应用程序作者必须提供
xApplicationDNSQueryHook() 回调函数，该函数
将字符指针作为参数，在传入函数的名称
与用于标识节点的名称相匹配时返回 pdTRUE。

