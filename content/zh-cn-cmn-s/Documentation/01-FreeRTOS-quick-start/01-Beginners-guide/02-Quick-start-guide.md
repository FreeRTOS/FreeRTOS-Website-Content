---
title: "FreeRTOS 内核快速入门指南"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 快速入门指南
---


本页面首先介绍如何尽快在目标设备上运行 RTOS
。下文“[后续步骤 — 延伸阅读](#延伸阅读)”部分提供了一组
链接，可帮助您加深对 FreeRTOS 的了解，获得常见问题的解答，
并且更熟练地使用 FreeRTOS。

另请参阅
[简单 FreeRTOS 项目入门](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project#getting-started-with-simple-freertos-demo-projects)文档，
为获得更出色的入门体验，也请参阅相关 [FreeRTOS 书籍](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)。我们还提供了 FreeRTOS 移植
（适用于 [Windows](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW) 和 [Linux](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux)）
以及 [QEMU 项目](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model)，供您通过免费工具尝试使用 FreeRTOS，
这些工具对硬件没有任何特殊要求。


  


### 入门建议


无论您是刚接触 FreeRTOS，还是已经具有丰富的开发经验，我们始终建议您在开发新项目时，先定义 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization#configassert)，
实现 [malloc 失败钩子函数](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions#malloc-failed-hook-function)，并将 [configCHECK_FOR_STACK_OVERFLOW](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking) 设置为 2。
  



### RTOS 快速入门说明


FreeRTOS 已移植到许多不同的架构和编译器。每个 RTOS 移植
都附带预配置的[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)，可助您快速开始使用。此外，每个演示应用程序
还配有相应的文档页面，提供的信息非常全面，包括如何找到 RTOS 演示项目源代码、构建演示项目以及配置目标
硬件。

演示应用程序文档页面还提供**基本的 RTOS 移植特定信息**，包括**如何编写与 FreeRTOS 兼容的
中断服务程序**。这些内容在不同的微控制器架构上可能会略有不同。



按照以下简单说明，几分钟内即可开始运行：


1. **下载 RTOS 源代码**：

RTOS 库[可通过 Git 分别获取](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning)，但最简单的入门方式是[下载 FreeRTOS .zip 文件](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)，因为该文件中还包含针对各官方移植的演示项目。请不要被文件数量吓到，[实际上，每个演示只需要其中一小部分文件](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)！将文件解压到您认为合适的目录中。

2. **找到相关文档页面**：

在“[支持的设备](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)”页面中，查看 FreeRTOS 官方支持的微控制器供应商名单。点击微控制器供应商名称，即可跳转至针对该供应商的文档页面列表。


如果没有针对您所用开发板的预配置移植，请参阅[修改演示应用程序以在其他硬件上运行](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)页面。

3. **构建项目**：

按照 RTOS 移植文档页面上的说明，在 [FreeRTOS 目录结构](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)中找到所需的项目，然后打开并构建演示项目。

4. **运行演示应用程序**：

按照 RTOS 移植文档页面上的说明设置目标硬件、下载并执行演示应用程序。该文档页面还提供有关演示应用程序功能的信息，助您判断该应用程序是否正确执行。

5. **创建您自己的项目：**

要[创建自己的 FreeRTOS 项目](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)，最简单的方法是以您所选移植配套的演示应用程序为基础来进行构建。演示应用程序开始运行后，逐渐删除演示函数和源文件，并替换为您自己的应用程序代码。  如在排查故障时需要帮助，请参阅常见问题：“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。



### 延伸阅读


要创建自己的 FreeRTOS 项目，最简单的方法是以您所选移植配套的演示应用程序为基础来进行构建。演示应用程序开始运行后，
逐渐删除演示函数和源文件，并替换为您自己的应用程序代码。


专业开发者可利用以下链接快速找到有用信息：


* [下载 FreeRTOS 书籍和手册](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)。
* [了解 FreeRTOS 目录结构](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)。
* [RTOS 演示应用程序项目简介](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)。
* [修改 RTOS 演示应用程序以在其他硬件上运行](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)。
* [了解 FreeRTOS 许可证](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing)。
* [常见问题：我的应用程序无法运行，问题可能出在哪里](/Why-FreeRTOS/FAQs/Troubleshooting)？
* [使用 configASSERT() 捕获用户错误](/Documentation/02-Kernel/03-Supported-devices/02-Customization#configassert)
* [获取免费支持](https://forums.freertos.org/)。
* [获取商业许可证和开发服务](https://www.highintegritysystems.com/)。
