---
title: "AWS IoT 核心 MQTT 文件流嵌入式 C"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: AWS IoT 核心 MQTT 文件流嵌入式 C 客户端库简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

### 引言

在 AWS IoT 中，流是一种可公开寻址的资源，是可传输到 IoT 设备的文件列表的抽象。MQTT 文件流库使用 MQTT 协议完成这种传输。它支持 JSON 和 CBOR 格式来发送请求和接收数据。有关流和基于 MQTT 的文件传输的更多信息可以在[此处](https://docs.aws.amazon.com/iot/latest/developerguide/mqtt-based-file-delivery.html)找到。

此库已通过代码质量检查，包括验证函数的 [GNU 复杂性分数](https://www.gnu.org/software/complexity/manual/complexity.html)均未超过 8 分，以及检查代码与 [MISRA 编码标准](https://www.misra.org.uk/)中强制性规则的偏差。与 MISRA C:2012 指南的偏差记录在 [MISRA 偏差](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c/blob/main/MISRA.md)中。此库还使用 [Coverity 静态分析](https://scan.coverity.com/)工具进行了静态代码分析，并通过 [CBMC 自动推理工具](https://www.cprover.org/cbmc/)验证了内存安全性。

此库可免费使用，且根据 MIT 开源许可发布。

**AWS IoT 核心 MQTT 文件流嵌入式 C 库的代码大小（通过 GCC 为 ARM Cortex-M 生成的示例）**

| 文件 | 使用 -O1 优化 | 使用 -Os 优化 |
| ---- | --------------------- | --------------------- | 
| MQTTFileDownloader.c | 1.1K | 1.0K |
| MQTTFileDownloader_cbor.c | 0.8K | 0.6K |
| MQTTFileDownloader_base64.c | 0.6K | 0.6K |
| core_json.c | 2.9K | 2.4K |
| cborparser.c | 2.8K | 2.2K |
| cborencoder.c | 2.0K | 0.7K |
| cborencoder_close_container_checked.c | 0.1K | 0.1K |
| 总估计值 | 10.3K | 7.6K |


### MQTT 文件流配置文件

MQTT 文件流库公开了构建库所需的构建配置宏。[MQTTFileDownloader_defaults.h](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c/blob/main/source/include/MQTTFileDownloader_defaults.h) 中定义了所有配置及其默认值的列表。要为配置宏提供自定义值，应用程序可向库提供名为 MQTTFileDownloader_config.h 的自定义配置文件。

默认情况下，需要 `MQTTFileDownloader_config.h` 自定义配置来构建库。要禁用此要求并使用默认配置值构建库，请提供 `MQTT_STREAMS_DO_NOT_USE_CUSTOM_CONFIG` 作为编译时预处理器宏。

因此，MQTT 库可以由以下两种方式构建：
  - 在应用程序中定义 `MQTTFileDownloader_config.h` 文件，并将其添加到程序库的包含目录列表中，或
  - 为构建库定义 `MQTT_STREAMS_DO_NOT_USE_CUSTOM_CONFIG` 预处理器宏。

**MQTT 文件流库工作流程**

[![MQTT 文件流库工作流程](/media/2024/mqtt-file-streams-lib.png)](/media/2024/mqtt-file-streams-lib.png)

_点击放大_

### 如何将 MQTT 流库用于 OTA 更新

请按照以下步骤操作：
  1. 用户将需要使用[作业库](https://github.com/aws/Jobs-for-AWS-IoT-embedded-sdk)和 
     [MQTT 流库](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c)，才能使将 AWS IoT Jobs 用于 OTA 更新。
  1. 收到作业文件后，将从 AWS IoT Jobs 库中提取作业 ID。
  1. 下载的 MQTT 数据流可使用 `mqttDownloader_init` 进行初始化。这里传递的是 
     使用 OTA 作业解析器从 AWS IoT OTA 作业文件中提取的参数。这将初始化 MQTT 文件下载器。它还会为 DATA 和 Get Stream Data 主题创建主题名称。
  1. 当收到请求文件块的 OTA 事件时：
      1. `mqttDownloader_createGetDataBlockRequest` 用于创建获取数据块请求。MQTT 流库只 
         创建获取块请求。要发布请求，需要使用 coreMQTT 等 MQTT 库。
      1. MQTT 库将调用 `mqttDownloader_isDataBlockReceived` API 来确定是否已收到 OTA 块。 
         API 通过比较传入的 MQTT 消息主题和 MQTT 流主题来执行此操作。
      1. 如果收到 OTA 块，MQTT 数据流库将从传入的 MQTT 消息中提取并解码收到的 OTA 
         数据块。API `mqttDownloader_processReceivedDataBlock` 将用于解码应用程序要处理的块。
  1. 由用户自行决定为 OTA 更新设计平台抽象层 API。这些 PAL API 可以 
     让用户执行以下功能：
  1. 中止 OTA 传输（如果 IOT 作业 OTA 需要此操作）
  1. 各种文件操作，如创建、删除和激活新接收的映像。
  1. 存储接收到的数据块中的数据——一旦数据流库处理了接收到的数据块，就需要进行存储。

_注意：创建、删除和激活操作不需要抽象层。应用程序集成器可直接使用其特定于移植的 API 进行文件操作、签名验证和启动加载。_

### 文档

  - [API 引用](https://aws.github.io/aws-iot-core-mqtt-file-streams-embedded-c/latest/)

### 演示：

这些演示利用 MQTT 文件流库演示 OTA 更新。

  1. [OTA（使用简单 OTA Orchestrator）](https://www.freertos.org/freertos-core/over-the-air-updates/mqtt-simple-orchestrator.html)
  1. [OTA（使用 OTA Agent Orchestrator）](https://www.freertos.org/freertos-core/over-the-air-updates/mqtt-ota-agent-orchestrator.html)
