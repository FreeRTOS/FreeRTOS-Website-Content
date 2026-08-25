---
title: "AWS IoT Device Shadow"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: AWS IoT Device Shadow 库简介
relatedLinks:
  - title: 设备阴影 Github 存储库
    link: https://github.com/aws/Device-Shadow-for-AWS-IoT-embedded-sdk
externalLinks:
  - title: AWS IoT Device Shadow 库
    link: https://aws.github.io/Device-Shadow-for-AWS-IoT-embedded-sdk/v1.3.0/
---


## 引言

AWS IoT Device Shadow 库使您能够存储和检索 
每个 IoT 设备的当前状态（["阴影"](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/03-Shadow-terminology)）， 
这些设备在您的 [AWS IoT](https://aws.amazon.com/iot/) 账户中注册。设备的阴影是对 
您的 IoT 设备的持续虚拟表示，即使设备处于离线状态，您也能在应用程序中与其互动 
。作为其“阴影”捕获的设备状态本身表示为 [JSON](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) 文档 
。您可以通过 MQTT 或 HTTP 向 AWS IoT Device Shadow 服务发送命令来查询 
最新已知的设备状态，或更改状态。每个 IoT 设备的阴影通过 
对应的 "thing" 名称唯一标识。“thing” 是特定 IoT 设备或逻辑实体 
（位于 AWS 云中）的表示。 
请参阅[使用 AWS 管理设备IoT](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html)， 
了解更多信息。关于阴影的更多详细信息，请参阅 
[AWS IoT 文档](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)。

AWS IoT Device Shadow 库以 C 语言编写，其设计符合 
[ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
和  [MISRA C:2012](https://misra.org.uk/misra-c/) 标准。除了 
标准 C 库以外，此库不依赖其他库。它也不依赖任何平台， 
例如线程或同步。它可与任何 MQTT 库和任何 JSON 库一起使用 
。此库拥有一些[验证](https://www.cprover.org/cbmc/)用于证明安全内存使用，而且 
不执行任何动态内存分配，使其适用于 IoT 微控制器，但也充分 
可移植到其他平台。

AWS IoT Device Shadow 库可以自由使用，并根据 [MIT 开源许可证](/Documentation/03-Libraries/01-Library-overview/04-Licensing)发布。

**AWS IoT Device Shadow 的代码大小（通过 ARM Cortex-M 的 GCC 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| --- | --- | --- |
| shadow.c | 1.2K | 0.9K |
| 总估计值 | 1.2K | 0.9K |
