---
title: FreeRTOS 202011.00 版本新特征介绍
created: 2020-11-10 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- luciodj
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Lucio Di Jasio](../author/luciodj) 于 2020 年 11 月 10 日发布 

我们很高兴地宣布，FreeRTOS 202011.00 版本现已可立即[下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)。

此版本通过将已发布的 
 [LTS 路线图](../../ltsroadmap)升级到官方 FreeRTOS 发行版中，引入了许多新特性和功能 
——后续内容可参阅 LTS 路线图页面。

鉴于库数量不断增加，我们还做了另外两项变动。首先，正如我们 
在[上一篇文章](https://www.freertos.org/FreeRTOS-V10.4.x.html)中所提到的，我们已经不再使用 
 FreeRTOS 内核的版本号对下载进行版本管理，而是使用时间戳版本管理。 
其次，为了使库更易于使用，我们已将每个库放置在其自己的 Github 存储库中。


## FreeRTOS 库更新

新库符合[ LTS 路线图页面上的代码质量检查清单要求](../../ltsroadmap#checklist)， 
包括越来越多的内存安全验证。为最大限度提高设计灵活性，新库设计为 
独立式，因此它们对除标准 C 库以外的任何东西都没有依赖性， 
因此对 FreeRTOS 或线程没有依赖性。

第一波新增的库为  
IoT 应用程序中常用的安全和连接协议提供与云无关的支持。现在这些库包括：

* **[coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)**：实现 [MQTT v.3.1.1](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html)  
  客户端。此库被设计为可在任何 TCP/IP 堆栈上运行。它可以在不进行多任务处理的情况下使用， 
  或者，正如我们的示例所示，它可以在多线程应用程序中作为代理运行。

* **[coreJSON](//Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)**：实现内存 
  高效的（严格执行 [ECMA-404 标准的](https://www.ecma-international.org/publications/standards/Ecma-404.htm)）[JSON](../../json/json-terminology)  
  解析器，适用于内存占用小，便于轻松操作使用此流行符号序列化的对象， 
  这是许多 IoT 应用程序的要求。

* **[corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)**：实现 
  [OASIS PKCS #11 API 标准](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=pkcs11)) 的子集， 
  用于控制认证信息的加密令牌。这些 API 将帮助您的 IoT 应用程序 
  以可移植方式处理安全身份验证。

最后： 

* **[AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)** 是  
  [AWS IoT Shadow 服务](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)的客户端， 
  旨在使 IoT 设备的状态对应用程序和云服务可用，无论 
  该设备是否处于活动和连接状态。


## FreeRTOS 内核更新

202011.00 包括 FreeRTOS 内核的新补丁程序版本——10.4.2 版本。请注意 FreeRTOS  
内核现在也在[其 GitHub 存储库](https://github.com/FreeRTOS/FreeRTOS-Kernel)中，以便于 
应用（子模块化）到各种项目中。V10.4.2 版本包含多个移植的补丁 
——详细信息请参阅内核的[变更历史记录](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/master/History.txt) 
。


## 其他更新

完整的 FreeRTOS 版本除了内核之外，必定包含多个包含演示 
项目、FreeRTOS Plus 库和第三方库的文件夹。其中，这一新版本有 
以下变化： 

* WolfSSL TLS 库现已更新到 v4.5.0，并添加了一个新的 FIPS 就绪演示。
* 已添加对 ESP IDF v4.2 的支持，以包括最新的 Espressif 工具链版本。

其他更新包括整个项目的 [MISRA C](https://www.misra.org.uk/) 合规性水平提高 
。 


##  另外，

在结束之前，我很高兴宣布推出我们的新视频系列“FreeRTOS 点播视频”，涵盖 
 FreeRTOS 相关话题以及社区成员的常见问题。以下 
是  [Richard Barry 的第一次采访，一起先睹为快吧](https://forums.freertos.org/t/freertos-on-demand-video-the-new-core-libraries-and-what-to-expect-in-lts/)。 
请（在[论坛](https://forums.freertos.org/)中）告诉我们您的想法！ 


## 作者简介

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio 是 Amazon Web Services 的产品经理。过去 20 年里，他在半导体行业 
担任过各种技术和营销职务。作为一个富有见解的高产作者，他发表了 
许多关于嵌入式控制应用程序编程的文章和技术书籍。热爱 
飞行的他又获得了 FAA 和 EASA 私人飞行员执照。  
[查看此作者的文章](../author/luciodj) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

