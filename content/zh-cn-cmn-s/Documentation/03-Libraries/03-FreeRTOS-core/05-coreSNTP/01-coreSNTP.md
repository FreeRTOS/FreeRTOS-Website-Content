---
title: 适用于小型 IoT 设备（ MCU 或小型 MPU）的 SNTP C 客户端库
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
description: coreSNTP 库简介
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
externalLinks:
- title: coreSNTP API 引用
  link: https://freertos.github.io/coreSNTP/v1.2.0/
---


## 简介

coreSNTP 库提供**简单网络时间协议 (SNTP)** 客户端， 
允许设备将其系统时钟与时间服务器同步。此库实现了 
[RFC 4330](https://tools.ietf.org/html/rfc4330) 定义的 SNTPv4 规范。SNTP 客户端可同时 
向 NTP 和 SNTP 服务器请求时间。 

该库提供了两个 API 层，为应用开发者提供不同程度的开发灵活性 
。应用程序开发者可以使用这两层中的任何一层 
在其应用程序中创建 SNTP 客户端：

1. **序列化器/反序列化器和和实用程序**——这一层提供了序列化 SNTP 时间请求 
   和反序列化 SNTP 响应数据包的功能，以及一些实用程序函数， 
   对于在应用程序中设置 SNTP 客户端时很有帮助。

2. **客户端**——该层为网络操作提供额外的***托管***功能， 
   包括 DNS 解析、通过 UDP 发送和接收 SNTP 数据包、为安全起见验证服务器（如果启用）、 
   通知系统根据服务器提供的信息修正时间， 
   以及处理服务器拒绝时间请求的情况。该层调用序列化器/反序列化器层， 
   对网络上发送和接收的 SNTP 数据包进行序列化和反序列化。(注意：该层通过库提供的接口的用户定义实现 
   执行网络和身份验证操作。）

**序列化器/反序列化器层**不依赖于任何接口。它可以被集成到一个应用程序中按原样使用， 
而**客户端层**通过暴露网络 I/O、 
加密计算以及获取和更新系统时间的接口操作与平台特定的调用解耦。如果 
针对**客户端**层进行开发，必须为平台实现这些接口。关于接口的更多信息， 
请参阅[移植指南](../Documentation/api-ref/coreSNTP/docs/doxygen/output/html/sntp_porting)。

此库以 C 语言编写，设计符合 
[ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 和 [MISRA C:2012](https://www.misra.org.uk/)。 
除标准 C 库以外，该库不依赖于其他库。该库 
[已被证明](https://www.cprover.org/cbmc/)具有安全使用内存，不具有堆分配， 
因此适用于 IoT 微控制器，也可以完全移植到其他平台。

当您在您的应用程序中设计一个用于时间同步的 SNTP 客户端时， 
我们建议您使用验证来与您选择的 SNTP/NTP 服务器进行通信。相互身份验证 
可防止对服务器响应的恶意修改或欺骗，从而防止 
设备中时间的恶意破坏。使用 coreSNTP 库的验证的例子，请参阅 
coreSNTP 演示。

此库可免费使用，且根据 [MIT 开源许可发布](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing/01-Licensing)。

**coreSNTP 的代码大小（与 GCC 为 ARM Cortex-M 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| core_sntp_client.c | 1.5K | 1.2K |
| core_sntp_serializer.c | 1.0K | 0.8K |
| 总估计值 | 2.5K | 2.0K |

