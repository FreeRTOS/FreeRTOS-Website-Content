---
title: 构建您的首个 FreeRTOS 项目
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 如何启动构建 FreeRTOS 的项目
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS
  - title: FreeRTOS 实现教程
    link: /Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FreeRTOS 参考手册
    link: /Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book/
  - title: 修改 FreeRTOS 演示
    link: /Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos/


previous:
  title: RTOS 基本概念
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals
next:
  title: FreeRTOS 库和第三方工具
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools
---


## 引言

FreeRTOS 的设计初衷是简单易用：仅需要 3 个
适用所有 RTOS 移植的源文件和 1 个微控制器专用的源文件，
其 API 的设计简单而直观。

FreeRTOS [已移植到许多不同的微控制器架构](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)和许多
不同的编译器。每个官方移植都附有一个官方演示
（至少在创建时），无需任何修改即可在其硬件开发平台上
编译和执行。

提供演示项目是为了确保新用户可以在最短时间内上手使用 FreeRTOS，
最大限度地降低学习和探索成本。

FreeRTOS 支持的每个架构都用于许多不同的微控制器，
这意味着 FreeRTOS 可以在成千上万个各不相同的微控制器上
顺利工作。将此数字乘以支持的编译器数量，
再乘以市面上与日俱增的开发板和开发入门套组，
虽然我们已经尽了最大努力，但很明显的是
我们提供的官方演示只能完全适用于很小一部分的
设备组合。

**强烈建议在新建 FreeRTOS 项目时，
[从提供的预配置演示入手，然后进行相应改编](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)。
此举可以确保新项目包含所有必要的源文件和头文件，并安装必要的中断服务例程，无需项目创建者付出额外的努力。
**

一些 FreeRTOS 用户也想知道如何从头开始创建 FreeRTOS 项目，
而不是在已有项目的基础上进行改编。此操作的具体过程
详见下文。

## 简易 FreeRTOS 演示项目入门

[另请参阅[快速入门指南](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide)和演示应用程序[简介页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)。]

### 立即尝试，使用 Windows 或 Linux 移植，或在 QEMU 中运行

还没有硬件？别担心，您可以在 Windows 或 Linux 环境中使用免费工具
以及 FreeRTOS Windows 或 Linux 移植来运行简易 blinky 演示，但是这些 RTOS 移植都不会表现出
真正的实时行为。
您还可以[使用 QEMU 中的 FreeRTOS Arm Cortex-M3 移植运行演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model)。

如果您是初学者，请先不要阅读
[Windows](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)
或 [Linux](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux) RTOS 移植的主文档页面，而是先配置示例，
以使用 [blinky 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#simple-blinky-demo-configuration)（暂时忽略[全面演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)）
。对于 Windows 的详细说明如下。


### Windows 说明

![使用 Windows 进行简易 FreeRTOS 演示](/media/2018/FreeRTOS_Windows_Blinky.jpg)

1. 如果尚未安装，请下载并安装
   [免费版 Microsoft Visual Studio](https://visualstudio.microsoft.com/vs/community)。
2. 请[下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)并解压缩 FreeRTOS 官方发行版（如尚未完成）。
3. 启动 Visual Studio，然后使用 "File|Open|Project/Solution" 菜单项
   打开 Win32.sln 解决方案文件，该文件位于
   FreeRTOS 官方发行版的 FreeRTOS/Demo/WIN32-MSVC 目录中。
4. 找到 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 定义
   （位于 main.c 顶部），并确保将其设置为 1。
5. 编译前请先阅读 main_blinky.c 顶部的注释，然后
   调试或运行应用程序。

![Windows 中简易 RTOS 演示输出的结果](/media/2018/RTOS_Windows_Output.jpg)
*适用于 FreeRTOS Windows 移植版本的简易 blinky 演示输出的结果*

## FreeRTOS 项目剖析

FreeRTOS 应用程序与非 RTOS 应用程序的启动和执行方式并无二致，
如果调用 [vTaskStartScheduler()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/03-vTaskStartScheduler) 的话，另当别论。vTaskStartScheduler()
通常从应用程序的 main() 函数调用。RTOS 仅控制
调用 vTaskStartScheduler() 后的执行顺序。

我们**强烈建议**您确保代码在选择的目标上正确执行
（正确的启动代码、正确的链接器配置等），
然后再开始尝试使用 RTOS 功能。


### 源文件

FreeRTOS 作为标准 C 源文件提供，
与项目中的其他 C 文件共同构建。FreeRTOS 源文件
以 zip 文件形式分发。[RTOS 源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面
介绍了 zip 文件夹中的文件结构。

您的项目必须至少包含以下源文件：

* FreeRTOS/Source/tasks.c
* FreeRTOS/Source/queue.c
* FreeRTOS/Source/list.c
* FreeRTOS/Source/portable/[compiler]/[architecture]/port.c
* FreeRTOS/Source/portable/MemMang/heap_x.c [其中 "x" 可以是 1、2、3、4 或 5](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)。

如果包含 port.c 文件的目录也包含程序集语言文件，
那么也必须使用程序集语言文件。


### 可选源文件

如果需要[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)功能，请在项目中添加 FreeRTOS/Source/timers.c。

如果需要[事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)功能，请在项目中添加 FreeRTOS/Source/event_groups.c。

如果需要[流缓冲区或消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)功能，请在项目中添加
FreeRTOS/Source/stream_buffer.c。

如果需要协程功能，请在项目中添加 FreeRTOS/Source/croutine.c（请注意，协程已弃用，
不推荐用于新设计）。


### 头文件

以下目录必须位于编译器的 include 路径中（必须告知编译器在这些目录中搜索
头文件）：

* FreeRTOS/Source/include
* FreeRTOS/Source/portable/[compiler]/[architecture]。
* 无论哪个目录包含要使用的 FreeRTOSConfig.h 文件，请参阅下文“配置文件”段落。

根据移植的不同，也可能需要将相同的目录放在汇编器的 include 路径中。


### 配置文件

每个项目还需要一个名为 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 的文件。 FreeRTOSConfig.h
它为正在构建的应用程序量身定制 RTOS 内核。因此，它是取决于
应用程序的，而不是 RTOS，并且应位于应用程序目录中，
而不是 RTOS 内核源代码目录中。

如果您的项目包含 heap_1、heap_2、heap_4 或 heap_5，则 FreeRTOSConfig.h 的
configTOTAL_HEAP_SIZE 定义将决定 FreeRTOS 堆的大小。如果
configTOTAL_HEAP_SIZE 设置得太高，则您的应用程序将无法建立连接。

FreeRTOSConfig.h 中的 configMINIMAL_STACK_SIZE 定义
设定了闲置任务使用的堆栈大小。如果 configMINIMAL_STACK_SIZE 设置得太低，
则空闲任务将造成栈溢出。建议您找到
使用相同微控制架构的 FreeRTOS 官方演示，
复制其中的 configMINIMAL_STACK_SIZE 设置。FreeRTOS 演示
项目存储在 FreeRTOS/Demo 目录的子目录中。
请注意，一些演示项目的时间距离现在比较久，因此不包含所有可用的
配置选项。


### 中断矢量

**[Cortex-M 用户：有关安装中断处理程序的信息，详见[“我创建的应用程序可以编译，但无法运行](/Why-FreeRTOS/FAQs/Troubleshooting)”常见问题]**


每个 RTOS 移植都使用定时器来生成周期性滴答中断。许多移植使用额外的中断
来管理上下文切换。RTOS 移植所需的中断由提供的 RTOS 移植源文件
提供服务。

RTOS 移植所提供的中断处理程序的安装方法取决于
所使用的移植和编译器。请参阅针对所使用移植提供的官方演示应用程序，
必要时也可复制。另请参阅官方演示应用程序配套的[文档页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)
。
