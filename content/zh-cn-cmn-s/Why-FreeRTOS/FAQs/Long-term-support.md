---
title: "FreeRTOS 常见问题 - 什么是长期支持 (LTS) 版本？"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 关于 FreeRTOS Long Term Support (LTS) 版本的常见问题
---


## FreeRTOS Long Term Support (LTS) 涵盖哪些库？

请参阅 [LTS 库](Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries.md)页面，了解更多详细信息。


## FreeRTOS LTS 库的支持期限是多长？

FreeRTOS LTS 库的支持期限为两年。最新 LTS 版本，FreeRTOS 202406.01 
LTS 将收到 AWS 认为关键的安全和故障修复，直至 2026 年 6 月 30 日。 
对上一个 LTS 版本（即 FreeRTOS 202012.01 LTS）的支持将于 2024 年 10 月 31 日结束。


## 使用 FreeRTOS LTS 库有哪些好处？

对于更新生产设备中的库而言，FreeRTOS LTS 库有助于降低其维护和测试成本 
。FreeRTOS 主线库可以引入新功能和关键 
修复，且对于临近生产的项目可能很难仅包含关键修复。 
FreeRTOS LTS 库还可提供两年的可预测性和功能稳定性，并接收安全更新和关键故障修复，以帮助确保设备安全 
。


## 从哪里获取 FreeRTOS LTS 库?

如需获取 FreeRTOS LTS 库，可以克隆 
[FreeRTOS-LTS GitHub 存储库](https://github.com/FreeRTOS/FreeRTOS-LTS)或各个 LTS 
库，或者从以下位置下载最新的 FreeRTOS LTS zip 文件： 
[下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)。


## 如何将 FreeRTOS LTS 库集成到我的项目中？

您可以在项目中包含或子模块化单个 LTS 库，或者通过从其相应的存储库克隆单个库来更新入 LTS 库 
。例如，您可以 
从 coreMQTT GitHub 存储库下载代码，将您的项目更新至 FreeRTOS LTS MQTT 库。


## 如何下载 FreeRTOS LTS 补丁并查找相关信息？

您可以访问 
LTS 库页面中的 “[FreeRTOS LTS 补丁](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries.md#freertos-lts-patches)” 
部分了解最新信息，或者订阅 GitHub 的 
FreeRTOS 202406.03 LTS 存储库通知。FreeRTOS LTS 版本使用基于日期的版本控制方案 (YYYYMM)， 
后跟一个补丁序号 ( .XX )。例如，FreeRTOS 202012.02 LTS 指的是 
 2020 年 12 月 FreeRTOS LTS 版本的第二个补丁。您可以使用关联的下载链接从 GitHub 获取最新补丁 
。


## FreeRTOS LTS 需要什么软件许可证？

FreeRTOS LTS 库凭借 MIT 开源许可证免费分发。 


## 需要付费才能使用 FreeRTOS LTS 库吗？

不需要。 FreeRTOS LTS 库对 MIT 开源许可证所涵盖的所有用户免费开放。


## FreeRTOS LTS 由谁发布和支持？

AWS 将发布 FreeRTOS LTS 库并对其进行持续维护，以供 
FreeRTOS 社区使用。我们鼓励 FreeRTOS 社区以 GitHub 拉取请求的形式提供反馈并贡献代码 
。 


## FreeRTOS LTS 的发布周期为多久？

我们预计新的 FreeRTOS LTS 版本将每隔 1.5 年发布一次。


## 什么是安全更新和关键故障修复的 SLA？

我们的目标是在成功实现缓解措施到发布更新的七天内解决 FreeRTOS LTS 库的安全漏洞和严重故障 
。 


## 可以获得超过两年的维护支持吗？

可以，请参阅 
[FreeRTOS 延长维护计划](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan)， 
了解更多详细信息。
