---
title: MTU 和 MTU 大小
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


### MTU

MTU 是 [Maximum Transmission Unit（最大传输单元）](http://en.wikipedia.org/wiki/Maximum_transmission_unit)的缩写，
它是硬件（物理层）的一个特征。
MTU 的大小用八位字节（8 位值）表示。


### MTU 大小

MTU 大小定义了可以发送到网络或从网络接收的最大数据包或帧的大小
。
如果应用程序发送了适合一帧的一小块数据，
那么只有一帧的数据将发送到网络。
如果应用程序发送的数据块大于 MTU 大小，
则数据将被拆分为多个数据包，
每个数据包将创建一个小于或等于 MTU 大小的帧
。

在 FreeRTOS-Plus-TCP 中， MTU 以字节为单位指定，并通过 
[ipconfigNETWORK_MTU](TCP_IP_Configuration.md#ipconfigNETWORK_MTU) 设置进行设置，
（位于 FreeRTOSIPConfig.h 中）。检查您的 MAC 或以太网硬件的规格，
为您的系统找到正确的设置。
某些 MAC 设备限制为 1400。

另请参阅 [MSS](MSS.md)。

