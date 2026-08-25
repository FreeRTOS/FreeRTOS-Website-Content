---
title: 新的 FreeRTOS Long Term Support 版本现已发布
date: 2022 年 10 月 14 日
feature: blog
categories:
- 长期支持
authors:
- stanmoy
---
我们推出 FreeRTOS Long Term Support (LTS) 已经 18 个月了。有了 FreeRTOS LTS， 
开发人员可以放心使用 FreeRTOS 版本，该版本自发布之日起两年内提供稳定的功能、安全补丁和 
关键漏洞修复服务。我们发布了 
[第一个 LTS 版本（FreeRTOS 202012 LTS）](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202012-LTS)， 
其中包含安全 AWS IoT 连接和 OTA 升级所需的所有库。此外， 
每个 FreeRTOS 库的设计都是模块化的，都有自己的资源库， 
对第一个 LTS 版本的其他库的依赖性最低。这使我们的合作伙伴 
[能够将 FreeRTOS 库集成到他们的工具链中](/Community/Blogs/2021/freertos-lts-libraries-are-now-part-of-our-partner-toolchains)， 
从而使客户更容易构建、更新和验证基于 FreeRTOS 的项目。

今天，我们很高兴地宣布推出 FreeRTOS Long Term Support (LTS) - FreeRTOS 
202210.00 LTS 的第二版。此版本包括新的库，如 AWSIoT Fleet Provisioning 和蜂窝 
LTE-M 接口，可简化设备配置和蜂窝连接。它还包括 coreMQTT 
和 FreeRTOS-Plus-TCP 库，具有更好的模块性和连接稳健性。所有库 
该 FreeRTOS LTS 版本中包含的所有库（如下表所示） 
将在 2024 年 10 月前收到安全和关键漏洞修复。有了 LTS 版本，您可以继续维护您现有的 FreeRTOS 
代码库，避免 FreeRTOS 版本升级可能造成的任何中断。

| 库 | LTS 202012 | LTS 202210 | 与以前 LTS 版本相比的变化 |
| --- | --- | --- | --- |
| [FreeRTOS 内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) | 10.4.3 | 10.5.0 | 没有 API 变化。 |
| [FreeRTOS-Plus-TCP](../../FreeRTOS-Plus/FreeRTOS_Plus_TCP/index) | 2.3.2 | 3.1.0 | 没有 API 变化。由于文件和文件夹结构的改进，现有的项目构建将受到影响。 |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) | 1.1.0 | 2.1.0 | API 变化。 |
| [coreHTTP](../../http/index) | 2.0.0 | 3.0.0 | 没有 API 变化。HTTP 解析器更新。 |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) | 3.0.0 | 3.5.0 | 没有 API 变化。 |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) | 3.0.0 | 3.2.0 | 没有 API 变化。 |
| [backoffAlgorithm](../../backoff-algorithm) | 1.0.0 | 1.3.0 | 没有 API 变化。 |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | 1.0.2 | 1.3.0 | 没有 API 变化。 |
| [AWS IoT OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) | 3.0.0 | 3.4.0 | 没有 API 变化。 |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) | 1.1.0 | 1.3.0 | 没有 API 变化。 |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | 1.1.0 | 1.3.0 | 没有 API 变化。 |
| [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP) |  | 1.2.0 | 新增。 |
| [AWS IoT SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4) |  | 1.2.0 | 新增。 |
| [蜂窝 LTE-M 接口](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) |  | 1.3.0 | 新增。 |
| [AWS IoT Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) |  | 1.1.0 | 新增。 |


与之前的 FreeRTOS LTS 版本类似， FreeRTOS 202210.00 LTS 包含 
使用 C Bounded Model 
Checker ([CBMC](https://freertos.org/2020/02/ensuring-the-memory-safety-of-freertos-part-1.html))  
自动推理工具验证过内存安全性的库，以帮助减少缓冲区溢出等代码安全问题。此外， 
所有 LTS 库都经过了一定的代码质量检查，包括 [MISRA-C](https://www.misra.org.uk/) 
合规性和 [Coverity](https://scan.coverity.com/) 静态分析，以帮助提高代码的安全性、 
可移植性和嵌入式系统的可靠性（参见 [LTS 代码质量检查表](https://freertos.org/lts-libraries.html#checklist)）。

上一个 LTS 版本的支持期将在 2023 年 3 月结束，因此，我们为您提供了 6 个月的 LTS 版本之间的重叠期， 
便于项目迁移。请参阅[迁移指南](../../lts-libraries) 
和相应的[验证测试](https://github.com/FreeRTOS/FreeRTOS-Libraries-Integration-Tests) 
将您的项目升级到 FreeRTOS 202210.00 LTS。如果您不想升级， 
并希望在之前的 LTS 版本到期后继续接收关键修复，可以考虑使用 
[FreeRTOS延长维护计划](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan)。

要使用最新 LTS 版本[鉴定](https://aws.amazon.com/partners/programs/dqp/)您的开发板 
并将其列入（或更新） [AWS 合作伙伴设备目录](https://devices.amazonaws.com/)， 
可以使用针对 FreeRTOS[(https://aws.amazon.com/freertos/device-tester/) 202210.00 LTS 的 ]AWS IoT Device Tester。

如需了解更多信息并开始使用，请参阅 [FreeRTOS LTS 页面](https://freertos.org/lts-libraries.html) 
和 [FreeRTOS-LTS](https://github.com/FreeRTOS/FreeRTOS-LTS) LTS GitHub 存储库。

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)
