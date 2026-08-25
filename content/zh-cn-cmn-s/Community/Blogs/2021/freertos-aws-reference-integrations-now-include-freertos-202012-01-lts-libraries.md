---
title: FreeRTOS AWS 参考集成现包含 FreeRTOS 202012.01 LTS 库
created: 2021-07-14 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 7 月 14 日发布

FreeRTOS AWS 参考集成指的是预集成的 FreeRTOS 项目，移植入基于微处理器的 
评估板，这些板能够显示与 AWS IoT 核心的端对端连接。这有助于开发人员保存 
几个月的开发成果，加速上市。FreeRTOS AWS 参考集成现 
包含新的托管式 [AWS IoT Over-the-Air](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) (OTA) 更新 
库、[AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) 库、 
[AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) 自定义指标功能（来自 FreeRTOS 
202012.01 LTS 版本）以及 [coreMQTT 代理](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)库（来自 
 [FreeRTOS 202104.00](https://github.com/FreeRTOS/FreeRTOS/releases/tag/202104.00) 版本）。

开发人员可以利用参考集成学会使用各种评估板 
并通过集成库远程更新 IoT 设备固件、管理 IoT 设备机群、监控 
IoT 设备机群指标并简化多线程应用程序中 MQTT 连接的管理。 
有关这些库功能的详细信息，请参阅 FreeRTOS 202012.01 LTS  
公告[博客](/Community/Blogs/2021/freertos-long-term-support-now-includes-aws-iot-over-the-air-update-aws-iot-device-defender-and-aws-iot-jobs-libraries) 
和 FreeRTOS 202104.00版本[博客](/Community/Blogs/2021/freertos-202104-00-includes-new-managed-ota-and-mqtt-capabilities-for-iot-applications)。

您可以在 AWS 参考集成 
[页面](../../aws-reference-integrations)（标记为 “LTS”）上找到使用 LTS 库的评估板列表，并 
下载 202107.00 FreeRTOS AWS 参考集成源代码（代码位于 [GitHub](https://github.com/aws/amazon-freertos) 
或 [FreeRTOS 控制台](https://console.aws.amazon.com/freertos)）。


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

