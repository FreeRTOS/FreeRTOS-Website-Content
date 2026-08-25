---
title: 2020 年 7 月 FreeRTOS 版本新特性介绍
created: 2020-07-17 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 发表于 2020 年 7 月 17 日

很高兴分享以下最新动态：

1. 关于 [FreeRTOS LTS 版本](../../ltsroadmap) 的进展：

   * 重构 MQTT 库：[200717_LTS_development_snapshot.zip](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 文件包含 
     我们在完成 MQTT 库的重构和质量检查清单方面的进展 
     。如今，您可更为轻松地将 MQTT 库应用于各种项目， 
     包括不使用 FreeRTOS 的项目。如需查看重构 MQTT 库的详细信息，请点击[此处](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)； 
     如需查看用于演示该库最基本使用场景的预配置项目， 
     请点击[此处](../../mqtt/basic-mqtt-example)。后续我们将推出演示更为复杂 
     使用场景的预配置项目。有关我们即将发布的长期支持 (LTS) 版本的更多详细信息， 
     请访问 [LTS 路线图页面](../../ltsroadmap)。

   * OTA 暂停和恢复：[200717_LTS_development_snapshot.zip](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 文件还包含 
     OTA 库的增强功能。现在，FreeRTOS 设备可以在断开网络连接的情况下暂停正在进行的 OTA， 
     然后在重新连接网络后恢复 OTA。这有助于在网络连接不稳定的情况下快速完成 OTA 下载 
     。如需查看 OTA 库的详细信息， 
     请点击[此处](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)。

   如需查看增强功能的完整列表，请参阅[更新日志](https://github.com/FreeRTOS/FreeRTOS/tree/V200717_LTS_development_snapshot/CHANGELOG) 
   。
   
2. AWS 参考集成：

   * [202007.00 版](https://github.com/aws/amazon-freertos/tree/202007.00) AWS 参考集成 
     包括针对 Cypress PSoC 64 标准安全微控制器的新集成。要想 
     充分利用 FreeRTOS 的功能和优势， 
     请使用 Cypress [PSoC 64 标准安全 AWS Wi-Fi 蓝牙先锋套件](https://devices.amazonaws.com/detail/a3G0h0000088AgXEAU)， 
     该套件由 Cypress 提供。有关详细信息，请点击[此处]。(../../aws-reference-integrations)


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户 
和嵌入式开发者将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

