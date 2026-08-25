---
title: "带 MIPS M14K 核心的 Microchip PIC32 MZ RTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### 简介

#### PIC32MZ 和 PIC32MZ EF RTOS 移植

本页介绍了 FreeRTOS 移植和演示应用程序，针对具有 MIPS M14K 内核的 [PIC32MZ](http://www.microchip.com/PIC32)
和 PIC32MZ EF 32 位微控制器（来自 [Microchip](http://www.microchip.com/)）。

FreeRTOS PIC32MZ 移植：

* 维持单独的中断堆栈。如果没有单独的中断堆栈，
 每个任务堆栈必须分配足够的空间来容纳整个
 （可能是嵌套的）中断堆栈框架。
* 除了标准的任务栈溢出检测外，
 还支持中断栈溢出检测。构建时
 将
 [configCHECK_FOR_STACK_OVERFLOW](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking) 设置为 3 可开启中断栈溢出检测，
 此时[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) 也被已定义。
* 提供了一个完整的中断嵌套模型，它本身不会完全禁用
 中断。尽管 MIPS 硬件在进入中断服务程序时禁用了中断，
 但 RTOS 代码在执行任何应用程序处理程序代码之前
 就迅速重新启用了它们。

![RTOS PIC32 入门套件上的](/media/2018/PIC32MZ-StarterKit.jpg)

**PIC32MZ 入门套件**

#### 演示应用程序

演示应用程序已经过预配置，可使用
[MPLAB X](http://www.microchip.com/mplabx) IDE 和
基于 [MPLAB XC32](http://www.microchip.com/XC32) GCC 的
编译器。提供三种构建配置； 针对
PIC32MZ 入门套件的 PIC32MZ2048_SK，以及 PIC32MZ2048EF_SK_SOFT_FLOAT 和
PIC32MZ2048EF_SK_HARD_FLOAT -两者都针对
[带有 FPU (EF) 入门套件的 PIC32 嵌入式连接](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=DM320007)。

演示项目的配置可用于构建简单的 blinky 演示或
综合测试和演示应用程序。综合应用程序展示
并测试中断嵌套行为。本页提供了构建说明
。

---

### 重要提示！PIC32 MZ RTOS 移植使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含
所有 RTOS 移植的源代码和演示应用程序，因此它包含的大多数文件与
PIC32MZ 演示无关。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解下载文件的描述，以及关于创建新项目的信息。

构建 PIC32MZ RTOS 演示的 MPLAB X 项目位于
FreeRTOS/Demo/PIC32MZ_MPLAB 目录中。

### 演示应用程序

#### 功能

常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，定义于
main.c 的顶部，用于在简单 "blinky" 样式的入门项目
和更全面的测试和演示应用程序之间切换。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 会调用 main_blinky()。
main_blinky () 创建一个非常简单的示例，此示例使用两个
任务、一个队列和一个软件定时器。
* Blinky 软件定时器：

 此示例展示了自动重载的软件定时器。定时器回调
 的唯一功能是切换 LED。
* 队列发送任务：

 队列发送任务由 prvQueueSendTask() 函数实现。
 任务位于每 200 毫秒向队列发送一次值 100
 的循环中。
* 队列接收任务：

 队列接收任务由 prvQueueReceiveTask()
 实现。任务位于一个循环中，阻止
 从队列读取的尝试（在阻塞时不消耗 CPU 周期），
 每次收到一个值时就切换一个 LED。由于队列发送任务
 每 200 毫秒向队列写一次，
 队列接收任务每 200 毫秒切换一次 LED。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 会调用 main_full()。
main_full() 创建一个非常全面的测试和演示应用程序，
创建大量 RTOS 任务和软件定时器。
* 第一个 LED 由简单的 "闪烁" 软件定时器控制。
* 第二个 LED 由被中断触发的任务控制
 。它提供了一个如何编写 FreeRTOS 兼容的
 中断服务程序的例子（RTOS 兼容的中断服务程序
 在本页也有描述）。
* 演示创建的大多数 RTOS 任务不会更新 LED，因此
 没有任何可见指示显示它们正在正常运行。因此，
 最后 LED 由“检查”软件定时器控制。软件
 定时器用于监控其他所有任务，并切换 LED。如果
 其他所有任务都按预期执行，LED 将
 每三秒钟切换一次。如果在其他任何任务中发现疑似错误，
 切换速率将增加到 200 毫秒。
* 使用一个任务和两个任务进行中断嵌套
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
2. 将 PIC32MZ 入门套件的调试 USB 连接器连接到
 您的主机（运行 MPLAB X 的计算机）。
3. 在 MPLAB X "Debug" 菜单中，选择 "Debug Project"。此项目
 应该在没有错误或警告的情况下构建，
 并将结果二进制文件编入 PIC32 闪存中。

### 配置和用法详情

#### RTOS 移植特定配置

此演示的特定配置项目包含在 FreeRTOS/Demo/PIC32MZ_MPLAB/FreeRTOSConfig.h 中。可以编辑
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
 请注意，只有以 FromISR () 结尾的 API 函数可以从 ISR 内部调用。
 FreeRTOS 维护用于 ISR 的单独 API ，以确保中断
 条目尽可能快速和标准，并确保
 从任务和中断中使用的各自的 API 版本
 都可以为其特定的使用场景进行优化。

 configKERNEL_INTERRUPT_PRIORITY 应设置为最低优先级。

 优先级高于 configMAX_SYSCALL_INTERRUPT_PRIORITY 的中断
 不会被内核的临界区所掩盖，
 因此不会受到 RTOS 内核活动的影响-在硬件本身的限制下。

 通过演示，演示应用程序定义
 configMAX_SYSCALL_INTERRUPT_PRIORITY 为 3，configKERNEL_INTERRUPT_PRIORITY 为 1，
 所有其他中断为：

	+ 用于唤醒切换 LED 的任务的中断优先级
	 被分配为 3 -这与 configMAX_SYSCALL_interrupt_PRIORITY 的设置相等，
	 因此是可以调用中断安全的
	 FreeRTOS API 函数的最高优先级。
	+ 分配中断嵌套测试使用的两个定时器
	 优先级分别为 2 和 3。尽管它们都可以访问
	 相同的两个队列，优先级 3 中断可以安全地中断
	 优先级 2 中断。两者都可以中断 RTOS tick。
	+ 最后，高频定时器中断的优先级
	 被配置为 4 -高于configMAX_SYSCALL_INTERRUPT_PRIORITY，
	 因此内核活动永远不会阻止
	 高频定时器立即执行中断
	 （在硬件本身的限制下）。从这个中断中
	 访问队列是不安全的，即使使用中断
	 安全 RTOS API 函数。

每个移植都将 "BaseType_t" 定义为
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

PIC32MZ 演示中的 T5 中断（用于演示任务从中断中解锁的定时器中断）
可以作为一个例子-其汇编代码包装器
复制到列表 1 中，其 C 处理程序复制到
列表 2 中。

---

```c

/* Prototype to be included in a C file to ensure the vector is
correctly installed. Note that because this ISR uses the FreeRTOS
assembly wrapper the IPL setting in the following prototype has no
effect. The interrupt priority is set using the Microchip provided
library functions. */
void __attribute__( (interrupt(ipl3), vector(_TIMER_5_VECTOR)))
                                                    vT5InterruptWrapper( void );

/* Header file in which portSAVE_CONTEXT and portRESTORE_CONTEXT are defined. */
#include "ISR_Support.h"

/* Ensure correct instructions is used. */
.set	nomips16
.set 	noreorder

/* Interrupt entry point. */
vT5InterruptWrapper:

  /* Save the current task context. This line MUST be included! */
  portSAVE_CONTEXT

  /* Call the C function to handle the interrupt. */
  jal vT5InterruptHandler
  nop

  /* Restore the context of the next task to execute. This line
 MUST be included! */
  portRESTORE_CONTEXT

  .end  vT5InterruptWrapper

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

void vT5InterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Give the semaphore. If giving the semaphore causes the task to leave the
 Blocked state, and the priority of the task is higher than the priority of
 the interrupted task, then xHigherPriorityTaskWoken will be set to pdTRUE
 inside the xSemaphoreGiveFromISR() function. xHigherPriorityTaskWoken is
 later passed into portEND_SWITCHING_ISR(), where a context switch is
 requested if it is pdTRUE. The context switch ensures the interrupt returns
 directly to the unblocked task. */
    xSemaphoreGiveFromISR( xBlockSemaphore, &xHigherPriorityTaskWoken );

    /* Clear the interrupt */
    IFS0CLR = _IFS0_T5IF_MASK;

    /* See comment above the call to xSemaphoreGiveFromISR(). */
    portEND_SWITCHING_ISR( xHigherPriorityTaskWoken );
}

```

**列表 2：ISR 中可能导致上下文切换的 C 部分**

---

关于 C 函数的一些说明：

* 如果不需要进行上下文切换， 传递给 portEND_SWITCHING_ISR() 的参数应该是 0，
 如果需要进行上下文切换， 则非 0。
 从中断的内部执行上下文切换可能会导致
 中断返回到最初中断的任务之外的任务。
* C 函数不使用任何特殊限定符或属性-它
 只是一个标准的 C 函数。

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

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 PIC32 演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。

