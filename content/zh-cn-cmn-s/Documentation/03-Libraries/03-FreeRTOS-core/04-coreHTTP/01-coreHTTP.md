---
title: coreHTTP
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
description: coreHTTP 库简介
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
external links:
- title: coreHTTP API 引用
  link: https://freertos.github.io/coreHTTP/v3.0.0/
---

coreHTTP

适用于小型 IoT 设备（ MCU 或小型 MPU）的 HTTP C 客户端库


## 简介

coreHTTP 库是 
[HTTP/1.1](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) 标准子集的客户端实现。HTTP 标准 
提供了一种在 TCP/IP 之上运行的无状态协议，通常用于分布式协作 
超文本信息系统。

coreHTTP 库实现 [HTTP/1.1](https://tools.ietf.org/html/rfc2616) 协议标准的子集 
。此库已经过优化，以减少内存占用。此库提供了一个完全同步的 API， 
允许应用程序完全管理其并发机制。此外，此库只在固定缓冲区上运行， 
因此应用程序可以完全控制其内存分配策略。

此库提供了一个高级的简单 API，用于序列化请求标头、发送请求和接收响应。

该库通过 
[双功能的发送和接收传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)从底层网络驱动程序中解耦。应用程序写入器 
可以选择现有的传输接口或实现其自己的传输接口，以适合其应用程序。

此库以 C 语言编写，设计符合 
[ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
和 [MISRA C:2012](https://www.misra.org.uk/MISRAHome/MISRAC2012/tabid/196/Default.aspx)。此库 
仅依赖于标准 C 库 
和 Node.js 的 [http-parser LTS 版本（v12.19.1）](https://github.com/nodejs/node/tree/v12.19.1/deps/http_parser) 
。此库已被[证明](https://www.cprover.org/cbmc/)具有安全使用内存，不具有堆分配， 
因此适用于 IoT 微控制器，也可以完全移植到其他平台。

在 IoT 应用程序中使用 HTTP 连接时，我们建议您使用安全的传输接口， 
例如使用 TLS 协议的接口（如 [HTTP TLS](http-demo-with-tls-mutual-authentication) 演示所示） 
。

此库可免费使用，且根据 [MIT 开源许可](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing/01-Licensing)发布。


**coreHTTP 的代码长度（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| core_http_client.c | 3.2K | 2.6K |
| api.c (llhttp) | 2.6K | 2.0K |
| http.c (llhttp) | 0.3 K | 0.3 K |
| llhttp.c (llhttp) | 179 | 159 |
| 总估算 | 23.9K | 20.7K |

