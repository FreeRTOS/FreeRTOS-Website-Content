---
title: "带 MIPS M4K 核心的 Microchip PIC32 MX RTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |  |
| --- | --- |
| <br /><br /><br />![正在使用 MPLAB RealICE 调试的 Microchip Explorer 16 开发板上的 PIC32 PIM](/media/2018/PIC32_RealICE.jpg)<br /><br /><br />**Explorer 16 带 PIC32 PIM** <br /><br /><br /> | <br />![PIC32 USB II 入门套件](/media/2019/PIC32_USB_Starter_Kit_II.jpeg)<br /><br /><br />**PIC32 USB II 入门套件** <br /><br /> |

### 引言

#### PIC32MX RTOS 移植

本页介绍了 FreeRTOS 移植和演示应用程序，针对 [PIC32MX](http://www.microchip.com/PIC32)——
来自 [Microchip](http://www.microchip.com/) 的具有 MIPS M4K 核心的 32 位微控制器
。

FreeRTOS PIC32MX 移植：

* 提供完整中断嵌套模型。
* 从不完全禁用中断——尽管 MIPS 内核
 在发生异常时已经自行禁用了中断，但异常处理程序中的
 RTOS 代码会快速重新启用此中断。
* 维持单独的中断栈。这确保了分配给
 RTOS 任务的各个堆栈不需要每个都提供足够空间，
 用于存放可能存在嵌套的完整中断栈帧。
* 除了标准的任务栈溢出检测外，
 还支持中断栈溢出检测。构建时
 将
 [configCHECK_FOR_STACK_OVERFLOW](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking) 设置为 3 可开启中断栈溢出检测，
 此时[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) 也被已定义。

FreeRTOS 是 MPLAB Harmony - Microchip'的集成驱动程序
和中间件包的组成部分。旧版[应用程序说明](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1824&appnote=en544728)
（和源代码）也可从 Microchip  网站上获得，其说明了如何将
FreeRTOS 集成到 Microchip'的现有旧版外设和中间件库。

#### 演示应用程序

[MPLAB X](http://www.microchip.com/mplabx) 和
[MPLAB XC32](http://www.microchip.com/XC32)
分别为目前构建 FreeRTOS 演示的首选 IDE 和首选编译器。MPLAB 8
项目仍然包含在 RTOS 源代码下载中，
但会在未来的某个版本中停用。

通过在 MPLAB X 项目中提供多项构建配置，可以预先配置对多个 PIC32
派生品和硬件平台的支持
。针对下述对象提供的构建配置：

* [Explorer 16](http://www.microchip.com/explorer16) 评估板上的 PIC32MX360F512 PIM。
* Explorer 16 评估板上的 PIC32MX460F512L PIM。
* Explorer 16 评估板上的 PIC32MX795 PIM。
* PIC32 USBII 入门套件（还配备了 PIC32MX795）。

MPLAB 8 项目被预先配置为针对运行在 Explorer 16 评估板上的 PIC32MX360 微控制器
。

各构建配置均可用于构建简单的 blinky 演示或
全面测试和演示应用程序。综合应用程序展示
并测试中断嵌套行为。本页提供了构建说明
。

---

### 重要提示！PIC32 RTOS 移植使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此，
包含的文件比 PIC32 演示使用的文件多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解下载文件的描述，以及关于创建新项目的信息。

PIC32MX / MIPS 移植的 MPLAB 8 演示应用程序工作区称为
RTOSDemo.mcw，位于 FreeRTOS/Demo/PIC32MX_MPLAB 目录中。
MPLAB X 项目称为 RTOSDemo.X，位于该目录之外。

### 演示应用程序

#### 演示应用程序硬件设置 - Explorer 16

所有 Explorer 16 跳线都可以保留在默认位置，特别是，应配备 JP2 以确保 LED 能正确工作。

演示应用程序包括经由 UART2 发送和接收字符的任务。一个任务发送的字符必须由另一个任务接收。
如果丢失了任何字符或接收顺序错误，则会标记错误情况。需要将环回连接器连接到 Explorer16 9 路 D 型插口上，
才能运行此机制（插口的引脚 2 和 3 应连接在一起）。默认情况下不使用 UART 本身的内部环回模式。

**注意：**UART 中断服务程序 (ISR) 使用一个 RTOS 队列从
ISR 发送单个字符到 RTOS 任务，用另外一个 RTOS 队列从
RTOS 任务发送单个字符到 ISR。用队列
以这种方式发送单个字符非常低效。提供的 UART 驱动程序
旨在演示从 ISR 使用的队列，
并对RTOS 移植进行压力测试。它并不是用来表示一个有效的中断实现。

#### 功能

可对演示应用程序进行配置，使其提供非常简单的 "blinky" 样式的功能，
或者提供 RTOS特性子集的全面测试和演示
。常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
定义于 main.c 的头部，用于在上述两项之间切换。

演示应用程序任务分为标准演示任务和演示特定
任务。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务仅用于演示 FreeRTOS API 和测试移植，不得用作其他用途。

#### 当将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 会调用 main_blinky()。
main_blinky () 创建一个非常简单的示例，此示例使用两个
任务、一个队列和一个软件定时器。
* Blinky 软件定时器：

 此示例展示了自动重载的软件定时器。定时器回调
 的唯一功能是切换 LED。
* 队列发送任务：

 队列发送任务由 prvQueueSendTask() 函数实现。
 prvQueueSendTask() 只位于一个循环中，每 200 毫秒向队列发送值 100
 。
* 队列接收任务：

 队列接收任务由 prvQueueReceiveTask()
 实现。prvQueueReceiveTask() 位于一个循环中，阻止
 从队列读取的尝试（在阻塞时不消耗 CPU 周期），
 每收到一个值就切换一个 LED。队列发送任务
 每 200 毫秒写入队列，所以队列接收任务
 每 200 毫秒取消阻塞并切换一次 LED。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 会调用 main_full()。
main_full() 创建一个非常全面的测试和演示应用程序，
用于创建大量 RTOS 任务和软件定时器。此演示会在
Explorer 16 和 USB II 入门套件上执行，尽管在入门套件上执行时，
未使用 LCD 和 UART 任务（因为它们在硬件上不可用），
且创建了少量 flash 任务，以允许下述“检查定时器”访问
入门套件硬件上的三个可用 LED 之一。
在 Explorer 16 上执行此演示时，以下描述是正确的。
* 标记为 D3 至 D5 的 LED 由 "flash"
 软件定时器控制。每盏灯将以恒定频率闪烁，LED D3
 速度最快，LED D5 速度最慢。
* LED D7 会在每次传输字符时进行切换
 。切换频率太高会导致
 无法区分字符之间的单次切换，
 但完整消息传输之间的间隔
 是可以察觉的。出于测试考量，每条消息之间的延迟是伪随机的
 。

 请注意，PIC32MX795 演示不包括串口测试任务，
 因为它的 UART IP 与
 PIC32MX460 和PIC32MX360 上的 UART IP 略有不同。
* 每当接收到字符并在串行端口上通过环回连接器进行验证时，
 LED D8 都会闪烁。
 同样地，切换频率太高，会导致无法区分单次
 切换。
* 大多数任务不会更新 LED 状态，
 因此没有任何可见指示显示它们正在正常运行。因此，
 创建了“检查”软件定时器来监视所有其他任务。
 检查软件定时器回调每
 3 秒监测一次系统运行情况，然后通过
 LCD 任务向 LCD 写入PASS 或 FAIL 消息。任何故障都会被锁定，
 显示的消息会表明在哪个任务中检测到了故障
 （可以在演示执行过程中
 移除环回连接器来测试此功能，
 并为此专门在 UART 环回测试任务中创建一条错误）。如果不存在错误，
 则显示 PASS 消息，
 消息中包含高频定时器发来的计数值。高频
 定时器中断的执行频率为 20 KHz，每
 20000 次中断增加一次显示值。因此，
 此显示值应以秒为单位。关于
 高频定时器的更多信息，请参阅本页面上的
 [RTOS 配置和使用](#中断服务程序)
 部分。

 检查软件定时器回调也会切换 LED D10。如果
 检测到错误，切换频率会相应增加。
* 该应用程序还演示了如何使用“网关守卫”任务，
 这里使用的是 LCD 网关守卫。只允许 LCD
 任务直接访问 LCD。其他
 希望向 LCD 写入消息的任务会将队列上的消息发送给
 LCD 任务，而非直接访问 LCD
 本身。LCD 任务只在等待消息的队列中发生阻塞（因此它不
 消耗任何 CPU 周期）
 ——收到消息后任务会自动解除阻塞
 并显示消息。
* 使用一个任务和两个中断进行中断嵌套
 -所有中断都访问两个相同的队列。两个
 中断在不同的优先级运行，并且都
 高于 RTOS 内核的中断优先级，这意味着这个特殊的测试
 所展示的最大嵌套深度为 3。高频定时器中断
 又增加了一个嵌套层次。请参阅
 [RTOS 配置和使用](#中断服务程序)
 章节，了解关于执行
 中断的更完整说明，及其各自的优先级。

### 使用 MPLAB X 构建和调试演示应用程序

这些说明假定您已在主机上正确安装了 MPLAB X 和 MPLAB XC32
安装在您的主机上。

 1. 从 MPLAB X IDE 内部打开项目（
 项目位置详见
 靠近本页面顶部的源代码组织章节）。
2. 选择与硬件配置匹配的构建
 配置。有三项构建配置针对的是 Explorer 16 硬件，
 一项构建配置针对 PIC32 USB II 入门套件。要使用入门套件，
 则必须选择 USB_II_STARTER_KIT 构建配置，
 因为 LED 映射各不相同。

![](/media/2018/MPLAB_X_Build_Configurations.jpg)

**在 MPLAB 中选择构建配置**
3. 如果正在使用 Explorer 16，
 请按照 Explorer 16 手册的说明，将 ICD3 或 Real ICE 调试器接口
 连接到 Explorer 16 开发板。

 如果正在使用 USB II 入门套件，
 则直接使用入门套件 PCB 上标记为 J1 的 USB 连接器连接入门套件
 。
4. 在 IDE 的 'Debug' 菜单中，选择 "Debug Project"。此项目
 应该在没有错误或警告的情况下构建，
 并将结果二进制文件编入 PIC32 闪存中。

### 配置和用法详情

#### RTOS 移植特定配置

此演示的特定配置项目包含在 FreeRTOS/Demo/PIC32MX_MPLAB/FreeRTOSConfig.h 中。可以编辑
在该文件中定义的常量，以适配您的应用程序。特别是——

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS tick 的频率。提供的 1000 Hz 的值
 对测试 RTOS 内核功能很有用，
 但比大多数应用程序所要求的速度要快。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY** 和 **configMAX_SYSCALL_INTERRUPT_PRIORITY**
请参阅[中断配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)
 章节（RTOS 内核配置文档中）了解
 这些选项的完整信息。

 configKERNEL_INTERRUPT_PRIORITY 设置 RTOS 内核使用的中断优先级，
 并且通常设置为尽可能低的中断优先级。
 configMAX_SYSCALL_INTERRUPT_PRIORITY 设置了最高中断优先级，
 从中可以调用队列、软件定时器和信号量 API 函数。
 请注意，只有以 FromISR() 结尾的 API 函数才能从
 ISR 中调用。

 configKERNEL_INTERRUPT_PRIORITY 应设置为最低优先级。

 优先级高于 configMAX_SYSCALL_INTERRUPT_PRIORITY 的中断
 不会被内核的临界区所掩盖，
 因此不会受到 RTOS 内核活动的影响-在硬件本身的限制下。

 通过演示，演示应用程序定义
 configMAX_SYSCALL_INTERRUPT_PRIORITY 为 3，configKERNEL_INTERRUPT_PRIORITY 为 1，
 所有其他中断为：

	+ UART 被分配的优先级为 2。这意味着它可以中断
	 RTOS tick，也可以安全地使用中断安全队列函数。
	+ 配置了两个定时器来生成中断，
	 以测试嵌套和队列访问机制。为这些定时器分配的
	 优先级分别为 2 和 3。尽管它们都可以访问
	 相同的两个队列，优先级 3 中断可以安全地中断
	 优先级 2 中断。两者都可以中断 RTOS tick。
	+ 最后，高频定时器中断的优先级
	 设置为 4，因此内核活动永远不会阻止
	 高频定时器立即执行中断
	 （在硬件本身的限制下）。从这个中断中
	 访问队列是不安全的，即使使用中断
	 安全 RTOS API 函数，因为它的优先级高于 configMAX_SYSCALL_INTERRUPT_PRIORITY。

每个移植 #defines 'BaseType_t' 为对该处理器而言最有效的
。此移植将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

无法嵌套的断开服务程序没有特殊要求，可以
按照编译器文档编写。但是，以这种方式编写的中断
将利用被中断的那个任务的堆栈，
而不是系统堆栈，
因此必须为每个创建的任务分配足够的堆栈空间。因此，不建议以这种方式
写入中断服务程序。

可以嵌套的中断服务程序需要一个简单的汇编包装器，
请参阅下文。建议以这种方式写入所有中断。

PIC32 演示中的 UART 中断可用作示例——
列表 1 中概述了此演示采用的汇编代码包装器，
列表 2 中概述了相应的 C 函数处理程序：

---

```c

/* Prototype to be included in a C file to ensure the vector is
correctly installed. Note that because this ISR uses the FreeRTOS
assembly wrapper the IPL setting in the following prototype has no
effect. The interrupt priority is set using the ConfigIntUART2()
PIC32 peripheral library call. */
void __attribute__( (interrupt(ipl1), vector(_UART2_VECTOR)))
                                                    vU2InterruptWrapper( void );

/* Header file in which portSAVE_CONTEXT and portRESTORE_CONTEXT are defined. */
#include "ISR_Support.h"

/* Ensure correct instructions is used. */
.set	nomips16
.set 	noreorder

/* Interrupt entry point. */
vU2InterruptWrapper:

  /* Save the current task context. This line MUST be included! */
  portSAVE_CONTEXT

  /* Call the C function to handle the interrupt. */
  jal vU2InterruptHandler
  nop

  /* Restore the context of the next task to execute. This line
 MUST be included! */
  portRESTORE_CONTEXT

  .end  vU2InterruptWrapper

```

**列表 1：用于处理可导致上下文切换的中断的汇编代码包装器**

---

关于汇编文件包装器的一些说明：

* 我发现放置包装器的汇编文件必须
 有一个 .S 扩展名 (大写的 S)。使用小写 .s 可能
 导致 portSAVE_CONTEXT 和 portRESTORE_CONTEXT 宏
 内嵌错误。
* portSAVE_CONTEXT 和 portRESTORE_CONTEXT 宏必须
 分别作为函数中的第一行和最后一行可执行行。
* 当 FreeRTOS 汇编文件包装器用作入口点时，
 ISR 函数原型中的 IPL 设置无效。

其次，由汇编文件包装器调用的 C 函数：

---

```c

        void vU2InterruptHandler( void )
        {
        /* Declared static to minimise stack use. */
        static BaseType_t xYieldRequired;

            xYieldRequired = pdFALSE;

            /* Are any Rx interrupts pending? */
            if( mU2RXGetIntFlag() )
            {
                /* Process Rx data here. */

                /* Clear Rx interrupt. */
                mU2RXClearIntFlag();
            }

            /* Are any Tx interrupts pending? */
            if( mU2TXGetIntFlag() )
            {
                /* Process Tx data here. */

                /* Clear Tx interrupt. */
                mU2TXClearIntFlag();
            }

            /* If sending or receiving necessitates a context switch, then switch
 now. */
            portEND_SWITCHING_ISR( xYieldRequired );
        }

```

**列表 2：ISR 中可能导致上下文切换的 C 部分**

---

关于 C 函数的一些说明：

* 如果调用了 portEND_SWITCHING_ISR()，则必须在 C 函数中的最后一行调用它
 。
* 如果不需要进行上下文切换，传递给 portEND_SWITCHING_ISR() 的参数应该是 0，
 如果需要进行上下文切换， 则非 0。
 从中断的内部执行上下文切换可能会导致
 中断返回到最初中断的任务之外的任务。
* C 函数不使用任何特殊限定符或属性-它
 只是一个标准的 C 函数。

如需查看完整示例，请参见 PIC32 演示应用程序中的完整 UART 中断处理程序——
但是请注意，下载的 UART 驱动程序旨在
生成大量中断（用于测试
MIPS 移植的稳健性），因此不应将其视为最佳解决方案。

#### 临界区

退出临界区将始终设置中断优先级，以便启用所有中断，无论输入临界区时的级别如何
。FreeRTOS API 函数本身将使用临界区。

#### 执行上下文

根据 XC32 编译器手册中记录的惯例， RTOS
内核假定所有对 K0 和 K1 寄存器的访问都是原子性的。由
XC32 编译器生成的代码符合这一惯例，所以如果您只用 C 语言编写应用程序，就无需担心这个问题。
但是，如果使用任何手写的汇编代码，必须注意确保它也符合同样的惯例。

#### Shadow 寄存器

中断 Shadow 寄存器未被使用，因此可供主机应用程序使用。不应在可能导致上下文切换的
中断服务程序中使用 Shadow 寄存器。

#### 软件中断

RTOS 内核使用 MIPS 软件中断 0，因此应用程序无法使用该中断。

#### 抢占式内核和协同式 RTOS 内核之间的切换

将 FreeRTOS/Demo/PIC32MX_MPLAB/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式；设置为 0，
可使用协同式。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 PIC32 演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。特别是，它们大量使用队列机制，不使用可用的 FIFO 或 DMA。
