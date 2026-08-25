---
title: 安全概述
date: 2022 年 1 月
---

FreeRTOS 遵循严格的编码标准，并且经过了多项
代码质量检查，包括 [MISRA-C](https://www.misra.org.uk/publications/) 合规性 
和 [Coverity](https://scan.coverity.com/) 静态分析，以确保
嵌入式系统中代码的安全性、可移植性和可靠性（请参阅
[LTS 代码质量检查清单](/lts-libraries.html#checklist) 中的列表）。
FreeRTOS 库的重大更新必须通过 AWS 应用程序
安全性 (AppSec) 审核和 AWS 渗透测试 (pentest) 审核，
方可发布。


### 内存安全

FreeRTOS 专为资源受限的设备设计，
不同于功能更丰富的操作系统，这些设备无法提供各种硬件机制
来保护系统免受外部攻击。此类小型设备的安全性
取决于是否有更简单的内存保护、具有执行特权级的硬件
以及操作系统代码本身。我们与
[自动推理小组](https://aws.amazon.com/security/provable-security/) 
（隶属于 AWS）合作，将基于数学且可证明的安全技术应用于 FreeRTOS。
FreeRTOS 库已通过 C 边界模型检查器
([CBMC](https://www.cprover.org/cbmc/)) 自动推理工具进行内存安全验证，
可缓解缓冲区溢出等代码安全问题。

要了解更多信息，请阅读博客“确保 
FreeRTOS 的内存安全”（[第 1 部分](/2020/02/ensuring-the-memory-safety-of-freertos-part-1.html)、[第 2 部分](/2020/05/ensuring-the-memory-safety-of-freertos-part-2.html)）。


### 威胁模型

请参阅本网站上的 [FreeRTOS 内核威胁模型](/security/kernel-threat-model.html) 页面。


### 安全认证

FreeRTOS 提供的基础连接库（例如 
[FreeRTOS-Plus-TCP](/FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.html) 
和 [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)）可帮助开发者自信安全地
将 IoT 设备连接到云端。FreeRTOS
已通过 
[IoT 平台安全评估标准 (SESIP™)](https://trustcb.com/iot/sesip/) 
2 级和 PSA 1 级认证，证明了其安全性和可靠性。SESIP™ 的基本宗旨源于
业界通行的[共同标准](https://en.wikipedia.org/wiki/Common_Criteria) 
框架。[PSA 认证](https://www.psacertified.org/) 提供了一个
保护互联设备安全的框架，涵盖从分析到安全评估
再到认证的整个过程。

了解更多 >> [SESIP 2 级](/2021/03/why-sesip-certification-for-freertos-matters.html)、[PSA 1 级](/2021/07/secure-ota-updates-for-cortex-m-devices-with-freertos.html)。


