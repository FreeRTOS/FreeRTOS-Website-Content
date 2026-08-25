---
title: "适用于使用 IAR 编译器的 Renesas RL78 微控制器的 FreeRTOS"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR 编译器](https://www.iar.com/products/iar-embedded-workbench-for-renesas-78k)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/Renesas-RL78-YRPBRL78G13-promo-board.jpg)  

 RL78/G13 Promotion Board 评估板 (YRPBRL78G13)

|  |
| --- |
| [**该演示已被支持更多 RL78 <br />部件号和评估板的演示所取代。点击查看文档<br /> 页面。**](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RTOS_RL78_IAR_Demos) |

**该项目需要 IAR Embedded Workbench（ RL78 (EWRL78) 1.10 版本或更高版本）。EWRL78 的免费 KickStart 版本
 [可从 IAR 网站 ](http://www.iar.com/ewrl78/) 下载。**

本页记录的应用程序演示了如何将 FreeRTOS
在 [Renesas RL78 16 位微控制器](http://www.renesas.com/pr/mcu/rl78/index.html)上使用的应用程序。

根据配置，此演示项目在 RL78/G13 Promotion Board
([YRPBRL78G13](http://am.renesas.com/products/tools/introductory_evaluation_tools/renesas_demo_kits/yrpbrl78g13/yrpbrl78g13.jsp)) 上运行，
该评估板配备了 R5F100LEA 微控制器。R5F100LEA 为软件
应用程序提供了略低于 4K 字节的可用 RAM，
不足以在单一应用程序中充分演示所有 FreeRTOS 功能。
然而，RL78 系列内确实有多达 32K 字节的 RAM，
几乎是 R5F100LEA 的 RAM 的八倍之多。R5F100LEA 演示创建了
13 个任务、4 个队列和 2 个定时器。

** 注意：**如果项目生成失败，可能是因为您使用的 IAR
嵌入式工作台版本过低。如果是这种情况，
那么也可能是项目文件(在无提示的情况下)已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR 。

---

### 重要提示！Renesas RL78 RTOS 移植使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件中包含所有 FreeRTOS 移植的源代码，
因此包含的文件远多于此演示所使用的文件。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
详细了解下载文件的描述和创建新项目的信息。

适用于 IAR RL78 Promo Board 演示的 Renesas Embedded Workbench 工作区被称为
RTOSDemo.eww，位于 FreeRTOS/Demo/RL78_RL78G13_Promo_Board_IAR
目录下。

---

### 演示应用程序

#### 演示应用程序硬件设置

演示应用程序使用直接安装在 promo board 板硬件上的 LED，
因此无需额外的硬件设置。

#### 功能

本部分介绍了 RL78G13 演示的功能。总共使用了 13 个任务、
4 个队列和 2 个定时器。一些任务来自
“标准演示”任务集。这些是所有 FreeRTOS 演示的常见内容，
并非 RL78 所特有。它们仅用于演示 FreeRTOS API 的使用，
及测试核心 FreeRTOS 功能。

除了标准演示任务外，还创建了以下特定演示任务：

* **寄存器测试任务** 

 这两个任务会测试 RTOS 内核上下文切换机制：
 首先用已知的唯一值填充各 RL78 寄存器，
 然后重复检查写入寄存器的原始值
 是否在整个任务周期内均保持在寄存器中。这些任务以尽可能低的优先级执行
 （空闲优先级），因此经常被抢占
 。

 这些任务的性质决定了它们必须用汇编语言编写。
* **“检查”软件定时器和回调** 

 检查定时器是一种非常简单的监视定时器。它
 会监视所有其他标准演示任务、寄存器检查任务
 和演示软件定时器，并使用 LED 提供有关系统状态的视觉反馈
 。

 检查定时器的周期最初设置为 3 秒。
 检查定时器回调函数会检查所有标准演示任务、
 寄存器检查任务和演示定时器是否不仅仍在执行中，
 而且执行时没有报告任何错误，然后会切换 LED。

 如果检查定时器发现某个任务或定时器已停滞，
 或报告了错误，那么它会从最初的 3 秒周期变换到
 200 毫秒。因此，如果 LED 每 3 秒切换一次，
 则表示未发现任何问题。如果 LED 每 200 毫秒切换一次，
 则表示已在至少一个任务或演示定时器中发现问题。
* **“演示”软件定时器和回调** 

 演示定时器回调函数的唯一作用是递增变量。
 演示定时器的周期是相对于检查定时器的周期设置的。
 这使得检查定时器知道
 在每次执行检查定时器回调函数之间
 演示定时器回调函数应该执行的次数。演示定时器回调中递增的变量
 会被检查定时器用来确定演示定时器回调
 是否正以预期速度执行。

main.c 还包括堆栈溢出、空闲和 malloc 文件挂钩函数的示例。

当正确执行时，演示应用程序将每 3 秒切换用户 LED。

#### 构建演示应用程序

1. 在 IAR Embedded Workbench IDE 中打开 FreeRTOS/DemoRL78_RL78G13_Promo_Board_IAR/RTOSDemo.eww 工作区。
2. 按 F7 构建项目。构建项目时不应出错，
 或生成警告。

#### 对微控制器进行编程和调试

1. 确保 YRPBRL78G131 演示板连接到主计算机，
 且所需 USB 驱动器已正确安装（
 首次连接硬件时会出现安装驱动器的提示）
2. 从 Embedded Workbench 的 "Project" 菜单中选择 "Download and Debug"。
 闪存被编程时会有短暂延迟，
 之后调试器会在进入 main() 函数时中断。

---

### 配置和使用详情

#### RTOS 移植专用配置

此演示的特定配置项目位于
[FreeRTOS/DemoRL78_RL78G13_Promo_Board_IAR/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。可对此文件中
定义的常量进行编辑以适应您的应用程序。

还有一个专门针对 Renesas RL78 移植和演示的常量：

* **configCLOCK_SOURCE**
 将 configCLOCK_SOURCE 设置为 0 以使用外部时钟源，或设置为 1 以使用高速内部时钟源。
 更改任何时钟配置时，请确保 configCPU_CLOCK_HZ 设置正确。

每个移植 #defines 'BaseType_t 等于该处理器的最有效数据类型。本端口将
BaseType_t 定义为短整型。

请注意，vPortEndScheduler() 尚未实现。

#### 内存模型

FreeRTOS 移植将在近端和远端内存模型之间自动切换，
具体取决于 IAR 项目选项中的设置。我们已使用两种内存模型组合对该移植进行了测试，
分别是：

1. 都设置为近端的数据和代码模型。
2. 都设置为远端的数据和代码模型。

#### 编写中断服务程序

不会引起上下文切换的中断服务程序没有特殊要求，可以按照
IAR 编译器文档中的描述编写。

通常，上下文切换需要中断服务程序。
例如，正在接收的串行端口字符可以解除对高优先级任务（在阻塞状态下等待该字符到达）的阻塞
。如果已解除阻塞任务的
优先级高于当前任务优先级，则 ISR 应直接返回
至已解除阻塞的任务。由于 IAR 内联汇编器的限制，
该中断服务程序必须使用汇编文件包装器来输入。请参阅
以下示例。首先是汇编文件包装器。

---

```c

; ISR_Support.h defines the portSAVE_CONTEXT and portRESTORE_CONTEXT
; macros.
#include "ISR_Support.h"

 ; The wrapped implemented in the assembly file.
 PUBLIC vISRWrapper

 ; The portion of the handler that is implemented in an external C file.
 EXTERN vISRHandler

 ; Ensure the code segment is used. 
 RSEG CODE:CODE

; The wrapper is the interrupt entry point.
vISRWrapper:

 ; The ISR must start with a call to the portSAVE_CONTEXT() macro to save
 ; the context of the currently running task.
 portSAVE_CONTEXT

 ; Once the context is saved the C portion of the handler can be called.
 ; This is where the interrupting peripheral is actually serviced.
 call vISRHandler

 ; Finally the ISR must end with a call to portRESTORE_CONTEXT() followed by
 ; a reti instruction to return from the interrupt to whichever task is
 ; now the task selected to run (which may be different to the task that
 ; was running before the interrupt started).
 portRESTORE_CONTEXT
 reti

 ; The interrupt handler can be installed into the vector table in the same
 ;assembly file.

 ; Ensure the vector table segement is used. 
 COMMON INTVEC:CODE:ROOT(1)

 ; Place a pointer to the asm wrapper at the correct index into the vector
 ; table. Note 56 is used is purely as an example. The correct vector
 ; number for the interrupt being installed must be used. 
 ORG 56
 DW vISRWrapper

```

---

用于中断处理程序的示例汇编文件包装器。

中断处理程序的 C 部分只是一个标准 C 函数。

---

```c

/* This standard C function is called from the assembly wrapper above. */
void vISRHandler( void )
{
short sHigherPriorityTaskWoken = pdFALSE;

 /* Handler code goes here, for purposes of demonstration, assume
 at some point the hander calls xSemaphoreGiveFromISR().*/
 xSemaphoreGiveFromISR( xSemaphore, &sHigherPriorityTaskWoken );

 /* If giving the semaphore unblocked a task, and the unblocked task has a
 priority that is higher than the currently running task, then
 sHigherPriorityTaskWoken will have been set to pdTRUE. Passing a pdTRUE
 value to portYIELD_FROM_ISR() will cause this interrupt to return directly
 to the higher priority unblocked task. */
 portYIELD_FROM_ISR( sHigherPriorityTaskWoken );
}

```

---

示例中断处理程序的 C 部分。

#### RTOS 内核使用的资源

RTOS 内核使用间隔定时器生成 RTOS tick。函数 prvSetupTimerInterrupts() 在
FreeRTOSSourceportableIARRL78port.c 中可被更改为使用任何方便的定时器源。

RTOS 内核还需要独占使用 BRK 软件中断指令。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

演示应用程序项目中包含 SourcePortableMemMangheap_1.c，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
