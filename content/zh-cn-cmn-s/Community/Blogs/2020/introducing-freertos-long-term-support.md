---
title: 推出 FreeRTOS Long Term Support
created: 2020-12-14 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2020 年 12 月 14 日发布

过去几年里，我们一直在与嵌入式开发合作伙伴和客户合作， 
加快我们交付 FreeRTOS 内核和库等功能更新的步伐。与此同时， 
我们也认识到，即便快速迭代、增设新功能，有时也很难满足嵌入式 
开发人员对功能稳定性的需求：开发人员希望不再需要操心不会影响已有 
项目或设备的更改。对于已有项目或设备而言，开发人员仅需要关键故障修复和安全 
补丁，而且希望通过最简单的方法识别这些修复和补丁，并将其整合入代码中。 

今天，我们很高兴发布 FreeRTOS 的第一个长期支持 (LTS) 版本：202012.00 LTS。 
借助这个版本，开发人员在发布日期起的两年里可以使用的 FreeRTOS 版本能够保障功能稳定性， 
并提供安全补丁和关键故障修复。这有助于更方便地识别并 
整合更改，不会带来因引入更新而导致现有应用程序崩溃的风险。 
下图显示了 FreeRTOS LTS 版本的运行模式，并将其与主线分支中的开发 
加以对比。您将注意到，故障修复和安全补丁会定期 
发布。这些更改将不会引入任何新功能，不会更改不需要故障修复的 
现有功能，也不会解决新发现的安全漏洞。


## 亮点

以下是 FreeRTOS LTS 版本演进将具备的一些亮点：

* FreeRTOS LTS 库功能稳定，不会添加新功能或更改。两年里， 
  新版本将仅提供安全补丁和关键故障修复。

* FreeRTOS LTS版本使用基于日期的版本控制 (YYYYMM) ，后跟补丁序列号 (.XX)。 
  基于日期的版本控制将有助于识别特定的 FreeRTOS LTS 版本和补丁。例如， 
  包含第二个补丁的 2020 年 12 月 LTS 版本将被标识为 FreeRTOS 202012.02 
  LTS。各个库继续使用[语义版本控制](https://semver.org/)。

* 新的 FreeRTOS LTS 版本预计每 18 个月发布一次。我们将权衡  
  FreeRTOS 社区对新功能更新和功能稳定性的期望，并根据反馈 
  加快或减缓发布节奏。

* FreeRTOS 主线库将继续滚动发布，提供最新功能和更新。

* 使用 FreeRTOS LTS 库和补丁无需支付任何费用。

* FreeRTOS LTS 库和补丁将在 MIT 开源许可证下继续可用。


![FreeRTOS LTS 操作模型（补丁版本为示例）](/media/2020/LTS-Operating-Model.png)   
*FreeRTOS LTS 操作模型（补丁版本为示例）*

首个 FreeRTOS [LTS 版本](../../lts-libraries)为FreeRTOS 202012.00，其中包括 FreeRTOS 
内核和 IoT 库：FreeRTOS-Plus-TCP、coreMQTT、coreHTTP、corePKCS11、coreJSON 和 AWS IoT 
 Device Shadow。这些库将至少维持到 2022 年 12 月 31 日。 


## FreeRTOS 安全性和内存使用的改进

安全性是我们 AWS 的第一要务，这同样适用于 FreeRTOS 开发。为了进一步改进  
FreeRTOS 及其库的安全性，我们一直与 
 AWS 的[自动推理小组](https://aws.amazon.com/security/provable-security/)合作，将 
基于数学且可证明的安全技术运用于 FreeRTOS。LTS 版本中的 FreeRTOS 库 
已通过 C 边界模型检查器 ([CBMC](https://www.cprover.org/cbmc/)) 自动推理工具 
验证内存安全性，以缓解缓冲区溢出等代码安全问题。参阅博客“确保 
 FreeRTOS 的内存安全”（[第 1 部分](../02/ensuring-the-memory-safety-of-freertos-part-1)、[第 2 部分](../05/ensuring-the-memory-safety-of-freertos-part-2)）， 
了解更多信息。

LTS 版本中的 FreeRTOS 库已针对内存使用进行了优化，并具备更强模块性。 
这些库对标准 C 库以外的任何其他库没有依赖性，从而提高了 
设计灵活性。这些库也经过许多代码质量检查， 
包括 [MISRA-C](https://www.misra.org.uk/MISRAHome/MISRAC2012/tabid/196/Default.aspx) 合规性检查 
和 [Coverity](https://scan.coverity.com/) 静态分析，以确保嵌入式系统中代码的安全性、可移植性和可靠性 
（请参阅 [LTS 代码质量检查清单](../../lts-libraries#checklist)）。 

这些安全性、内存使用和代码质量属性在 FreeRTOS 库、主线 
或 LTS 分支中都很常见，使其在资源受限的设备中更容易使用。


## 新的 Github 存储库结构

每个 LTS 库现在都自带[ GitHub 存储库](https://github.com/FreeRTOS/FreeRTOS)。这 
让开发人员可以更轻松地在其 FreeRTOS 项目中集成并更新库。开发人员 
现在可以从 FreeRTOS 存储库中将各个库 
作为 [Git 子模块](https://git-scm.com/book/en/v2/Git-Tools-Submodules)（“Git 存储库内的 Git 存储库”）集成， 
无需合并剩余其他库。开发人员还可以通过更新子模块指针 
来更新其项目中的库，无需复制或移动库。


## 入门指南

想要开始使用，请从 [FreeRTOS.org 下载 FreeRTOS 202012.00](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) LTS 源代码。或者， 
通过对各个 LTS 库或整个 
 FreeRTOS 202012.00 LTS 存储库进行子模式化，从而将 LTS 库集成到您的项目中。如果您希望将自己的设备连接至 AWS IoT 并使用 
 AWS IoT Device Shadow 等功能，请访问 AWS IoT 参考集成[页面](../../aws-reference-integrations)， 
然后选择并下载标记为使用 LTS 库的 IoT 参考集成。 


## FreeRTOS LTS 响应

我们对新 LTS 版本获得的反响感到兴奋，这个版本是我们基于 FreeRTOS 合作伙伴、 
客户和嵌入式开发人员社区的反馈而构建的。我们获得一些来自 FreeRTOS 社区的 
早期反馈，可能有助于您决定采用 LTS 版本。以下是我们迄今为止收到的反馈…… 

* “随着 LTS 的发布，开发人员现在可以采用稳定的接口，并且使用 CMSIS-Pack 管理 
  系统简化产品生命周期管理。”—— *Arm 嵌入式工具高级总监 Reinhard Keil*

* “我们对 FreeRTOS Long Term Support 的发布感到很高兴，因为我们的客户将 
  受益于长期支持版本提供的稳定性和安全性更新。”——*Espressif 
  创始人兼首席执行官 Teo Swee Ann*。

* “我们很高兴看到 AWS 发布 FreeRTOS LTS 以进一步加强商业市场中的 FreeRTOS， 
  并满足我们共同客户的需求。”——*IAR Systems 嵌入式工具总经理 Anders Holmsberg*

* “FreeRTOS LTS 库与长期的半导体支持相结合，可为我们的客户提供 
  他们为 IoT 产品选择解决方案时所需的稳定性和寿命保证。”——*Infineon IoT 计算与无线事业部软件与生态系统副总裁
   Rob Conant*

* “集成 FreeRTOS LTS 库进一步扩大了我们对 MCU 客户的承诺。这些客户开发 
  连接至 AWS 云服务且需要能够使用关键软件更新的安全 
  边缘设备。”——*NXP Semiconductors IoT 生产线副总裁兼总经理 Joe Yu*

* “FreeRTOS LTS 版本发布后，相信我们的客户可以从更高的质量和可靠性中 
  受益，快速解决安全漏洞，能有更多精力 
  为开发增值。”——*Renesas IoT 平台事业部副总裁 Daryl Khoo*

* “FreeRTOS LTS 版本及其在 STM32Cube 软件包中的集成确保了 
  长期稳定性和保障性维护, 让我们的客户在构建其 
   AWS 连接解决方案时能专注于质量与增值。”——*
  STMicroelectronics 微控制器生态系统市场经理 Laurent Desseignes。*

我们很期待看到 FreeRTOS LTS 版本如何改进下一代嵌入式应用程序的 
开发和维护。我们期待您的反馈。如有任何意见或要求，您可以访问 
[FreeRTOS 论坛](https://forums.freertos.org/)联系我们！


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 


FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

