---
title: FreeRTOS 202107.00 版本现包含 SNTP 库，可获取 IoT 应用程序中的时间信息
created: 2021-07-23 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 7 月 23 日发布

FreeRTOS [202107.00 版本](../../faq-github-repository-structure-versioning#question2)现已包含 
简单网络时间协议 (SNTP) 客户端库 ，以便开发人员 
在其基于 FreeRTOS 的 IoT 应用程序中轻松添加对时间信息的支持。SNTP 客户端库 
名为 [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP)，用于同步设备和云端之间的时钟。

您可以在设备需要显示时间的 IoT 应用程序中使用 coreSNTP，或者在其业务 
逻辑（例如控制温度和照明）中使用。此外，您可以使用 coreSNTP 库 
在 TLS 与云端握手期间验证证书，或在需要时生成签名以验证云存储请求 
（例如   [SigV4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
签名，用于 HTTP 向 Amazon 简单存储服务发出请求）。SNTP 功能 
对于在没有外部电源的情况下无法保留时间和日期信息的 IoT 设备尤其重要（例如 
没有实时时钟模块的 IoT 设备）。有关 coreSNTP 库的更多详细信息，请参阅 
 [readme](https://github.com/FreeRTOS/coreSNTP/blob/main/README)。

您可以先下载 FreeRTOS 源代码，代码位于 [下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)  
或 [GitHub](https://github.com/FreeRTOS/FreeRTOS)，并了解 
[库页面](/Documentation/03-Libraries/01-Library-overview/Library-categories)中的更多信息。


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

