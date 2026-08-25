---
title: "Microchip 使用 wizC 或 fedC 的 PIC18 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

*PICmicro wizC 移植和此文档页面由 Marcel van Lieshout 提供。*

该移植
 使用
 [Forest Electronic Developments](http://www.fored.co.uk/)。该移植还可以与
 同样由 Forest ElectronicDevelopments 提供
 的 FED C 编译器一起使用。这两种环境之间的区别
 在于 fedC 中缺少快速应用程序开发前端。
 但是，该移植不使用此前端。已使用 wizC 和 fedC 的版本 11（最低 11.04c）和版本 12（最低 12.02e）成功
 测试了该移植。

最初，此移植和演示应用程序完全使用 wizC 模拟器开发。直到所有模拟运行无任何问题后，
 才开始在真实芯片上进行硬件测试。最后的硬件测试不过是一次验证：
 所有测试
 [PIC18F4620](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1335&dDocName=en010304)。

虽然 WizC 和 fedC 都不是免费或开源产品，但性价比确实非常高。WIZC Professional 还推出了精简版，
 在教育用途优势方面极具吸引力。

FreeRTOS 源代码下载包含针对 wizC/PIC18 移植的综合演示应用程序，
 主要用于测试该移植的可靠性并演示其功能。

---

### 重要提示！Microchip PIC18 wizC/fedC RTOS 移植的使用注意事项

*使用此 RTOS移植前，请阅读下述所有要点。*
1. [源代码组织](#源代码组织)
2. [使用 wizC 或 fedC IDE 的注意事项](#freertos使用-wizc-或-fedc-的注意事项)
3. [演示应用程序](#演示应用程序)
4. [配置和用法详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

 FreeRTOS 源代码下载文件包含所有 FreeRTOS 移植的源代码。
 请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
 获取下载文件的介绍以及有关创建新项目的信息。

 Microchip PIC18 wizC/fedC 移植位于/Source/portable/WizC/PIC18目FreeRTOS录
 下。您可在此目录中找到安装脚本 (install.bat)。在运行
 此脚本前，请阅读以下注意事项。

与其他移植随附的演示应用程序不同，RTOS 演示分为几个较小的程序
 。有助于在 RAM 受限的 PIC18 设备上执行演示。
 演示应用程序可以在 FreeRTOS/Demo/PIC18_WizC 目录中找到。每个应用程序
 都有自己的子目录。要将演示应用程序加载到 IDE 中，请双击项目文件（例如 Demo1.pc）。

---

### FreeRTOS使用 wizC 或 fedC 的注意事项

1. **可能需要安装其他 fedC 或 wizC 库**
FedC/wizC 版本 11：这些库可以在 fedCwizC CD 上的目录 Libraries/LibExt 中
 找到。请按照库随附的 pdf 文件中的说明进行操作：
 运行安装程序并不是全部，必须在 IDE 中进行一些更改。特别是，必须将 mem.c 作为库
 添加到 IDE 文件/库菜单中的 "16 Bit Core" 选项卡中。

 FedC/wizC版本12：此库已安装并可供使用。
2. **需要安装 Malloc 库**
该移植需要安装 malloc 库，该库可从
 [用户页面](http://www.fored.co.uk/html/user_page.html)下载，
 位于[Forest Electronic Developments](http://www.fored.co.uk/) 网站。
 下载文件随附安装说明和文档。
3. **需要安装 ANSI 头文件**
该移植需要 ANSI 头文件，可从
 [用户页面](http://www.fored.co.uk/html/user_page.html)下载，
 位于[Forest Electronic Developments](http://www.fored.co.uk/) 网站。
 下载文件随附安装说明和文档。
4. **FreeRTOS 需要安装**
Microchip PIC18 wizC/fedC FreeRTOS 是 wizC 或 fedC 开发环境中
 的一个库。需要安装库文件。移植源目录
 FreeRTOS/Source/portable/WizC/PIC18 包含一个名为 install.bat 的文件。
 此脚本将在 fedC 或 wizC 安装的 LibsUser 目录中
 安装使用该移植所需的所有文件。双击运行该脚本。
5. **WizC 和 fedC 项目设置**
WizC 和 fedC 在项目对话框中有几个优化选项。除非下文另有说明，
 否则所有选项均可根据需要进行更改。

	***使用 PIC 调用堆栈（快速调用）**
	可以指示编译器使用其软件堆栈或 PIC 调用堆栈来存储
	 调用函数时的返回地址。FreeRTOS 移植要求编译器
	 使用 PIC 调用堆栈。如果未启用此选项，则将在编译过程中标记错误。调用堆栈
	 将调用深度限制为 32 级。使用 FreeRTOS，每个任务都有自己的 32 级调用堆栈，
	 使得 PIC 调用堆栈溢出的可能性非常小。
	***本地优化字节**
	编译器可以将全局内存设置为用于存储本地变量和
	 在函数调用期间传递参数。这减少了软件堆栈的使用，
	 因此，可以提高性能。使用此 FreeRTOS 移植，
	 可以自由使用（或禁用）本地优化字节。然而，重要的是要认识到，
	 在 RTOS 下运行的每项任务都有这些本地优化字节的副本。在任务切换时，
	 “locopt” 区域将保存到任务的堆栈中。因此，区域的大小会影响
	 任务切换的性能。
6. **WizC 和 fedC 堆使用情况**
编译器使用堆将大于 4 个字节的函数返回值传回调用函数。
 出于性能原因，此移植无法保留任务切换之间的堆。因此，
 不允许函数返回大于 4 个字节的变量。为避免此类函数，
 FreeRTOS 标头包含一个杂注 ，用于通知编译器有关此限制的信息。然后，
 编译器在遇到使用堆的函数时会发出警告。虽然只发出警告，
 但不应忽略此消息，否则会发生意外行为。如果需要返回
 大于 4 个字节的变量（例如结构体），应改用指向结构体的指针。
7. **WizC 和应用程序设计器**
WizC 和 fedC 的区别在于 wizC 中存在快速应用开发前端。
 这个所谓的应用程序设计器不能与 FreeRTOS 一起使用，
 对于任何使用此 FreeRTOS 移植的项目都应关闭。
8. **最小堆栈大小**
FreeRTOSConfig.h 文件包含一个名为 configMINIMAL_STACKSIZE 的定义，
 用于定义最小任务的堆栈应包含的最小字节数。对于此移植，默认情况下，configMINIMAL_STACKSIZE 定义
 为 portMINIMAL_STACKSIZE。在 portmacro.h 中查找 portMINIMAL_STACKSIZE 时，
 您会发现最小堆栈大小是在运行时根据
 第一次引用 configMINIMAL_STACKSIZE 计算得出。这是因为最小堆栈大小取决于
 项目中的几个优化设置。建议不要更改 configMINIMAL_STACKSIZE 的定义。如果项目中的一个或多个任务需要更大的堆栈，
 请使用 configMINIMAL_STACKSIZE 作为基值：

```c
// MyTask needs 20 extra bytes
#define MyStackSIZE  ( configMINIMAL_STACKSIZE + 20 )

```

 这样，较大的堆栈仍然会根据项目中的
 优化设置自动调整。有关此函数的示例，请参阅演示应用程序。

---

### 演示应用程序

#### 演示应用程序硬件设置

虽然， PIC18 wizCfedC 移植完全在模拟器中开发，
 但运行演示应用程序的预期硬件
 是 Forest Electronic Developments 的 40 引脚 PICMicro 原型板。
 已安装 [PIC18F4620](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1335&dDocName=en010304)嵌入式微控制器。该原型板允许通过
 同样由 Forest Electronic Developments 提供的 PicProg 实用程序
 进行系统内闪存编程 (ICSP)。

使用不同的硬件平台时，该替代主板可能无法
 将 LED 连接到与用于创建移植的开发板相同的配置中。LED 例程
 包含在FreeRTOS/Demo/PIC18_WizC/ParTest/ParTest.c 中，可能需要修改。

#### 演示应用程序项目

* **Demo1**
第一个演示仅用于测试 FreeRTOS是否正确安装。该演示
 只能在模拟器中运行，这是因为它会使 8 个 LED 闪烁，而开发板仅有 4 个 LED。当然，
 也可以在 portD 有 8 个 LED 的替代板上运行该演示。  

 创建了 8 个任务。每个任务负责控制 portD 上一个 LED 的闪烁。以这样一种方式选择每个任务的闪烁速率，
 即将 portD 视为一个二进制计数器。然而，有 8 项独立的任务：
 每项任务都已获得最方便的闪烁速率。此演示是最小 FreeRTOS 项目的完美示例。
* **Demo2**
包括标准的最小“整数”、“pollQ”、“SemTest”、“Flash”任务，以及定期检查
 其他任务是否正常无错运行并相应闪烁 LED 的“检查”任务。
 为确保目标不会意外复位，应用程序启动时，
 USART 会发送“X ”。正确操作时，Demo2 将每 10 秒切换一次 LED 4。如果任何任务发生错误，
 则切换速率将增加到 1 秒。总共创建了 12 个任务。
* **Demo3**
包括标准的最小“整数”、“BlockQ”、“Flash”任务，以及定期检查
 其他任务是否正常无错运行并相应闪烁 LED 的“检查”任务。
 为确保目标不会意外复位，应用程序启动时，
 USART 会发送“X ”。正确操作时，Demo3 将每 10 秒切换一次 LED 4。如果任何任务发生错误，
 则切换速率将增加到 1 秒。总共创建了 12 个任务。
* **Demo4**
包括标准的最小“整数”、“dynamic”、“Flash”任务，以及定期检查
 其他任务是否正常无错运行并相应闪烁 LED 的“检查”任务。
 为确保目标不会意外复位，应用程序启动时，
 USART 会发送“X ”。正确操作时，Demo4 将每 10 秒切换一次 LED 4。如果任何任务发生错误，
 则切换速率将增加到 1 秒。总共创建了 11 个任务。
* **Demo5**
包括标准的最小“flop”、“Flash”任务，以及定期检查
 其他任务是否正常无错运行并相应闪烁 LED 的“检查”任务。
 为确保目标不会意外复位，应用程序启动时，
 USART 会发送“X ”。正确操作时，Demo5 将每 10 秒切换一次 LED 4。如果任何任务发生错误，
 则切换速率将增加到 1 秒。总共创建了 13 个任务。
* **Demo6**
包括标准的最小“ComTest”任务，以及定期检查
 其他任务是否正常无错运行并相应闪烁 LED 的“检查”任务。
 正确操作时，Demo6 将每 10 秒切换一次 LED 4。如果任何任务发生错误，
 则切换速率将增加到 1 秒。总共创建了 4 个任务。  

**注意**：要成功运行此演示，需要串行端口上的环回连接器。
* **Demo7**
包括标准的最小“Death”、“Flash”任务，以及定期检查
 其他任务是否正常无错运行并相应闪烁 LED 的“检查”任务。
 为确保目标不会意外复位，应用程序启动时，
 USART 会发送“X ”。正确操作时， Demo7 将每 10 秒切换一次 LED 4。如果任何任务发生错误，
 则切换速率将增加到 1 秒。Demo7 重复创建和删除任务，
 一次最多可创建和删除 10 个任务。

#### 构建演示应用程序

每个演示应用程序目录都包含自己的项目文件。双击项目 (.pc) 文件，
 可将项目加载到 wizC 或 fedC IDE 中。加载完成后，
 可以按常规方式编译项目。

一个项目由以下几个文件组成：

* **Main.c**
此文件包含演示的主应用程序代码，包括 main() 入口点。
* **Fuses.c**
将运行此演示芯片的配置设置。
* **Interrupt.c**
PIC18 MCU 仅支持单个中断矢量（此移植不使用优先中断）。
 因此，所有中断处理都集于在
 位于此文件的单个 Interrupt() 函数中，如果需要其他处理程序，则可以将其添加到此文件。有几个演示
 使用了此功能。
* **FreeRTOSConfig.h**
此项目的 FreeRTOS 配置设置。 
 请参阅 [自定义部分](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
 获取有关所有设置的说明。
* **MallocConfig.h**
Malloc 库也有配置文件。文件定义了
 私有 malloc 堆大小之类的内容。更多详细信息，请参阅 malloc 库随附的文档。
* **WIZCmake.h**
大多数演示应用程序使用FreeRTOS/Demo/Common/Minimal目录中的其他代码。为了 
 使编译器能够在FreeRTOS/Demo/Common/Include, WIZCmake.h中找到标头文件
 WIZCmake.h 需包含指向此目录的搜索路径设置（如果项目目录中存在 WIZCmake.h，
 则编译器会自动在每次编译中将其作为第一份头文件）。

#### 如何创建新项目

FreeRTOS/Demo/PIC18_WizC/Demo1目录中的演示项目非常小。开始新项目的最简单方法就是，
 将此目录中的所有文件复制到新项目目录中。

---

### 配置和用法详情

#### RTOS 移植特定配置

此移植的特定配置项目位于 FreeRTOSSourceportableWizCPIC18portmacro.h。
 此文件中定义的常量通常不需要任何修改。

可在每个项目目录中的 FreeRTOSConfig.h 文件中找到特定于应用程序的配置项目。
 此文件中的所有定义都可以修改。

可使用 ConfigTICK_RATE_HZ 定义
 来设置 RTOS 滴答的频率。演示项目提供的数值 250 Hz 可用于测试 RTOS 内核功能，
 但比大多数应用程序所要求的速度要快。降低此值可提高效率。使用过低的值时，
 编译器将标记错误。使用 40MHz 的 MCU 频率（pll 为 10MHz xtal），最低频率为 20Hz。
 降低 MCU 频率，滴答频率随之降低。

由于 PIC 移植的 RTOS 调度器运行后无法停止，因此 vPortEndScheduler() 将
 执行 MCU 重置。

#### 中断服务例程

仅使用 INTCON 寄存器中的 GIE 位。这意味着该移植当前
 不支持高/低优先中断。

每个项目都包含一份 interrupt.c 文件。可将测试每个中断标志的例程添加到
 此文件中的 Interrupt() 函数中。也可以 #include 这些例程。仔细研究演示项目，
 了解更多信息。

进入ISR 后，始终会保存当前上下文。因此，允许在 ISR 中使用整个 C 语言
 的频谱（例外：局部变量，请参见下文）。如果需要上下文切换，
 请将 uxSwitchRequested 设置为 pdTRUE。这样一来，在 ISR 退出时，准备运行的具有
 最高优先级的候选任务会恢复（激活）。请参阅 FreeRTOS/Demo/PIC18_WizC/serial，
 了解有关 ISR 例程的示例。

在 ISR 中，无法使用局部变量。要克服此限制，请使用
 以下替代方法之一：

* 使用静态变量。全局 RAM 使用量增加。
* 调用函数。需要额外的周期。
* 将变量映射到当前未使用的 SFR。此方法为首选，
 因为没有额外的开销。有关此方法的示例，请参阅 FreeRTOS/Demo/PIC18_WizC/serial/isrSerialTx.c。

#### 使用 PIC18F4620 以外的处理器

从 Microchip  PIC18 系列中选择不同的 MCU 非常简单：

* 确保新的 MCU 有足够的 RAM、ROM 和外围设备。
* 使用 wizC 或 fedC IDE 中的项目选项选择新的 MCU。
* 验证 fuses.c 中的 MCU 配置设置仍然有效。如有需要，请更改。
* （重新）编译项目。

#### 在抢占式和协同式 RTOS 内核之间切换

将项目目录中 FreeRTOSconfig.h 文件内的定义 configUSE_PREMPTION 设置为 1
 即可使用抢占式机制，设置为 0 即可使用协作式。

#### 计时器的使用

此移植使用定时器 1 上的比较匹配来生成 RTOS 滴答。在编译过程中，定时器和比较
 值会自动计算，以匹配 MCU 时钟速度。

#### 内存分配

该移植使用 malloc 库，
 可从[Forest Electronic Developments](http://www.fored.co.uk/)网站免费下载。有关详细的 API 规范，
 请参阅此库的文档。

#### 串口驱动程序

还需注意的是，编写串行驱动程序是为了测试实时内核的部分功能，并不是
 为了提供一个优化的解决方案。比特率寄存器设置为 
 根据 MCU 运行的频率自动调整。

Copyright (C) Amazon Web Services, Inc. or its affiliates. All rights reserved. 
