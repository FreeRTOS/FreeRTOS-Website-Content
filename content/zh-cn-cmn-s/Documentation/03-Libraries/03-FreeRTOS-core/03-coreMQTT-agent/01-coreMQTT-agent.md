---
title: "coreMQTT Agent"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: MQTT C 客户端库简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
externalLinks:
  - title: coreMQTT agent API 引用
    link: https://freertos.github.io/coreMQTT-Agent/v1.2.0/
---


适用于小型 IoT 设备（ MCU 或小型 MPU）的线程安全 MQTT C 客户端库



## 简介

coreMQTT Agent 库是一个高级 API，它为 [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 
增加线程安全性。使用该库可创建一个专用的 MQTT Agent 任务，用于在后台管理 MQTT 连接， 
不需要其他任务进行任何干预。该库为 coreMQTT 的 API 提供了线程安全等价物， 
因此可以在多线程环境中使用。

MQTT Agent 是独立的任务（或执行线程）。它是唯一允许访问 MQTT 库 API 的任务， 
因此可轻松实现线程安全。它通过将所有 MQTT API 调用隔离到单个任务来实现序列化访问， 
而且无需使用信号量或任何其他同步原语。

该库使用线程安全的消息传递队列（或其他进程间通信机制）来序列化 
所有调用 MQTT API 的请求。消息传递实现通过消息传递接口与库解耦， 
该接口允许将库移植到其他操作系统。消息传递接口 
由发送和接收指向代理的命令结构体的函数以及分配这些命令对象的函数组成，
这使得应用程序写入器可以决定适合其应用程序的内存分配策略 
。

此库以 C 语言编写，其设计符合 [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90)  
和 [MISRA C:2012](https://misra.org.uk/misra-c/) 标准。该库没有除 
[coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 和标准 C 库以外，此库不依赖任何其他库。此库 
[已被证明](https://www.cprover.org/cbmc/)具有安全使用内存，不具有堆分配， 
因此适用于 IoT 微控制器，也可以完全移植到其他平台。

此库可自由使用，且根据 [MIT 开源许可证](/Documentation/03-Libraries/01-Library-overview/04-Licensing)发布。


**coreMQTT Agent 的代码大小（使用适用于 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| core_mqtt_agent.c | 1.7K | 1.5K |
| core_mqtt_agent_command_functions.c | 0.3K | 0.2K |
| core_mqtt.c (coreMQTT) | 4.0K | 3.4K |
| core_mqtt_state.c (coreMQTT) | 1.7K | 1.3K |
| core_mqtt_serializer.c (coreMQTT) | 2.8K | 2.2 K |
| 总估计值 | 10.5K | 8.6K |

内存估算包括 [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 库
