---
title: "源组织"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 源组织信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

### 简介

每个 RTOS 移植都附有一个预配置的演示应用程序，该应用程序已构建必要的 RTOS 源文件， 
并包含必要的 RTOS 头文件。强烈建议将所提供的演示程序作为 
所有基于 FreeRTOS 的新应用程序的基础。此页面旨在帮助 
查找和了解所提供的项目。


### 基本目录结构

FreeRTOS 下载文件包括每个处理器移植和每个演示应用程序的源代码。将所有移植放在一个单一的下载包中， 
大大简化了发布工作， 
但文件数量可能看起来令人生畏。然而，目录结构非常简单，FreeRTOS 实时内核 
***仅包含在 3 个文件中*** 
（如需要[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers/)、  [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups) 
或协程功能，则需要其他文件）。

从顶部开始，下载被分割成两个子目录：FreeRTOS 和 FreeRTOS-Plus。如下所示：

```c
+-FreeRTOS-Plus    Contains [FreeRTOS-Plus](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction) components and demo projects.
|
+-FreeRTOS         Contains the FreeRTOS real time kernel source
                   files and demo projects
```

FreeRTOS-Plus 目录树包含多个描述其内容的自述文件。


### FreeRTOS 内核目录结构

核心 FreeRTOS 内核源文件和演示项目包含在两个子目录中，如下所示：

```c
FreeRTOS
    |
    +-Demo      Contains the demo application projects.
    |
    +-Source    Contains the real time kernel source code.
```

核心 RTOS 代码包含在三个文件中，分别称为 task.c、queue.c 和 list.c。 
这三个文件位于 FreeRTOS/Source 目录中。同一目录包含两个 
名为 timers.c 和 croutine.c 的可选文件，分别实现软件计时器和协程功能。

每个受支持的处理器架构都需要少量的架构特定 RTOS 代码。这是 
RTOS 可移植层，位于 FreeRTOS/Source/Portable/[compiler]/[architecture] 
子目录，其中 [compiler] 和 [architecture] 分别是用于创建移植的编译器 
和移植运行的架构。

出于 
[内存管理页面上所述的原因](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)， 
示例堆分配方案也位于可移植层中。各种示例 heap_x.c 
文件位于 FreeRTOS/Source/portable/MemMang 目录中。

**可移植层目录示例：**

* 如果将 TriCore 1782 移植与 GCC 编译器一起使用：

  TriCore 特定文件 (port.c) 位于 FreeRTOS/Source/Portable/GCC/TriCore_1782 目录中。 
  除 FreeRTOS/Source/Portable/MemMang 外，所有其他 FreeRTOS/Source/Portable 子目录 
  都可以忽略或删除。

* 如果将 Renesas RX600 移植与 IAR 编译器一起使用：

  RX600 特定文件 (port.c) 位于 FreeRTOS/Source/Portable/IAR/RX600 目录中。除 
  FreeRTOS/Source/Portable/MemMang 外，所有其他 FreeRTOS/Source/Portable 子目录 
  都可以忽略或删除。

* 所有移植都是如此......

FreeRTOS/Source 目录的结构如下所示。

```c
FreeRTOS
    |
    +-Source        The core FreeRTOS kernel files
        |
        +-include   The core FreeRTOS kernel header files
        |
        +-Portable  Processor specific code.
            |
            +-Compiler x    All the ports supported for compiler x
            +-Compiler y    All the ports supported for compiler y
            +-MemMang       The sample heap implementations
```

FreeRTOS 下载还包含每个处理器架构和编译器移植的演示应用程序 
。大多数演示应用程序代码对所有移植都通用，位于 
FreeRTOS/Demo/Common/Minimal 目录中（位于 FreeRTOS/Demo/Common/Full 
目录下的是历史遗留代码，仅用于 PC 移植）。

其余的 FreeRTOS/Demo 子目录包含用于构建单个 
演示应用程序的预配置项目。子目录的命名与移植平台和编译器相关。每个 RTOS 移植 
[都有自己的网页](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)， 
详细说明了该移植演示应用程序所在的目录。


**演示目录示例：**

* 如果构建的 TriCore GCC 演示应用程序面向 Infineon TriBoard 硬件：

  TriCore 演示应用程序项目文件位于 FreeRTOS/Demo/TriCore_TC1782_TriBoard_GCC 
  目录中。FreeRTOS/Demo 目录下的所有子目录（Common 目录除外） 
  都可以忽略或删掉。

* 如果构建的 RenesasRX6000IAR 演示应用程序面向 RX62N RDK 硬件：

  IAR 工作区文件位于 FreeRTOS/Demo/RX600_RX62N-RDK_IAR 目录中。所有其他 
  FreeRTOS/Demo 目录下的所有子目录（Common 目录除外） 
  都可以忽略或删除。

* 所有移植都是如此......

FreeRTOS/Demo 目录的结构如下所示。

```c
FreeRTOS
    |
    +-Demo
        |
        +-Common    The demo application files that are used by all the demos.
        +-Dir x     The demo application build files for port x
        +-Dir y     The demo application build files for port y
```
---


### 创建您自己的应用程序

**[更多详细信息请参阅[创建新的 FreeRTOS 应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)页面]**  

提供预配置的演示应用程序，以确保项目已经存在， 
其中包括正确的 RTOS 内核源文件，并设置了正确的编译器选项， 
从而最大限度地减少用户的工作量。因此，强烈建议通过修改现有的预配置演示应用程序 
来创建新应用程序。首先构建现有的演示应用程序， 
确保可以实现干净的构建， 
然后在 FreeRTOS/Demo 目录中将项目中包含的文件逐渐替换为自己的应用程序源文件。
