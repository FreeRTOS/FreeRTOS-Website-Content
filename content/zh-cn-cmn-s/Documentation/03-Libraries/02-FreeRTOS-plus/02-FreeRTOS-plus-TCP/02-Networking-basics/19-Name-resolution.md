---
title: 网络名称解析
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


使用原始 [IP 地址](IP_address.md)对远程节点寻址
并不总是可行，这是因为：

* IP 地址可能会更改。
* 远程计算机的 IP 地址可能未知。
* IP 地址不太好记。

使用人类可读名称来对远程节点寻址
更为便捷。将人类可读名称转换为
IP 地址的过程被称为名称解析。为此，FreeRTOS-Plus-TCP 包括 [DNS](DNS.md)、[LLMNR](LLMNR.md)
和 [NBNS](NetBIOS.md) 实现。

