---
title: "AWS IoT Jobs"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: AWS IoT Jobs 库简介
relatedLinks:
  - title: 作业 Github 存储库
    link: https://github.com/aws/Jobs-for-AWS-IoT-embedded-sdk
externalLinks:
  - title: AWS IoT Jobs Client 库
    link: https://aws.github.io/Jobs-for-AWS-IoT-embedded-sdk/v1.3.0/
 
---

## 引言

AWS IoT Jobs 是通知一个或多个连接的设备有待处理的[“作业”](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/02-Jobs-terminology)的服务。 
您可以通过作业管理您的设备机群，在设备上更新固件和安全证件， 
或执行管理任务，例如重启设备和执行诊断。对于 
服务的文档，请参阅[作业](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) 
（位于 *AWS IoT 核心开发者指南*）。与作业服务互动时使用轻量级发布-订阅协议 [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 
。此库提供了一个方便的 API 来撰写和识别 
作业服务使用的 MQTT 主题字符串。 

AWS IoT Jobs 库以 C 语言编写，其设计符合 [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
和 [MISRA C:2012](https://misra.org.uk/misra-c/) 标准。该库 
不依赖标准 C 库以外的任何其他库。它可与 
任何 MQTT 库和任何 JSON 库一起使用。此库拥有一些[验证](https://www.cprover.org/cbmc/)，用于证明 
安全内存使用和无堆分配，使其适用于 IoT 微控制器，也充分 
可移植到其他平台。

此库可自由使用，且根据 [MIT 开源许可证](/Documentation/03-Libraries/01-Library-overview/04-Licensing)发布。


**AWS IoT Jobs 的代码大小（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| jobs.c | 1.9K | 1.6K |
| 总估算 | 1.9K | 1.6K |
