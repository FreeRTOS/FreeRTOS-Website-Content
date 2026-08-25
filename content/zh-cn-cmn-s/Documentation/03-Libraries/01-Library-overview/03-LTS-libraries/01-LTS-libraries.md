---
title: "FreeRTOS LTS 库"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS Long Term Support (LTS) 库的基本信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


**注意**：现在可以从 [FreeRTOS-LTS](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202406-LTS) GitHub 存储库中下载 FreeRTOS 202406.05 LTS 库。
请参阅[最新资讯](/Community/Blogs/2024/new-freertos-long-term-support-version-released)。

### 引言

FreeRTOS 长期支持 (LTS) 各版本至少在发布后的两年内
都能获得安全和关键故障修复服务（如有必要）。
这种持续的维护使您能够在整个开发和部署周期中
整合故障修复问题，不会因为升级至新的 FreeRTOS 库主版本而造成代价高昂的中断。
为保障整个 FreeRTOS 社区的利益，AWS 竭力提供长期支持。

AWS 还提供 FreeRTOS 延长维护计划 (EMP)，
为您所选择的 FreeRTOS LTS 版本提供长达 10 年的安全补丁和关键故障修复服务。请访问
AWS 网站上的 [EMP 页面](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan)了解详细信息。

FreeRTOS LTS 库也可从我们合作伙伴的工具链中获得。
请参阅[博客文章](/Community/Blogs/2021/freertos-lts-libraries-are-now-part-of-our-partner-toolchains)。


**注意：**您可以在[主 FreeRTOS 下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)文件中找到此捆绑包中包含的库的示例项目。详情请参阅[常见问题](/Why-FreeRTOS/FAQs/Long-term-support)。

[下载 LTS 202406 库](https://github.com/FreeRTOS/FreeRTOS-LTS/releases/download/202406.05-LTS/FreeRTOSv202406.05-LTS.zip)

下载以前的版本：
[LTS 202210 库](https://github.com/FreeRTOS/FreeRTOS-LTS/releases/download/202210.01-LTS/FreeRTOSv202210.01-LTS.zip)


### 从以前的版本升级到 FreeRTOS LTS 的 202406.xx 版本

请参阅 FreeRTOS-LTS 库中的[升级至 FreeRTOS202406-LTS](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202406-LTS?tab=readme-ov-file#upgrading-to-freertos-202406-lts-from-a-previous-version-of-freertos-lts) 部分，了解如何升级以前的版本。


### LTS 状态

下表列出了 FreeRTOS 202406 LTS 版包含的库。除内核
和 TCP 堆栈仍符合其最初的质量要求外，其他均符合 LTS 模块化和[代码质量检查清单](#lts-代码质量检查表)
的要求。


**最后更新日期：2025 年 10 月 22 日**

| 库 | 版本 | 维护到期时间 |
| --- | --- | --- |
| [FreeRTOS 内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) | 11.1.0 | 2026 年 6 月 30 日 |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) | 4.2.5 | 2026 年 6 月 30 日 |
| [coreMQTT](/Documentation/03-Libraries/02-FreeRTOS-core/02-coreMQTT/00-coreMQTT) | 2.3.1 | 2026 年 6 月 30 日 |
| [coreHTTP](/Documentation/03-Libraries/02-FreeRTOS-core/04-coreHTTP/01-coreHTTP) | 3.1.1 | 2026 年 6 月 30 日 |
| [corePKCS11](/Documentation/03-Libraries/02-FreeRTOS-core/08-corePKCS11/01-corePKCS11) | 3.6.3 | 2026 年 6 月 30 日 |
| [coreJSON](/Documentation/03-Libraries/02-FreeRTOS-core/07-coreJSON/01-coreJSON) | 3.3.0 | 2026 年 6 月 30 日 |
| [coreSNTP](/Documentation/03-Libraries/02-FreeRTOS-core/05-coreSNTP/01-coreSNTP) | 1.3.1 | 2026 年 6 月 30 日 |
| [FreeRTOS-Cellular-Interface](/Documentation/03-Libraries/02-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) | 1.4.0 | 2026 年 6 月 30 日 |
| [backoffAlgorithm](/Documentation/03-Libraries/03-FreeRTOS-plus/05-backoff-algorithm) | 1.4.1 | 2026 年 6 月 30 日 |
| [AWS IoT SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4) | 1.3.0 | 2026 年 6 月 30 日 |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | 1.4.1 | 2026 年 6 月 30 日 |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | 1.4.0 | 2026 年 6 月 30 日 |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) | 1.5.1 | 2026 年 6 月 30 日 |
| [AWS IoT Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) | 1.2.1 | 2026 年 6 月 30 日 |
| [AWS IoT MQTT 文件流](/Documentation/03-Libraries/02-FreeRTOS-core/10-coreMQTT-Streams/01-coreMQTT-Streams) | 1.1.0 | 2026 年 6 月 30 日 |


关于之前 LTS 版本的库版本信息，请参阅
GitHub 上的 [FreeRTOS 202210.xx-LTS 存储库](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202210-LTS)。


### FreeRTOS LTS 补丁

想要了解最新信息，请通过观看
[FreeRTOS LTS 存储库](https://github.com/FreeRTOS/FreeRTOS-LTS) 订阅 Github 通知。


| 补丁版本 | 更新 | 帖子 |
| --- | --- | --- |
| 202406.04 LTS | 包括 FreeRTOS-Plus-TCP (V4.2.5) 的修复。| [更新日志](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.04-LTS/CHANGELOG.md) |
| 202406.03 LTS | 包括 FreeRTOS-Plus-TCP (V4.2.4) 的修复。| [更新日志](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.03-LTS/CHANGELOG.md) |
| 202406.02 LTS | 包括 corePKCS11 (v3.6.3) 和 FreeRTOS-Plus-TCP (V4.2.3) 的修复。| [更新日志](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.02-LTS/CHANGELOG.md) |
| 202406.01 LTS | 包括 coreMQTT (v2.3.1) 和 FreeRTOS-Plus-TCP (V4.2.2) 的修复。| [更新日志](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.01-LTS/CHANGELOG.md) |
| 202210.01 LTS | 包括 coreMQTT (V2.1.1) 和 FreeRTOS 内核 (V10.5.1) 的关键修复。 | [更新日志](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202210.01-LTS/CHANGELOG.md) |
| 202012.05 LTS | 包括 FreeRTOS 内核 (10.4.3-LTS-Patch-3) 的关键修复。 | [版本说明](https://github.com/FreeRTOS/FreeRTOS-Kernel/releases/tag/V10.4.3-LTS-Patch-3) |
| 202012.05 LTS | 包括 FreeRTOS 内核 (10.4.3-LTS-Patch-3) 的安全补丁。 | [安全更新](/Security/03-Vulnerabilities) |
| 202012.04 LTS | 包括 FreeRTOS-Plus-TCP 库 (2.3.2-LTS-Patch-2) 的关键故障修复。 | [版本说明](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V2.3.2-LTS-Patch-2) |
| 202012.03 LTS | 包括 FreeRTOS 内核 (10.4.3-LTS-Patch-2) 的安全补丁。 | [安全更新](/Security/03-Vulnerabilities) |
| 202012.02 LTS | 包括 FreeRTOS 内核 (10.4.3-LTS-Patch-1) 和 TCP 库 (V2.3.2-LTS-Patch-1) 的安全补丁。 | [安全更新](/Security/03-Vulnerabilities) |
| 202012.01 LTS | AWS IoT OTA、AWS Device Defender 和 AWS IoT Jobs 库被添加至 LTS 202012.00 版 | [博客文章](/Community/Blogs/2021/freertos-long-term-support-now-includes-aws-iot-over-the-air-update-aws-iot-device-defender-and-aws-iot-jobs-libraries) |


### LTS 代码质量检查表

下表记录了 LTS 版本的代码质量要求。


| # | 类别 | 检查事项 |
| --- | --- | --- |
| 1 | 复杂性评分 | 函数的 [GNU 复杂性](https://www.gnu.org/software/complexity/manual/complexity.html)得分应小于 8。 |
| 2 | 编码标准 | 函数应符合 [MISRA 2012 编码标准](/Documentation/02-Kernel/05-Coding-guidelines/02-FreeRTOS-Coding-Standard-and-Style-Guide/#coding-standard--misra-compliance)。 |
| 3 | 静态检查 | 函数应通过 [Coverity](https://scan.coverity.com/) 静态检查。 |
| 4 | APSEC 审查和渗透性测试 | 库必须通过 AWS 安全审查。 |
| 5 | 代码测试，包括内存安全性证明 | 所有代码都应经过广泛的单元测试和函数测试，并附有有关测试覆盖范围<br/> 和 CBMC 内存安全性证明的详细信息的 Gcov 报告。 |
| 6 | 要求文档 | 各个库的要求都应文档化，这些要求可能包括资源、依赖性和移植方面的要求（如适用）。 |
| 7 | 设计文档 | 各个库都应具有设计文档，包括应用程序、云接口、状态机和同步（如适用）等方面的设计文档。 |
| 8 | 编译器警告 | 代码应通过 GCC，使用 -Wall 和 -Wextra 命令行选项，且不生成编译器警告的情况下进行编译。 |
