---
title: "AWS IoT Device Defender"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 库
description: AWS IoT Device Defender 库简介
relatedLinks:
  - title: Device defender Github 存储库
    link: https://github.com/aws/Device-Defender-for-AWS-IoT-embedded-sdk
externalLinks:
  - title: API 引用
    link: https://aws.github.io/Device-Defender-for-AWS-IoT-embedded-sdk/v1.3.0/
 
---

## 引言

AWS IoT Device Defender 库允许您将安全指标从您的 IoT 设备发送到 
AWS IoT Device Defender 服务。AWS IoT Device Defender 服务可持续监控设备的安全指标， 
基于您为每个设备定义的适当行为来发现偏离 
。如果出现问题，AWS IoT Device Defender 会发出警报， 
以便您可以采取行动解决问题。有关 AWS IoT Device Defender 的更多信息， 
请参阅 [AWS IoT 文档](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html)。 
使用 [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)（轻量级发布-订阅协议）与 AWS IoT Device Defender 服务进行交互 
。此库提供了一个方便的 API 来撰写和识别 
AWS IoT Device Defender 服务所使用的 MQTT 主题字符串。 

此库以 C 语言编写，其设计符合 [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90)  
和 [MISRA C:2012](https://misra.org.uk/misra-c/) 标准。该库 
不依赖标准 C 库以外的任何其他库。它也没有 
任何平台依赖性，如线程或同步。它可以与任何 MQTT 
库以及任何 [JSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/02-coreJSON-terminology) 或 [CBOR](https://cbor.io/) 库一起使用。该库 
[已被证明](https://www.cprover.org/cbmc/)具有安全使用内存，不具有堆分配， 
因此适用于 IoT 微控制器，也可以完全移植到其他平台。

此 AWS IoT Device Defender 库可免费使用，且根据 [MIT 开源许可发布](/Documentation/03-Libraries/01-Library-overview/04-Licensing)。


**AWS IoT Device Defender 代码大小（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| defender.c | 1.1K | 0.6K |
| 总估计值 | 1.1K | 0.6K |
