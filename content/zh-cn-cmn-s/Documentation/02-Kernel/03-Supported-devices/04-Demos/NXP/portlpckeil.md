---
title: "飞利浦 LPC2129 (ARM7) RTOS Keil/RVDS开发工具的移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |
| --- |
| <br />![mcb2100.gif](/media/2018/mcb2100.gif)<br /> |

***请注意：***从FreeRTOS V5.1.0 开始，本页面上展示的演示已经不再使用旧版和已经停止供应的 Keil DKARM 编译器，
改用最新的 Keil/RVDS/ARM 编译器。

此移植在[MCB2100开发/原型开发板](http://www.keil.com/mcb2100)上开发
（如果您想使用其他开发板，可以参考[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)） 
。事实证明，Keil 模拟器也非常有用。全套开发工具包可
由  [Hitex 开发工具](http://www.hitex.co.uk/)获取。

MCB2100 是一款功能齐全的综合原型板，可轻松访问 LPC2129 外设，
包括 8 个内置 LED，由FreeRTOS演示应用程序使用。

开发工具中包含一整套由编译器、汇编器和链接器组成的工具链、IDE 以及
性能出色的设备专用模拟器。模拟器中包含“逻辑分析器”功能，可用于监视微控制器 IO，
在模拟环境中提供与 LED 在真实目标硬件上工作时的实际视觉反馈一样的模拟视觉反馈。遗憾的是，
这些工具的评估版受到了限制，ROM 和 RAM 的组合映像大小被限制为 16 KB，这一限制太过严苛，导致无法运行此演示
（因为 FreeRTOS 堆内存包含在 16 KB 中，即使未使用堆内存时，也是如此）。

---

### *重要提示！Keil/ARM/RVDS LPC2129 RTOS 移植*使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件远多于运行此演示所需的文件。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
下载文件的描述和有关创建新项目的信息。

此演示的 uVision  项目文件称为 RTOSDemo.Uv2，可位于 Demo/ARM7_LPC2129_Keil_RVDS 目录中。
该项目包含两个配置，一个使用 ARM 指令集，另一个使用 THUMB 指令集。

---

### 演示应用程序

FreeRTOS 源代码下载包含用于 Keil LPC2000 RTOS 移植的完全抢占式多任务演示应用程序。

#### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在 COM 1 的 P1 串行端口连接器上将引脚 2 和 3 连接在一起
——通常情况下，使用回形针便能实现此目的）。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。

#### 功能

此演示应用程序创建了 25 个任务。如果演示应用程序正确执行，其表现如下：
* LED P1.16、P1.17 和 P1.18 由 "flash" 任务控制。每个 LED 将以恒定频率闪烁，LED P1.16
 速度最慢， LED P1.18 速度最快（请参见下面的逻辑分析器屏幕截图）。
* 串行端口上每传输一个字符， LED P1.19 都会闪烁。
* 串行端口上每传输一个字符， LED P1.20 都会闪烁。
* 并非所有任务都会改变 LED，所以没有可见的指示来表明它们运行正常。
 因此，系统创建了一个检查任务，用于确保所有其他任务中没有检测到任何错误。

 LED P1.23 由检查任务控制。检查任务每 3 秒就会将系统中的所有任务检查一次，
 以确保任务执行无误。然后切换 LED P1.23。如果 LED P1.23 每 3 秒切换一次，
 则表明没有检测到错误。如果切换频率提高到 500 毫秒，则表示 'Check' 任务
 至少发现了一个错误。可以通过将环回连接器从串行端口（如上述）上移除来检查此机制，
 这样做是在故意制造一个错误。

请参阅  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解各个任务的详细信息。

#### 构建演示应用程序

1. 从 Keil uVision3 IDE 中打开 Demo/ARM7_LPC2129_Keil_RVDS 项目文件
2. 如下所示，选择 ARM 或 THUMB 配置：

![](/media/2018/Keil-uVision-RTOS-Demo-Select-Configuration.jpg)

选择 ARM 或 THUMB 配置

4. 从 IDE 的 "Project" 菜单中选择 "Built Target"。

应用程序应能成功构建，不出现任何错误或警告。

#### 运行演示应用程序

该演示应用程序可以在模拟器中或在目标硬件上执行。

要在模拟器和 JTAG 调试器之间切换：

1. 如下图所示，右键单击 "Project Workspace" 窗格中的 FreeRTOS_ARM 或 FreeRTOS_THUMB 目标。

![](/media/2018/keildebug1.gif)

在 "Project Workspace" 窗格中右键单击目标

3. 从生成的弹出菜单中选择 "Options for Target FreeRTOS"。
4. 然后会出现一个弹出窗口。选择 "Debug" 选项卡。
5. 如下图所示，使用单选按钮在模拟器和 JTAG 调试器之间切换。

![](/media/2018/keildebug2.gif)

在模拟器和 ULINK JTAG 调试器之间切换

#### 使用模拟器和逻辑分析器

微控制器 IO 端口可以使用模拟器的“逻辑分析器”功能进行监控。下方
是在模拟演示应用程序时使用逻辑分析器监控某些输出引脚时
的屏幕截图。

![](/media/2018/logicanalyzer.gif)

监控逻辑分析器中的端口引脚

红线、绿线、蓝线分别表示由 "Flash" 任务控制的引脚 P1.16、P1.17 和 P1.18。黑线表示
引脚 P1.19，每当传输字符时就会切换该线。您需要近距离放大，
才能看到为每个传输的字符切换的线路。

模拟时，检查任务会在 "ComTest" 任务中发现一个错误。这是因为 "ComTest" 任务需要
上述环回连接器。

#### 编写闪存

可以在 Keil IDE 中通过 "Flash" 菜单项将演示应用程序编程到微控制器闪存中。
必须重置原型板才能开始执行程序。
必须先对闪存进行编程，然后才能使用 JTAG 调试器。

---

### 配置和用法详情

#### RTOS 移植特定配置

此移植的特定配置项目位于 Demo/ARM7_LPC2129_Keil_RVDS/FreeRTOSConfig.h中。可以编辑此文件中定义的常量
确保适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。此移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

如果中断导致某个任务（通过队列或信号量事件）解除阻塞，并且解除阻塞的任务的优先级高于被中断的任务，
则可能需要从中断服务程序内部进行上下文切换。

不会引起上下文切换的中断服务程序没有特殊要求，可以按照
正常的 RVDS 语法写入。
会引起上下文切换的中断服务程序需要用到汇编文件包装器，具体如下所示。

```c

    ;To define an interrupt service routine first we need an assembly file wrapper.
 ;The wrapper is installed in the interrupt controller as the interrupt entry
 ;point.

    ;portmacro.inc must be included within the assembly file as this defines
 ;the portSAVE_CONTEXT and portRESTORE_CONTEXT macros.
    INCLUDE portmacro.inc

    ;Here the C portion of the handler is imported so it can be called from this
 ;assembly file. The asm wrapper is exported so it can be installed in the
 ;interrupt controller.
    IMPORT vUART_ISRHandler
    EXPORT vUART_ISREntry

    ;Interrupt entry must always be in ARM mode.
    ARM
    AREA    |.text|, CODE, READONLY
    PRESERVE8

;Define the interrupt entry point.
vUART_ISREntry

    ;portSAVE_CONTEXT must be the first thing called in the wrapper.
    portSAVE_CONTEXT

    ;The rest of the interrupt functionality can be implemented in a standard C
 ;function. Call the function now.
    LDR R0, =vUART_ISRHandler
    MOV LR, PC
    BX R0

    ;Finish off by restoring the context of the task that has been chosen to
 ;run next - which might be a different task to that which was originally
 ;interrupted.
    portRESTORE_CONTEXT

    END

```

有关完整示例，请参阅演示应用程序中的文件 Demo/ARM7_LPC2129_Keil_RVDS/serial/serialISR.s。

汇编文件包装器调用 C 函数（在上方示例中，该 C 函数被称为 vUART_ISRHandler()），
可以在该函数中实现主中断功能。C 函数没有特殊要求，因而不需要任何特殊函数
限定符。有关完整示例，请参阅 Demo/ARM7_LPC2129_Keil_RVDS/serial/serial.c 中的 vUART_ISRHandler() 函数。
vUART_ISRHandler() 还演示了宏 portEXIT_SWITCHING_ISR()，该宏用于确保
在中断退出时选择正确的任务来运行。

#### 使用 LPC2129 以外的部件

LPC2129 使用带有特定于处理器的外围设备的标准 ARM7 内核。核心实时内核组件应该
可以在所有 ARM7 设备上移植，但是需要考虑到外设设置和内存需求。
需要考虑的事项：
* Source/portable/Keil/ARM7/port.c 中的 prvSetupTimerInterrupt() 配置 LPC2129 定时器 0 以生成滴RTOS答。
* 端口、内存访问和系统时钟由 Demo/ARM7_LPC2129_Keil_RVDS/main.c 中的 prvSetupHardware() 配置。
* 中断服务程序设置和管理假设存在向量中断控制器。
* 串口驱动程序。
* 文件 lpc21xx.h 中提供了寄存器位置定义，该文件位于 Demo/ARM7_LPC2129_Keil_RVDS/的FreeRTOSConfig.h顶部。
* 启动代码、内存映射和向量表设置位于 Demo/ARM7_LPC2129_Keil_RVDS/Startup.s 中。
* RAM 大小：参见下面的内存分配部分。

#### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/ARM7_LPC2129_Keil_RVDS/ 中的定义 configUSE_PREEMPTION 设置为 1，FreeRTOSConfig.h可使用抢占式；
设置为 0，则可使用协同式。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是以
提供的演示应用程序项目文件为基础构建您的应用程序，如[源组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节所示。

#### 执行上下文

RTOS 调度器以监管者模式执行，任务以系统模式执行。
注意：
 启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。

中断服务例程总是在 ARM 模式下运行。

Demo/ARM7_LPC2129_Keil_RVDS/Startup.s 为系统/用户、IRQ 和 SWI 模式配置堆栈。

SWI 指令由实时内核使用，不能被应用程序代码使用。

#### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ARM7 演示应用程序的 makefile 中，以提供实时内核所需的
内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
以获取完整信息。

#### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。
