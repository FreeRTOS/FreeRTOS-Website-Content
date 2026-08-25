---
title: FreeRTOS 常见问题 - GitHub 存储库结构 & 版本控制
created: 2018-09-20 00:00:00.0 UTC
description: 有关 FreeRTOS GitHub 存储库结构和版本控制的常见问题
---

## FreeRTOS Git 存储库是如何构建的？

共有两种类型的存储库：**单库**存储库和**软件包存储库**。
所有单库存储库均包含库的源代码，不含任何构建项目或
示例。软件包存储库包含多个库，并且可能包含
用于演示库使用方法的预配置项目。

虽然软件包存储库包含多个库，但不包含这些库的副本，
而是以
[git 子模块](https://git-scm.com/book/en/v2/Git-Tools-Submodules)的形式引用所含的库。使用子模块可确保
每个库都有唯一的事实来源。

单个库的 git 存储库在两个 GitHub 组织间拆分。含有
FreeRTOS 特定库（如 FreeRTOS-Plus-TCP）或通用库（如 coreMQTT 一类的
跨云库，因其适用于任何 MQTT代理）位于 [FreeRTOS GitHub 组织中](https://www.github.com/FreeRTOS)。
包含 AWS IoT 特定库的存储库（如 AWS IoT over-the-air
更新客户端）则位于 [AWS GitHub 组织](https://github.com/AWS)中。

下图为该结构体的演示。

[\![](/media/2021/gsv-faq-image1.png)](/media/2021/gsv-faq-image1.png)
* GitHub 存储库结构 - 点击放大*


## FreeRTOS 库是如何进行版本控制的？

[单个库](#freertos-git-存储库是如何构建的)使用 *x.y.z* 样式版本号，类似于
[语义版本控制](https://semver.org/)。 *x* 为主要版本号，*y* 为次要版本号，
（自 2022 年起）*z* 为补丁号。在 2022 年之前，*z* 曾经是单点发行编号，这也意味着
第一个 [LTS 库](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries)的补丁需要一个单独的
*"x.y.z LTS Patch 2*" 形式的补丁号。

在 FreeRTOS 库的 LTS 版本中，LTS 补丁的 *x.y.z* 将保留 *z*。例如，
如果 *3.1.0* 是 FreeRTOS 库的 LTS 版本，则 *3.1.1*将是 LTS 版本的补丁。这
意味着来自 *3.1.z* 版本中 FreeRTOS 库的非 LTS 单点发行版本
必须递*增次*要版本（即 *y*）号，而非 *z* 编号。因此，LTS 版本的补丁
可以扩展。

仅 LTS 版本的库可保留 *z*。非 LTS 版本的库单点发布时
将递增 z。例如，在主线的后续版本中，
FreeRTOS 库的未来版本，例如 *3.3.0*，可以以 *3.3.1* 的编号进行单点发布，而 *3.1.0* 则继续作为
LTS 版本。

[库包](#freertos-git-存储库是如何构建的)使用 *yyyymm.x* 样式日期戳版本号。*yyyy* 是年份，
*mm* 是发布月份，*x* 是顺序补丁号。包中包含的单个库
是在该日期的最新版本的库
（或者如果是 LTS 包，则是当天最初发布为 LTS 版本的
LTS 库的最新补丁版）。


## 可以使用哪些库包？

一共有四种库包。

1. 主要 FreeRTOS 分发包（来自于 FreeRTOS GitHub 组织）：

   此包内含大量预配置项目，可演示在不同处理器上运行的 FreeRTOS 内核，
   并使用不同的编译器和项目来演示其他 FreeRTOS 库（例如
   FreeRTOS-Plus-TCP），这些库在模拟环境中运行。

1. 精选 FreeRTOS IoT 参考集成（来自 FreeRTOS GitHub 组织） ：

   [精选 FreeRTOS IoT 集成](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)
   是预配置的项目，展示了提升 IoT 设备软件安全性和稳健性的最佳实践
   。这些 FreeRTOS IoT 集成旨在通过使用 FreeRTOS 软件和
   合作伙伴提供的具有硬件安全功能的开发板来提高安全性。

1. 设备的 AWS IoT 嵌入式 C SDK（来自 AWS GitHub 组织） ：

   此包内含大量预配置项目，可演示在 POSIX 操作系统上运行的 FreeRTOS 和 AWS 的集成，
   而非在 FreeRTOS 上运行。

1. FreeRTOS 库的 LTS 版本（来自 FreeRTOS GitHub 组织）：

   此包仅供参考和便利用途。其仅含
   [FreeRTOS 库的长期支持 (LTS) 版本](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries)，不含示例项目。


## 如何获取并使用各个 FreeRTOS 库?

使用应用程序中的单个库的推荐方法是，
直接从 GitHub 将它们子模块化至应用程序。或者，您可以通过下载来自 GitHub 存储库 Releases 区域的 zip 文件，
将单个库复制到您的应用程序中。下表
含有指向单个库的链接。包的下载中含有示例。

| 库 | 将单个库复制到您的应用程序中。 |
| ------- | --------------------------------- |
| [FreeRTOS 内核](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)（RTOS 内核）  | https://github.com/FreeRTOS/FreeRTOS-Kernel |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)（TCP/IP 堆栈）  | https://github.com/FreeRTOS/FreeRTOS-Plus-TCP |
| [coreMQTT-Agent](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)（多线程 MQTT 客户端）  | https://github.com/FreeRTOS/coreMQTT-Agent（包括 coreMQTT） |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)（基础 MQTT 客户端）  | https://github.com/FreeRTOS/coreMQTT |
| [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)（HTTP 客户端）  | https://github.com/FreeRTOS/coreHTTP |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)（PKCS#11 软件模拟）  | https://github.com/FreeRTOS/corePKCS11 |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) (JSON)  | https://github.com/FreeRTOS/coreJSON |
| [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP) (SNTP)  | https://github.com/FreeRTOS/coreSNTP |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | https://github.com/aws/device-shadow-for-aws-iot-embedded-sdk |
| [AWS IoT OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) | https://github.com/aws/ota-for-aws-iot-embedded-sdk |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) | https://github.com/aws/jobs-for-aws-iot-embedded-sdk |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | https://github.com/aws/device-defender-for-aws-iot-embedded-sdk |



## 如何获取 FreeRTOS 分发包?

以下是对各个包的说明。请注意，如果使用 git 获取库包，
则需另外遵循包中的自述文件中的存储库克隆说明，
以确保一并进行了子模块引用的初始化和同步：

1. 主要 FreeRTOS 分发包:

   大部分人会使用[ FreeRTOS.org 网站上的下载按钮](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)
   以获取 zip 文件。该分发包也可在 GitHub 上作为
   [git 存储库](https://github.com/FreeRTOS/FreeRTOS)
   或 [zip 文件](https://github.com/FreeRTOS/FreeRTOS/releases) 获取。

1. 精选 FreeRTOS IoT 集成：

   每个精选集成位于 FreeRTOS github 组织下的
   一个单独存储库（命名格式为：iot-reference-targetplatform）中。从
   [精选 FreeRTOS IoT 集成页面](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)中查看最新项目的列表。

1. AWS IoT 用于设备的嵌入式 C SDK：

   此软件包可从 GitHub 作为 [git 存储库](https://github.com/aws/aws-iot-device-sdk-embedded-C)
   或 [zip 文件](https://github.com/aws/aws-iot-device-sdk-embedded-C/releases) 获取。

1. FreeRTOS 库的 LTS 版本：

   类似于主要 FreeRTOS 分发包，大部分人会用
   [FreeRTOS.org 网站](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)上的下载按钮获取 zip
   文件。此软件包可从 GitHub 作为 [git 存储库](https://github.com/FreeRTOS/FreeRTOS-LTS)
   或 [zip 文件](https://github.com/FreeRTOS/FreeRTOS-LTS/releases) 获取。
