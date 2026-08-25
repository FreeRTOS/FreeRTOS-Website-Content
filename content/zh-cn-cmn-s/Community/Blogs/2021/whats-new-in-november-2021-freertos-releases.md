---
title: 2021 年 11 月 FreeRTOS 版本新特性介绍
created: 2021-11-12 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 11 月 12 日发布

我们很高兴向大家介绍以下最新内容： 

* FreeRTOS 下载内容目前包含一个代码示例，演示了如何将 
  应用程序使用特权模式的时间降至最低。此模式用于微控制器 (MCU) FreeRTOS 移植， 
  支持内存保护单元 (MPU)。这些  带 MPU 支持的 [FreeRTOS 移植](../../FreeRTOS-MPU-memory-protection-unit)可以 
  通过以非特权模式运行应用任务，增强 MCU 应用程序的稳定性和安全性。 
  因为应用程序只能访问自己的堆栈和预配置的内存区域。以 
  特权模式运行在这些启用 MCU 的 MPU 上的唯一应用程序代码段是中断服务程序 (ISR)。 
  示例代码演示了如何缩短 ISR 时间，并将应用程序的大部分工作 
  延迟到非特权 FreeRTOS 任务。这有助于通过最大程度减少处于特权模式的时间， 
  提高应用程序的安全性。如需了解更多内容并开始入门，请访问 
  [演示页面](/safe-interrupt-demo-nxp-lpcxpresso55s69)并下载代码示例，示例位于 
  [下载页面](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) 或 [GitHub](https://github.com/FreeRTOS/FreeRTOS)。

* 去年，我们[推出了](/Community/Blogs/2020/introducing-the-freertos-cellular-library) 
  一个新 FreeRTOS 库的预览，旨在简化 IoT 应用程序的开发， 
  这些应用程序可通过[蜂窝 LTE-M 技术](https://en.wikipedia.org/wiki/LTE-M)连接至云端。我们很高兴地 
  宣布 FreeRTOS 蜂窝 LTE-M 接口库现在是 FreeRTOS 主下载内容的一部分。 
  此次发布之后，开发人员将能更轻松地构建通过蜂窝 LTE-M 协议连接到云服务的 IoT 设备 
  。要了解有关 FreeRTOS 蜂窝接口库的详细信息，请访问 
  [库页面](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface)，并下载 
   [FreeRTOS 蜂窝接口库](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface) 
  和[演示]。(https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Cellular_Interface_Windows_Simulator) 
  FreeRTOS 主下载内容包含 AWS IoT 蜂窝模块参考集成，这些蜂窝模块来自 
   Sierra Wireless、u-blox 和 Quectel 等供应商。

我们期待您的反馈。如有任何意见或要求，请通过 [FreeRTOS 论坛](https://forums.freertos.org/)联系我们 
！ 


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

