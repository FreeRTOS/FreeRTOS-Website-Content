---
title: FreeRTOS Long Term Support 现包含 AWS IoT Over-the-Air 更新、AWS IoT Device Defender 和 AWS IoT Jobs 库
ceated: 2021-03-01 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 3 月 1 日发布

FreeRTOS Long Term Support (LTS) 202012.01 版本现包含 
[over-the-air 更新 (OTA)](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)、[AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender)  
和 [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) 库，这些都来自首个 LTS 版本 (FreeRTOS 202012.00 LTS)。 
在新版本中，开发人员可使用 FreeRTOS LTS 库更新固件，管理设备机群， 
并监控基于微控制器的 IoT 设备机群的指标。此外，开发人员可在两年里享受 
 FreeRTOS 版本提供的稳定功能、安全补丁和关键错误修复 
。

[OTA 库](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)可以更容易地下载和对更新固件进行密码验证 
。您可以将 OTA 库与您首选的 MQTT 库、HTTP 库和 
底层操作系统（例如 FreeRTOS、Linux）结合使用。[Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender)  
库允许客户向 AWS IoT Device Defender 服务发送设备指标。此库 
还支持自定义指标，该功能可帮助您监控设备机群或用例所独有的运行健康指标 
。例如，您可以定义一个新的指标来监控设备内存使用情况或 CPU 使用情况 
。[作业库](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs)可帮助您通知连接的 IoT 设备 
有[待处理的作业](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/02-Jobs-terminology)。作业可用于管理设备机群，更新 
固件和安全证书，或执行管理任务，如重新启动设备和执行 
诊断

远程无线更新固件和监控设备指标对于提高和维护 
 IoT 设备的生命周期安全性至关重要。考虑到这些功能对于 
客户通过 FreeRTOS LTS 库构建 IoT 设备的重要作用，我们已经在 LTS 版本中集成 OTA、Device Defender 
和作业库，即 [FreeRTOS 202012.01 LTS](https://github.com/FreeRTOS/FreeRTOS-LTS) 版本。 
这些库是可添加的：未对已有的 FreeRTOS LTS 库添加任何更改、修复或功能 
。此外，为了让开发人员对所有 LTS 库进行至少两年的维护， 
我们已将对 FreeRTOS 202012.01 LTS 的支持时间延长到 2023 年 3 月 31 日。

与 FreeRTOS LTS 库的其他部分一样，OTA、Device Defender 和作业库已重构， 
以提高设计灵活性、安全性和代码质量。首先，每个 LTS 库均位于其 GitHub 
存储库内，从而使开发人员可以更轻松地在其 FreeRTOS 项目中集成和更新库。 
其次，Device Defender 和作业库已通过 C 语言边界 
模型检查器 ([CBMC](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)) 自动推理工具进行内存安全验证， 
可缓解缓冲区溢出等代码安全问题。最后，所有 LTS 库均已 
经过代码质量检查，包括 [MISRA-C](https://www.misra.org.uk/)   合规性检查 
和 [Coverity](https://scan.coverity.com/) 静态分析，以确保嵌入式系统中代码的安全性、可移植性和可靠性 
（请参阅 [LTS 代码质量检查清单](../../lts-libraries#checklist)）。

您可以在 [FreeRTOS.org](../../lts-libraries) 的 FreeRTOS LTS 库中找到更多信息，并 
下载 FreeRTOS 202012.01 LTS 源代码开始使用，代码位于[下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 
或 [GitHub](https://github.com/FreeRTOS/FreeRTOS-LTS)。


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

