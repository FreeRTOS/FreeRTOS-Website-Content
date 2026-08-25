---
title: "FreeRTOS + AWS IoT 解决方案"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 内核简介
relatedLinks:
  - title: AWS IoT OTA 库
    link: /Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates
  - title: AWS IoT Device Shadow 库
    link: /Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow
  - title: AWS IoT Jobs 库
    link: /Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs
  - title: AWS IoT Device Defender 库
    link: /Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender
  - title: AWS IoT Fleet Provisioning 库
    link: /Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning
  - title: AWS IoT 签名版本 4 库
    link: /Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4
  - title: AWS IoT Quick Connect
    link: /Why-FreeRTOS/Quick-Connect
  - title: AWS 合作伙伴设备目录
    link: https://devices.amazonaws.com/search?page=1&sv=freertos

previous:
  title: FreeRTOS 库和第三方工具
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools
next:
  title: 加入 FreeRTOS 社区
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/06-Join-the-FreeRTOS-community
---

**FreeRTOS 和 AWS 可共同为您提供简单、安全的 IoT 解决方案。**

## 引言

为简化 FreeRTOS 在物联网 (IoT) 设备上的使用，AWS 在核心开源产品中新增了一系列解决方案，
包括各种库和精选集成。

![FreeRTOS + AWS](/media/2023/FreeRTOS_Plus_AWS.png)

FreeRTOS 继续保持开源，不依赖任何云服务。您可以选择单独使用 FreeRTOS，也可以将其 
连接到 AWS IoT 平台，该平台提供了各种物联网 (IoT) 服务与解决方案，可用于连接和管理
数十亿台设备。收集、存储并分析用于工业、消费者、商业和汽车工作负载领域的 IoT 数据；
请访问 [AWS IoT](https://aws.amazon.com/iot/) 或继续阅读以了解更多信息。


## 通过简易 FreeRTOS 演示项目入门

还没有硬件？别担心，您可以参阅*通过简易 FreeRTOS 演示项目入门*部分 
（位于[构建您的首个 FreeRTOS 项目](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)下）， 
帮助您开始在 Windows 或 Linux 环境中使用免费工具 
和 FreeRTOS Windows 或 Linux 移植运行简易 blinky 演示。您还会在该部分找到使用 QEMU 中的 FreeRTOS Arm Cortex-M3 
移植运行的演示的链接。 


## 通过 Quick Connect 开始使用 AWS IoT 和 FreeRTOS

借助 Quick Connect 演示，您可以轻松设置合作伙伴提供的经 FreeRTOS 认证的开发板并将其连接到 AWS IoT，
只需几分钟即可完成。这些演示可用于非生产性应用程序，助您探索 IoT 领域。

如需了解更多信息，请参阅 [AWS Quick Connect 演示](/Why-FreeRTOS/Quick-connect)页面。
还没有硬件？[在 Windows、Linux 或 QEMU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/01-Emulation-and-simulation) 模拟环境中运行简易 blinky 演示。

## 探索 AWS IoT 库

查看[适用于 AWS IoT 的 FreeRTOS 库](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools#freertos-for-aws-iot-libraries)。
了解 IoT 设备和 AWS IoT 如何协同工作后，即可开始
探索 [FreeRTOS 库](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools) 
和[长期支持 (LTS) 库](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)了。

## 开发您的 AWS IoT 应用程序产品

请按照以下步骤为您的 AWS IoT 产品创建应用程序项目：

1. 下载最新 FreeRTOS 或长期支持 (LTS) 版本，或者
   从 [FreeRTOS-LTS](https://github.com/FreeRTOS/FreeRTOS-LTS) GitHub 存储库克隆。您还可以
   将所需的 FreeRTOS 库
   （如有，可通过 [MCU 供应商的工具链](/Community/Blogs/2021/freertos-lts-libraries-are-now-part-of-our-partner-toolchains)获取）
   集成到您的项目中。

2. 按照 [FreeRTOS 移植指南](https://docs.aws.amazon.com/freertos/latest/portingguide/porting-guide.html)
   创建项目、设置开发环境并将 FreeRTOS 库集成到项目中。
   使用 [FreeRTOS-Libraries-Integration-Tests](https://github.com/FreeRTOS/FreeRTOS-Libraries-Integration-Tests)
   GitHub 存储库来验证移植。
