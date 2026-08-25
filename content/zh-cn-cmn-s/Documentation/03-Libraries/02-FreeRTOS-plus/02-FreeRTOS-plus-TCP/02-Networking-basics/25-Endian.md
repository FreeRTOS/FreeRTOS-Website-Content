---
title: 小 Endian，大 Endian
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


不同的 MCU 能以不同方式存储多字节值，
如两个字节的 uint16_t 或四个字节的 uint32_t。首先存储
最重要的字节的微控制器被称为大 Endian。首先存储
最不重要字节的微控制器被称为小 Endian。
将字节存储在运行 FreeRTOS-Plus-TCP 的 MCU 上的方式
被称为*主机字节序*。

非连接应用程序的编写者很少需要考虑
他们的目标 MCU 如何在内部存储数据。
如果数据以小 Endian 顺序写入内存，则会被
从内存中以小 Endian 的顺序读回，因此读回的值将
与最初写入的值相匹配。

当 MCU 连接时就较为复杂，因为
无法保证连接网络上的所有 MCU
都将具有相同的字节序。网络上的所有 MCU
必须事先约定用于发送和接收数据的字节序。
传输中的数据所使用的字节序称为*网络字节
序*。

在 [TCP/IP](TCP.md)
网络中，发送数据首先发送最重要的字节，
使 TCP/IP 网络成为有效的大 Endian。因此，
发送到 TCP/IP 网络的小 endian MCU 必须交换
多字节值发送到网络之前字节在这些值中
出现的顺序，以及使用这些多字节值之前
字节在从网络接收到的多字节值中出现的顺序
。大 endian MCU无需执行任何
字节交换，因为 MCU（主机字节
序）的 endian 匹配网络的约定 Endian（网络字节序）。

**注意：**字节交换由 TCP/IP 堆栈执行，用户
 无需手动交换字节。

