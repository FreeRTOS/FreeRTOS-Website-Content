---
title: "新的 FreeRTOS Long Term Support 版本现已发布"
date: 2024 年 7 月 3 日
feature: blog
authors:
  - luciodj
---

由 [Lucio Di Jasio](../author/luciodj) 于 2024 年 7 月 3 日发布

距前一版 FreeRTOS Long Term Support (FreeRTOS 202210 LTS) 发布又过了 18 个月。 
借助 FreeRTOS LTS，开发人员在发布日期起的两年里可以使用的 FreeRTOS 版本能够保障功能稳定性， 
安全补丁和关键故障修复服务。我们发布了 
[第一个 LTS 版本 (FreeRTOS 202012 LTS)](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202012-LTS)， 
其中包含安全 AWS IoT 连接和 OTA 升级所需的所有库。此外， 
每个 FreeRTOS 库均为模块化设计，自带资源库，极少依赖其他库 
。

今天，我们很高兴地宣布推出第三版 FreeRTOS Long Term Support (LTS)，即 FreeRTOS 202406 
LTS。此版本包括 
最新 [FreeRTOS 内核 v11.1](/Community/Blogs/2023/introducing-freertos-kernel-version-11-0-0-a-major-release-with-symmetric-multiprocessing-smp-support)
（支持对称多处理 (SMP)） 
和[内存保护单元 (MPU)](/Security/04-FreeRTOS-MPU-memory-protection-unit)。 
[FreeRTOS-Plus-TCP v4.2.1](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)
库提供改进的 IPv6 支持（具有向后兼容模式），将 IPv4 和 IPv6 文件 
完全分离，从而轻松优化您的应用程序占用空间。最后，OTA 库 
已重构，以获得最大的灵活性。详细了解 
全新[模块化 Over the Air 更新](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) 
方法和新的[文件流库](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c/tree/690fb2bd10020da916fe54f3e8c59f1e3f925e44)， 
以满足您最多样化的 OTA 需求。

此 FreeRTOS LTS 版本中包含的所有库（如下表所示）都将获得安全 
和关键故障修复，直至 2026 年 6 月。有了 LTS 版本，您可以继续维护您现有的 
FreeRTOS 代码库，避免 FreeRTOS 版本升级可能造成的任何中断。

| 库                | LTS 202406 | LTS 202210 | 与以前 LTS 版本相比的变化 |
| ---------------------- | ---------- | ---------- | ---------------------------------------- |
| [FreeRTOS 内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)        | 11.1.0     | 10.5.1     | 现包括对称多处理 (SMP) 和内存保护单元 (MPU) 支持。 |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)      | 4.2.1      | 3.1.0      | 现提供改进的 IPv6 支持和向后兼容模式。 |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)               | 2.3.0      | 2.1.1      | 没有 API 变化。 |
| [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)               | 3.1.1      | 3.0.0      | 没有 API 变化。 |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)             | 3.6.1      | 3.5.0      | 没有 API 变化。 |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)               | 3.3.0      | 3.2.0      | 没有 API 变化。 |
| [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP)               | 1.3.1      | 1.2.0      | 没有 API 变化。 |
| [FreeRTOS-Cellular-Interface](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) | 1.4.0 | 1.3.0      | 没有 API 变化。 |
| [backoffAlgorithm](/Documentation/03-Libraries/02-FreeRTOS-plus/05-backoff-algorithm)       | 1.4.1      | 1.3.0      | 没有 API 变化。 |
| [AWS IoT SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4)          | 1.3.0      | 1.2.0      | 没有 API 变化。 |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)  | 1.4.1      | 1.3.0      | 没有 API 变化。 |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | 1.4.0     | 1.3.0      | 没有 API 变化。 |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs)           | 1.5.1      | 1.3.0      | 没有 API 变化。 |
| [AWS IoT Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) | 1.2.1  | 1.1.0      | 没有 API 变化。 |
| [AWS IoT MQTT 文件流](/Documentation/03-Libraries/03-FreeRTOS-core/10-coreMQTT-Streams/01-coreMQTT-Streams) | 1.1.0   | -          | 扩展和简化以前的 OTA 库的新库。 |

与之前的 FreeRTOS LTS 版本类似， FreeRTOS 202406 LTS 包含 
已通过 C 边界模型检查器 (CBMC) 自动推理工具验证内存安全的库， 
以帮助减轻代码安全问题，如缓冲区溢出。此外，所有 LTS 库都经过了 
代码质量检查，包括 [MISRA-C](https://www.misra.org.uk/) 合规性检查 
和 [Coverity](https://scan.coverity.com/) 静态分析，以帮助提高代码在嵌入式系统中的 
安全性、可移植性和可靠性（请参阅 
[LTS 代码质量检查表](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries#lts-code-quality-checklist)）。

上一个 LTS 版本的支持期将在 2024 年 10 月结束，因此前后 LTS 版本的支持期存在重叠， 
便于项目迁移。请参阅 
[迁移指南](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)和 
相应的[验证测试](https://github.com/FreeRTOS/FreeRTOS-Libraries-Integration-Tests) 
以将您的项目升级到 FreeRTOS 202406 LTS。如果您不希望升级，并希望在以前的 LTS 版本到期后 
继续接收以前版本的关键修复，您可以考虑 
[FreeRTOS 延长维护计划](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan)。

如需了解更多信息，请参阅 [FreeRTOS LTS 页面](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries) 
和 [FreeRTOS LTS GitHub 存储库](https://github.com/FreeRTOS/FreeRTOS-LTS)。

