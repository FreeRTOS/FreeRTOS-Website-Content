---
title: 2021 年 12 月 FreeRTOS 版本新特性介绍
created: 2021-12-21 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 12 月 21 日发布

我们很高兴向大家介绍以下最新更新： 

* FreeRTOS 现推出一个 [MCUBoot 演示项目](/Documentation/03-Libraries/05-FreeRTOS-labs/05-FreeRTOS-MCUBoot)， 
基于 FreeRTOS 运行的应用程序的安全引导加载程序可以此为参考。[MCUBoot](https://github.com/mcu-tools/mcuboot) 
是适用于 32 位微控制器的可配置安全引导加载程序。它可作为 
第一或第二阶段的引导加载程序运行，支持软件映像的加密验证。
  
* 此外，FreeRTOS 下载包现包括 AWS 第 4 版签名 (SigV4) 库以及 
   IoT 应用程序的 AWS IoT Fleet Provisioning 客户端库。 

  SigV4 是对 AWS 服务请求进行身份验证的过程，验证方法是向 
   HTTP 请求添加身份验证消息。SigV4 库提供了一个可生成签名和授权标头的接口， 
  此接口符合 [SigV4 签名过程](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)。 
  SigV4 库还帮助验证发送 HTTP 请求到 AWS 服务（例如 Amazon S3）的 IoT 设备。 

  Fleet Provisioning 库允许利用 Fleet Provisioning 预置 IoT 设备， 
  [用于 AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html)。 
  在此功能中，[AWS IoT](https://aws.amazon.com/iot-core/)   生成并安全传递设备 
  证书和私钥至首次连接至 AWS 的设备。

  SigV4 和 Fleet Provisioning 库已针对内存使用和模块性加以优化，而且 
  经过代码安全检查（例如 [MISRA-C 合规检查](https://www.misra.org.uk/misra-c/)、[Coverity 静态分析](https://scan.coverity.com/)）。 
  如需了解更多内容并开始入门，请访问 [SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4)  
  和 [Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) 网页或 GitHub  
  存储库（[SigV4](https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk)、[Fleet Provisioning](https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk)）。

* 最后要提到的是，作为在您使用硬件之前评估 FreeRTOS 的一个方法，我们添加了 
  一个 [FreeRTOS 内核演示](../../freertos-on-qemu-mps2-an385-model)，它针对的是 Arm 
  Cortex-M3 [mps2-an385  QEMU](https://qemu.readthedocs.io/en/latest/system/arm/mps2.html) 模型。 
  此外还提供了预配置构建项目，用于  
  [IAR Embedded Workbench](https://www.iar.com/products/architectures/arm/iar-embedded-workbench-for-arm/) 
  和 [arm-none-eabi-gcc](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)  
  (GNU GCC) 工具链（位于 FreeRTOS 下载包）。

我们期待您的持续反馈。如果您有任何意见或要求，请访问 [FreeRTOS 论坛](https://forums.freertos.org/)！ 


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

