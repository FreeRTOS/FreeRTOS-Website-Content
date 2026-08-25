---
title: LLMNR
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

LLMNR 是 [Link Local Multicast Name Resolution](http://en.wikipedia.org/wiki/Link-local_Multicast_Name_Resolution)（链路本地多播名称解析）的缩写，
这是用于[名称解析](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/19-Name-resolution)的协议。

LLMNR 是在局域网上使用的多播协议。所有主要 Web 浏览器使用此方法 
解析不包含点 ('.') 的名称。例如，如果您尝试打开网页
http://my_freertos_device/index.html，Web 浏览器将发送 LLMNR 请求以尝试解析 
名称 "my_freertos_device"。

所有 LLMNR 数据包都发送到 IP 地址 224.0.0.252，对应的 MAC 地址为
01:00:5E:00:00:FC，因此为确保 LLMNR 正常工作，网络接口 (MAC) 必须编程为
接受发送到该地址的数据包。此外， 
[ipconfigUSE_LLMNR](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_LLMNR)
在 FreeRTOSIPConfig.h 中必须定义为 1，并且
用户必须提供回调函数 xApplicationDNSQueryHook() 的实现，
该函数将字符指针作为参数，在传入函数的名称
与用于标识节点的名称相匹配时返回 pdTRUE。

