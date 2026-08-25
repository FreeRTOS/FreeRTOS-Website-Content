---
title: coreMQTT
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
description: MQTT C 客户端库简介
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
- title: FreeRTOS 初学者指南
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
- title: 下载 FreeRTOS
  link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
- title: 常见问题
  link: /Why-FreeRTOS/FAQs
external links:
- title: coreMQTT API 引用
  link: https://freertos.github.io/coreMQTT/v2.1.1/
---

**适用于小型 IoT 设备（MCU 或小型 MPU）的 MQTT C 客户端库**


## 简介

coreMQTT 库是 [MQTT](https://en.wikipedia.org/wiki/MQTT) 标准的客户端实现。 
MQTT 标准提供轻量级[发布/订阅](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) 
消息传递协议。此协议在 TCP/IP 上层运行，通常用于机器对机器 (M2M) 和 
物联网 (IoT) 用例。

coreMQTT 库符合 [MQTT 3.1.1](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html)  
协议标准。此库已经过优化，以减少内存占用。此库的设计兼容 
不同用例，从仅使用 
[QoS 0（服务质量等级 0）MQTT PUBLISH 消息](mqtt_terminology)的资源受限平台，到 
使用 [TLS（传输层安全）](../tls/tls-terminology)连接上 [QoS 2 MQTT PUBLISH](mqtt_terminology) 的资源丰富平台。 
该库提供了可组合函数的菜单，用户可以组合使用这些函数来精确地适配特定用例 
。

此库提供了一个高级 API，来连接 MQTT 代理，订阅或取消订阅主题， 
向主题发布消息，接收传入消息。该库还公开了一个低级序列化器/反序列化器 API 
。此低级 API 处理格式化和解析消息，让应用程序完全零开销地控制通向 MQTT 代理的网络连接 
。

该库通过 
[双功能的发送和接收传输接口](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)从底层网络驱动程序中解耦。应用程序编写者可以 
选择现有的传输接口或实现其自己的接口，以适配其应用程序。

此库以 C 语言编写，其设计符合 [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90)  
和 [MISRA C:2012](https://www.misra.org.uk/MISRAHome/MISRAC2012/tabid/196/Default.aspx)。除了 
标准 C 库以外，此库不依赖任何其他库。该库 
包含[验证](https://www.cprover.org/cbmc/)，证明具有内存使用安全性，并且不分配堆， 
因此适用于 IoT 微控制器，也可以完全移植到其他平台。

在 IoT 应用程序中使用 MQTT 连接时，我们建议您使用安全的传输接口， 
例如使用 TLS 协议的接口（如 [MQTT TLS](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) 演示所示）。

此库可免费使用，且根据 [MIT 开源许可](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing/01-Licensing)发布。


**coreMQTT 的代码大小（ARM Cortex-M 的 GCC 生成的示例）**
| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| ---- | --------------------- | --------------------- |
| core_mqtt.c | 4.0K | 3.4K |
| core_mqtt_state.c | 1.7K | 1.3K |
| core_mqtt_serializer.c | 2.8K | 2.2 K |
| 总估算 | 8.5K | 6.9K |

