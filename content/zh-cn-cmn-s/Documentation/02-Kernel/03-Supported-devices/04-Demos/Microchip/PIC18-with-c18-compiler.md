---
title: "Microchip PICmicro (PIC18) RTOS 移植 适用于 MPLAB C18 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![fored.jpg](/media/2018/fored.jpg)

目前有两个移植适用于嵌入式微控制器的 Microchip PICMicro PIC18 系列。本页内容仅与
使用 MPLAB C18 编译器的移植有关。

PICMicro PIC18 RTOS 移植是在 Forest Electronic Developments (FED) 公司的 [40 引脚的 PICmicro 原型板](http://www.fored.co.uk/devboard.HTM) 上开发而成的 
（如果想使用其他开发板，可参阅此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。

已安装 [PIC18F452](http://www.microchip.com/stellent/idcplgidcplg?IdcService=SS_GET_PAGE&nodeId=1335&dDocName=en010296)
微控制器。该原型板可通过 PICPROG 实用程序进行系统内闪存编程，
该程序也由 FED 提供。

[MPLAB C18 开发工具](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en010014)
与 [MPLAB IDE](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en019469) 前端一起使用
。MPLAB 开发工具下载中包含的实时模拟器用于调试。

但是，该编译器*并非*免费或开源的，而且似乎也没有合适的其他开源方案。
不过，IDE 和模拟器是免费的，而开发工具可以下载，并且提供相当长的评估期。也可
下载功能有限的学生版本。

---

### 重要！PICMicro MPLAB RTOS 移植使用注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

MPLAB PIC18 演示应用程序项目文件位于 Demo/PIC18_MPLAB 目录下。

---

### 演示应用程序

与其他移植随附的 RTOS 演示应用程序不同，PICMicro PIC18 RTOS 演示分为几个较小的程序，
有助于在 RAM 受限的 40 引脚设备上执行演示。64 和 80 引脚设备本需要
成本更高的原型板。所有三个 RTOS 演示应用程序都包含在一个名为 RTOSDemo.mcw 的工作区中，
可在 MPLAB IDE 中打开工作区。

#### 演示应用程序项目

 演示应用程序工作区包括以下三个项目。

* **RTOSDemo1**

 包括标准的最小“整数”和 “pollQ” 任务，以及定期检查
 其他任务是否正常无错运行并相应闪烁 LED 的“检查”任务。为确保目标不会意外重置，
 应用程序启动时，会从 USART 传输一个 “X”。正确操作时，RTOSDemo1 会
 让 LED 1 每秒切换一次。如果在任何任务中发生错误，切换速率将增加到 100 毫秒。
* **RTOSDemo2**

 包括标准最小“闪烁”任务，以及“整数”任务的修改版本。为确保目标不会意外重置，
 应用程序启动时，会从 USART 传输一个 “X”。正确操作时，RTOSDemo2 会
 让 LED 1 每 333 毫秒切换一次，LED 2 每 666 毫秒切换一次，LED 3 每 999 毫秒切换一次。LED 4 仅在整数任务遇到错误时
 会常亮。
* **RTOSDemo3**

 包括标准最小 “comtest” 和最小“整数”任务，以及检查任务。该演示
 会测试 ISR 内的上下文切换，并要求在 J2 上放置环回连接器（即引脚 2 和
 引脚 3 必须短接到串行端口上）。为确保目标不会意外重置，
 应用程序启动时， LED 1 会亮 500 毫秒。正确操作时，只要有字符传输，RTOSDemo3 都会切换 LED 3，
 接收到字符时会切换 LED 4，LED 2 会每秒切换一次（如果为 100 毫秒切换一次意味着存在错误），
 在最初闪烁 500 毫秒后，LED 1 将保持关闭状态。

请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分，
了解更多标准演示应用程序文件的信息。

#### 构建 RTOS 演示应用程序

RTOS 演示应用程序项目文件包含绝对路径定义。如果您能解决该问题，
 请告知我们！若要在您的系统上使用项目文件，可能
 需要更改路径。最简单的方法是打开文本编辑器中的 RTOSDemo1.mcp、RTOSDemo2.mcp 和 RTOSDemo3.mcp 文件，
 并根据需要进行编辑。搜索字符串 "e:dev"，找到需要
 修改的行。

1. 打开 MPLAB IDE 中的工作区后，右键点击项目窗口中的项目名称，
 并从弹出菜单中选择 "Set as Active Project"，以选择要构建的项目。
2. 从 MPLAB IDE 的 "Project" 菜单中选择 "Build all"。根据工作区中选择的项目，输出 RTOSDemo1.hex、RTOSDemo2.hex 或 RTOSDemo3.hex
 。

#### 对 PICMicro PIC18 进行编程

使用 FED 提供的 PICPROG 实用程序对原型板进行编程。PICPROG 可以打开 Intel 十六进制和二进制文件。
然而，我发现很多时候十六进制文件无法被正确识别（也许是十六进制文件格式间
不兼容？）。从 PICPROG 中打开并查看文件时，第一个字节应为 E7（十六进制）——
一个 GOTO 指令。如果情况并非如此，请将十六进制文件转换为二进制文件，然后再打开（指令如下）。

1. 确保主机连接到 FED 原型板，并且原型板已通电，
 然后启动 PICPROG。
2. 构建所需的 RTOS 演示应用程序，如上所述。
3. 下载 [HEX2BIN](http://gnuwin32.sourceforge.net/packages/hex2bin.htm) 并将其放置在路径中。
4. 打开命令提示符并导航至 Demo/PIC18_MPLAB 目录。
5. 运行 MakeBin1.bat、MakeBin2.bat 或 MakeBin3.bat，具体取决于您构建的演示。此操作会将
 已创建的十六进制文件转换为一个名为 RTOSDemo.bin 的文件。请注意，无论转换为何种十六进制文件，都使用相同的 .bin 输出文件名。
6. 在 PICPROG 中，从 file 菜单中选择 "Clear Buffer"，然后打开创建的 RTOSDemo.bin 文件。
7. 请确保配置熔丝按如下设置。有时保留这些值，有时不保留。如果
 熔丝未正确设置，请双击 "Fuses" 一词，按图所示进行设置。这还确保了
 不启用监视器。

![](/media/2018/fuses.gif "配置熔丝设置")
8. 单击 "Write Device" 速度按钮（带有手状图标的按钮）。

### 配置和使用详情

#### 编译器使用的内存区域

MPLAB 编译器不会生成可重入代码。特别是，执行数学运算时，
它会将内存区域作为暂存器使用。这些内存区域由 RTOS 内核保存为各任务上下文的一部分，以确保
重入性。任务上下文中保存的 RAM 量由宏 portCOMPILER_MANAGED_MEMORY_SIZE 设置，
该宏位于 Source/portable/MPLAB/PIC18F/port.c 中。

构建应用程序后，请检查映射文件中 .tmpdata 和 MATH_DATA 部分的大小。如果这些部分的大小超过 19
 字节，则要对常量 portCOMPILER_MANAGED_MEMORY_SIZE、宏 portSAVE_CONTEXT 和宏 portRESTORE_CONTEXT
 进行相应修改。不清楚该数据块是否始终为固定大小，还是
 依应用程序而定。

#### 内存分配

Source/Portable/MemMang/heap_1.c 包含在 PICMicro 演示应用程序项目中，用以提供实时内核所需的
内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
了解完整的信息。

#### 链接器脚本

随演示应用程序提供的链接脚本会创建一个大型内存区域，用以保存
heap_1.c 文件中定义的堆。这样的安排对演示应用程序很有效。

MPLAB 开发工具存在以下限制，如链接器手册所述：*“使用 MPLINK 链接器和 MPLAB C18 C 编译器时，不得合并数据内存区域。
MPLAB C18 要求所有部分必须位于
单个内存库中。*” 根据用户应用程序的内存要求，可能会
违反这一限制。John Franklin 提供了一个示例，说明了如何避免这种情况（如有需要）。
John 的示例文件以及包含详细信息的 pdf 文件
[可点击此处获取](http://www.realtimeengineers.com/PIC_Linker_Files.zip)。

#### 开发工具选项

与所有的移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是基于提供的演示应用程序项目
搭建您的应用程序。

#### RTOS 移植特定配置

此移植的特定配置项位于 Demo/PIC18_MPLAB/FreeRTOSConfig.h 中。
可以编辑此文件中定义的常量，
以适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但

每个移植会定义 (#define) 'BaseType_t' 为该处理器的最有效数据类型。此移植将
BaseType_t 定义为 char 类型。

#### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/PIC18_MPLAB/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，即可使用抢占式内核；设置为 0即可使用
协同式内核。

#### 演示应用程序串行端口驱动器

提供的串行端口驱动器是为了测试某些 RTOS 内核功能而编写的，并非表示
一个优化的解决方案。

#### 使用 MPLAB 模拟器

使用 MPLAB IDE 模拟器时，请确保监视器处于禁用状态，
 可通过 MPLAB IDE 的 Configuration 菜单上的  "Configuration Bits"  选项进行确定。此外，请记得每次执行后清除文件寄存器。该操作可通过使用
 MPLAB IDE 中的 Debugger->Clear Memory 菜单项完成。

#### 使用其他 PICMicro PIC18 设备

* 要运行演示应用程序，微控制器必须提供至少与 PIC18F452 相同的 RAM。
* 必须修改所选设备的链接器脚本文件，目的是要提供一个足够大的内存块，
 用以包含 heap_1.c 中定义的内存池。演示应用程序项目中包含的链接器脚本演示了如何实现此操作。
* 通过 RTOS 移植和 RTOS 演示应用程序访问的外围设备使用 MPLAB PIC18
 编译器头文件中定义的常量。由此保证了
 设备间的可移植性。然而，使用其他设备可能需要利用不同的定时器和 CCP
 外围设备，以生成 RTOS 内核 tick。定时器设置包含在 prvSetupTimerInterrupt() 中，
 可在 PICMicro PIC18 specific port.c 文件中找到。

#### 使用其他硬件平台

 选择 FED 原型板是因为其功耗低，但是将演示应用程序移植到其他平台应该很容易做到。

* 其他板不太可能有与 FED 演示板相同配置的
 LED 连接。LED 例程包含在 Demo/PIC18_MPLAB/ParTest/ParTest.c 中，且需要修改。

