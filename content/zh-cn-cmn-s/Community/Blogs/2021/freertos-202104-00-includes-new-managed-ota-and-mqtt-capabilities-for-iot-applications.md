---
title: FreeRTOS 202104.00 包括适用于 IoT 应用程序的新的托管式 OTA 和 MQTT 功能
created: 2021-04-29 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---


本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 4 月 29 日发布

FreeRTOS 202104.00 版本包含托管式 [AWS IoT Over-the-Air](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) 更新 (OTA)  
和 [coreMQTT 代理](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)库，以及 
 [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) 自定义指标功能。开发人员 
可以利用这些库远程更新 IoT 设备固件、管理 IoT 设备机群并监控 IoT  
设备机群指标。

这些库已针对受限微控制器的模块化和内存使用进行了优化， 
并已通过代码质量检查（例如 
 [MISRA-C 合规性检查](https://www.misra.org.uk/)、[Coverity 静态分析](https://scan.coverity.com/)、 
和通过 C 语言边界模型检查器  
([CBMC](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)) 自动推理工具 
进行内存安全验证。 

使用 [OTA 库](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)可以更容易地下载和对固件更新进行密码验证。 
。您可以将 OTA 库与您 
首选的 [MQTT 库](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)、[HTTP 库](../../http/index)和底层操作 
系统（例如 FreeRTOS、Linux）结合使用。[coreMQTT 代理](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent) 库通过序列化访问 
 [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 库以及减少实现开销来管理 MQTT 连接。 
例如， MQTT 代理消除了应用程序定期 
调用 [MQTT_ProcessLoop()](../../Documentation/api-ref/coreMQTT/docs/doxygen/output/html/mqtt_processloop_function) 的需求。 
这不仅简化了应用程序设计，还允许多线程应用程序中的任务（线程） 
安全有效地共享相同的 MQTT 连接。请参阅 
 [coreMQTT-Agent 演示](https://github.com/FreeRTOS/coreMQTT-Agent-Demos)，了解在多线程中使用 
 [OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)、[Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)  
 和 [Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) 但共享相同 MQTT 连接的示例 
。[Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) 库允许您将设备 
指标发送到 AWS IoT Device Defender 服务。此库还支持自定义指标，该功能 
可帮助您监控设备机群或用例所独有的运行健康指标。例如， 
您可以定义一个新的指标来监控设备内存使用情况或 CPU 负载。 

您可以在[库页面](/Documentation/03-Libraries/01-Library-overview/Library-categories)找到关于 FreeRTOS 库的更多信息， 
并下载 FreeRTOS 源代码开始使用，代码位于 
[下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 或 [GitHub](https://github.com/FreeRTOS/FreeRTOS)。 


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

