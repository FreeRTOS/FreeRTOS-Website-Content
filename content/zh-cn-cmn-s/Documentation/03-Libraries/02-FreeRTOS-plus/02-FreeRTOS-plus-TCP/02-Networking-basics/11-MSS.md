---
title: MSS
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


MSS 是 [Maximum Segment Size（最大报文段长度）](http://en.wikipedia.org/wiki/Maximum_Segment_Size)的缩写。它
定义了 [TCP](TCP.md) 或 [UDP](UDP.md) 数据包中可发送或接收的最大数据量。
MSS 与 [MTU](MTU.md) 值的不同之处在于
其值仅适用于数据大小，而不适用于帧大小，因此
MSS 并不包括以太网、IP、TCP 或 UDP 协议标头。MSS
取决于 MTU 和选项最大字节数。

从 1526 字节的 MTU 开始的 MSS 计算
示例如下。减去
帧中包含的各个标头消耗的字节数，
即可得到 MSS 大小：

```c
1526  MTU size
 -14  Ethernet header size
 -20  IP protocol header size
 -20  TCP protocol header size
 -12  TCP options bytes
----
1460  MSS size

```

在 FreeRTOS-Plus-TCP 中，MSS 值由 [ipconfigTCP_MSS](TCP_IP_Configuration.md#ipconfigTCP_MSS)
（FreeRTOSIPConfig.h 中的设置）设置。如果未定义 ipconfigTCP_MSS，则将其设置为
默认值 1460。

在上述实例中，计算出的 1460 字节的 MSS 值适用于
局域网 (LAN)，但此值可能太大，无法在 Internet 上使用。
在 Internet 上，MSS 应限制为 1400 字节，以实现最大可靠性。因此，
如果远程节点的 IP 地址位于本地网络之外
（详见[网络掩码](subnet.md) ），
则 FreeRTOS-Plus-TCP 会自动将 MSS 设置为 1400 与
配置的 ipconfigTCP_MSS 值中的较小值。

