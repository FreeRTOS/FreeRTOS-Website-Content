---
title: "'Officially Supported'（官方支持） 和 'Contributed'（贡献）的 FreeRTOS 代码"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

每个架构**和**编译器组合会被视作是单独的 FreeRTOS 移植。 
FreeRTOS 移植的微控制器架构特定部分称为移植层。 
由于创建和维护移植的人员差异，FreeRTOS 移植被分成多种类型：

1. 官方支持的移植——这些移植由 FreeRTOS 团队创建并直接提供支持。

2. 合作伙伴创建但 FreeRTOS 团队提供支持的移植。

3. 合作伙伴创建并提供支持的移植。

4. 社区支持的移植。

虽然不同类别的移植位于不同的 Git 存储库中（如下所述），但全部以子模块形式存储到 
主 [FreeRTOSGit 存储库](https://github.com/FreeRTOS/FreeRTOS)中并且包含在 
[官方 zip 文件中进行发布](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)。


## 官方支持的移植

官方支持的移植：

* 直接挂载于 [FreeRTOS 内核的 Git 存储库](https://github.com/FreeRTOS/FreeRTOS-Kernel)中。

* 包括至少一个[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)，且被收录于 FreeRTOS.org 网站上。

* 来源已知，消除对知识产权归属的疑虑。这反过来又允许 
  我们的合作伙伴 WITTENSTEIN high integrity systems（可选择）提供商业许可和支持合同，且是在 
  OpenRTOS 的名义下进行的。

* 已由 Amazon Web Services Inc. 进行编写及/或全面检查和测试。

* 一般而言，且绝大多数情况下，被作为 FreeRTOS 新版本的核心代码进行维护和更新，或者 
  会发布新版的相关 build 工具。

* 通常可以在免费访问的有人监管的
  [支持论坛](https://forums.freertos.org/)上获取支持。

* 可被包含在长期支持 (LTS) 版本中。


## 第三方贡献的移植

贡献的移植：

* 由 FreeRTOS 合作伙伴创建，而不是由 Amazon Web Services 直接创建。

* 在 Github 中免费提供。

* 只能在标准开源 FreeRTOS 许可下提供。第三方贡献的代码 
  无商业许可。

* 由创建者自己编写文档因此，不同的第三方数据包 
  所提供文档的数量和质量参差不齐。

第三方移植可以分为如下三种子类。

**1：受 FreeRTOS 团队支持的第三方贡献移植**

位置：[https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/ThirdParty](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/ThirdParty)

这些第三方 FreeRTOS 移植由 FreeRTOS 团队提供支持。对于
FreeRTOS 团队支持的第三方 FreeRTOS 移植具有以下特点：

* 代码已由 FreeRTOS 团队审核。

* FreeRTOS 团队可以接触到硬件，且测试结果已经
  由 FreeRTOS 团队验证。

* FreeRTOS 团队会处理客户的提问和 bug。

* 代码可被包含在长期支持 (LTS) 版本中。

新的 FreeRTOS 移植不会被直接收入此处。相反，
FreeRTOS 团队将会根据社区的需要决定是否接管合作伙伴支持的或是
社区支持的 FreeRTOS 移植。


**2：合作伙伴支持的 FreeRTOS 移植**

位置: [https://github.com/FreeRTOS/FreeRTOS-Kernel-Partner-Supported-Ports/tree/main](https://github.com/FreeRTOS/FreeRTOS-Kernel-Partner-Supported-Ports/tree/main)

这些 FreeRTOS 移植由 FreeRTOS 合作伙伴支持。合作伙伴
支持的 FreeRTOS 移植具有以下特点：

* 代码未由 FreeRTOS 团队审核。

* FreeRTOS 团队未核验测试结果，但已进行测试
  且合作伙伴报告测试成功。

* 客户的提问和 bug 也由合作伙伴处理。

新的 FreeRTOS 移植可以直接由合作伙伴完成。贡献 FreeRTOS 移植的流程 
[请参阅 Github](https://github.com/FreeRTOS/FreeRTOS-Kernel-Partner-Supported-Ports/blob/main/README.md)。


**3：社区支持的 FreeRTOS 移植**

位置: [https://github.com/FreeRTOS/FreeRTOS-Kernel-Community-Supported-Ports/tree/main](https://github.com/FreeRTOS/FreeRTOS-Kernel-Community-Supported-Ports/tree/main)。

这些 FreeRTOS 移植由 FreeRTOS 社区成员支持。社区
支持的 FreeRTOS 移植具有以下特点：

* 代码未由 FreeRTOS 团队审核。
* FreeRTOS 移植的测试可能存在，也可能不存在。
* 客户的提问和 bug 也由合作伙伴处理。

任何人都可以直接贡献新的 FreeRTOS 移植。贡献 FreeRTOS 移植的流程 
[请参阅 Github](https://github.com/FreeRTOS/FreeRTOS-Kernel-Community-Supported-Ports/blob/main/README.md)。

