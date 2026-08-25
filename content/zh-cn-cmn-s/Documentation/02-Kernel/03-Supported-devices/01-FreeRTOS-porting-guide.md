---
title: "新建 FreeRTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


***如果使用众多现有的移植和演示应用程序，则无需阅读或理解此页面！***


将 FreeRTOS 移植到完全不同且尚未支持的微控制器并非易事。本页的目的是 
描述启动新移植所需的内务管理初始工作。

每个移植都具有一定的独特性，并且非常依赖于所使用的处理器和工具，因此本页无法提供 
移植细节的详细信息。不过已经存在[许多其他 FreeRTOS 移植](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)， 
建议将这些移植作为参考。

在同一个处理器系列中移植则直接得多，例如，从一个基于 ARM7 
的设备移植到另一个。如果您的目标是修改现有的演示程序， 
可以从详细介绍[如何修改现有演示程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)的文档页面 
开始阅读。

[模板移植](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/template) 
可作为为新架构开发 FreeRTOS 移植的切入点。


### 设置目录结构

FreeRTOS 内核源代码通常包含在对所有移植通用的 3 个源文件（如果使用协程，则为 4 个）， 
和一个或两个 “移植”文件，用于根据特定的架构定制 RTOS 内核。

建议采取的步骤:

1. 下载最新版 FreeRTOS 源代码。

2. 将文件解压到方便的位置，注意保持目录结构。

3. 熟悉[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)和目录结构。

4. 创建一个目录，用于包含 [architecture] 移植的“port”文件。按照链接中概述的惯例， 
   目录的形式应为：FreeRTOS/Source/portable/[compiler name]/[processor name]。例如， 
   如果使用的是 GCC 编译器，则可以在现有的 
   FreeRTOS/Source/portable/GCC 目录下创建一个 [architecture] 目录。

5. 将空 port.c 和 portmacro.h 文件复制到刚创建的目录中。这些文件应只包含 
   需要实现的函数和宏的存根。有关此类函数和宏的列表， 
   请参阅现有的 port.c 和 portmacro.h 文件。只需删除函数和宏正文， 
   即可从这些现有文件中创建一个存根文件。

6. 如果要移植到的微控制器上的堆栈从高内存向下增长到低内存， 
   则将 portmacro.h 中的 portSTACK_GROWTH 设置为 -1 ，否则将 portSTACK_GROWTH 设置为 1。

7. 创建一个目录，用于包含 [architecture] 移植的[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)文件。
   按照惯例，该格式应为 FreeRTOS/Demo/[architecture\\_compiler] 或类似格式。

8. 将现有 FreeRTOSConfig.h 和 main.c 文件复制到刚创建的目录中。同样，应将这些文件编辑为仅存根文件。

9. 不妨看看 FreeRTOSConfig.h 文件：该文件包含一些适合您选择的硬件设置的宏。

10. 从刚创建的目录中创建一个目录，并将其命名为 ParTest（可能是 FreeRTOS/Demo/[architecture\\_compiler]/ParTest）。
    将 ParTest.c 存根文件复制到此目录中。

11. ParTest.c 包含三个简单函数来执行如下操作：

	1. 设置一些可以使 LED 闪烁的 GPIO，
	2. 设置或清除特定的 LED ，以及
	3. 切换 LED 的状态。

    These three functions need implementing for your development board. Having LED outputs working will facilitate the rest 
	所需的工作。
    请查看其他演示项目中包含的许多现有 ParTest.c 文件示例（名称 ParTest 是 
	PARallel port TEST 的曾用名） ，以及[描述如何修改现有演示应用程序的页面]
	(/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) ，获取有关写入和测试 ParTest.c 函数的信息。


### 创建项目


现在，所有必需的文件都已就绪，您需要创建一个项目（或 makefile）来成功构建这些文件。
很显然，这些文件只包含存根，所以还不会完成任何操作，但是一旦开始构建， 
就可以用工作函数逐渐替换存根。

该项目需要包含以下文件：

* Source/tasks.c
* Source/Queue.c
* Source/List.c
* Source/portable/[compiler name]/[processor name]/port.c
* Source/portable/MemMang/[heap_1.c (or heap_2.c or heap_3.c or heap_4.c)](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
* Demo/[processor name]/main.c
* Demo/[Processor name]/ParTest/ParTest.c

下列目录需要在包含路径中，请使用 Demo/[Process name] 
目录中的相对路径-而不是绝对路径：

* Demo/Common (i.e. ../Common)
* Demo/[Processor Name]
* Source/include
* Source/portable/[Compiler name]/[Processor name]


### 实现存根

现在来完成最困难的部分。编译项目后，就需要实现可移植层存根。建议 
首先实现 pxPortInitialiseStack() 函数。若要实现 pxPortInitialiseStack()， 
必须首先确定任务上下文堆栈帧结构体，该结构体对架构的依赖性非常高。
  

### 获取帮助

一定要记得，[WITTENSTEIN high integrity systems](https://www.highintegritysystems.com/openrtos/) 提供完整的移植和测试服务！
