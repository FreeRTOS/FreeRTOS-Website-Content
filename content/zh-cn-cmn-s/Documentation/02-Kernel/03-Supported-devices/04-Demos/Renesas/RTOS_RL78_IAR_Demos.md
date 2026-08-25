---
title: "适用于 Renesas RL78 MCU 的 FreeRTOS 使用 IAR 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR 编译器](https://www.iar.com/products/architectures/renesas/iar-embedded-workbench-for-renesas-rl78/)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

|  |  |
| --- | --- |
| ![Renesas RL78 RPBRL78G13 评估板](/media/2018/Renesas-RL78-YRPBRL78G13-promo-board.jpg) | ![Renesas RL78/G14 入门套件 (RSK)](/media/2018/rsk_rl78g14.jpg) |
\| <br/>**Renesas RL78 推广和入门套件** <br/> \|

本页记录的应用程序演示了如何将 FreeRTOS
用于 [Renesas RL78 16 位微控制器](http://www.renesas.com/pr/mcu/rl78/index.html)。

该演示包括五个独立的构建配置，分别用于以下
设备评估板：

* YRPBRL78G13 - Renesas RL78/G13 推广板
* YRDKRL78G14 - Renesas RL78/G14 开发板
* RSKRL78G1C - Renesas RL78/G1C 入门套件
* RSKRL78L13 - Renesas RL78/L13 入门套件
* RL78/G1A TB - Renesas RL78/G1A 目标板

**注意：**
本页描述的项目需要使用 IAR Embedded Workbench，
版本不低于 RL78 (EWRL78) 1.30.2。EWRL78 免费评估版
[可从
 IAR 网站下载](http://www.iar.com/ewrl78/)。

如果项目构建失败，可能是使用的 IAR
Embedded Workbench 版本过低。如果打开 IAR 项目所使用的
EWRL78 版本低于创建项目时所使用的版本，
则通常会损坏项目文件（无提示），因此需要
先从 FreeRTOS zip 文件下载内容中恢复项目的原始副本，然后再继续使用
更新后的编译器。

---

### 重要提示！Renesas RL78 RTOS 移植使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件中包含所有 FreeRTOS 移植的源代码，
因此包含的文件远多于此演示所使用的文件。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，了解
查看下载文件的描述和有关创建新项目的信息。

适用于 IAR RL78 项目的 Renesas Embedded Workbench 工作区称为
RTOSDemo.eww，位于 FreeRTOS/Demo/RL78_multiple_IAR
目录中。

---

### 演示应用程序

### 演示应用程序硬件设置

演示应用程序所使用的 LED 直接安装在各个
受支持的硬件平台上，无需进行硬件设置。

### 功能

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。如果
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将调用 main_blinky()，
这会创建一个简单的 "'blinky" 样式的演示。如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
设置为 0，则 main() 将调用 main_full()，这会创建一个更全面的
演示。

### 
 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

main_blinky() 会在启动 RTOS 调度器之前创建一个队列和两项任务。

* **队列发送任务：**

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数
 实现。

 prvQueueSendTask() 处于一个循环中，
 因此在将值 100 发送到
 在 main_blinky() 中创建的队列之前，该任务会被反复阻塞 200 毫秒。此数值发送之后，任务就会重新循环，
 再次被阻塞 200 毫秒，依此类推。
* **队列接收任务：**

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 。

 prvQueueReceiveTask() 处于一个循环中，
 会反复阻塞试图从队列中读取数据的操作，该队列创建于 main_blinky() 中，
 每次收到值 100 时就会切换一次 LED。

 只有当队列发送任务写入队列时，
 队列接收任务才会离开阻塞状态。由于队列发送任务每 200 毫秒向队列写入一次，
 队列接收任务每 200 毫秒离开一次阻塞状态，
 切换一次 LED。

### 
 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

main_full() 会创建 13 项任务、4 个队列和 2 个软件定时器。许多
任务来自与所有 RTOS 演示一起使用的一组标准演示任务，
并记录在 FreeRTOS.org 网站上。

除标准演示任务外，还创建了以下任务和定时器：

- **"Reg test" （寄存器测试）任务：**

 这些任务使用已知值填充寄存器，然后检查
 每个寄存器是否仍包含其预期值。每项任务使用
 一组不同的值。寄存器测试任务以非常低的优先级执行，
 因此经常被抢占。如果寄存器中包含意外值，
 则表示上下文切换机制中存在错误。

- **“演示”软件定时器和回调函数：**

 演示软件定时器回调函数的唯一作用是递增变量。
 演示定时器的周期相对于检查定时器的周期进行设置
 （详见下文）。因此，检查定时器非常清楚
 在每次执行检查定时器回调函数之间
 演示定时器回调函数应该执行的次数。演示定时器回调函数中递增的变量
 可用于确定回调函数
 执行的次数。

- **“检查”软件定时器和回调函数：**

 检查软件定时器周期最初设置为 3 秒。检查定时器
 回调函数会检查所有标准演示任务、寄存器测试
 任务和演示定时器是否仍在执行，且执行时
 是否报告任何错误。如果检查定时器发现某项任务
 定时器已停顿，或报告了错误，则会自行将周期
 从最初的 3 秒更改为仅 200 毫秒。

 检查定时器回调函数
 每次被调用时，都会切换 LED。这可直观体现
 系统状态指示：如果 LED 每三秒切换一次，
 则表示未发现任何问题。如果 LED 每 200 毫秒切换一次，
 则表明至少在一项任务中发现问题。

### 构建演示应用程序

1. 打开 FreeRTOS/Demo/RL78_multiple_IAR/RTOSDemo.eww 工作区
 （位于 IAR Embedded Workbench IDE 中）。
2. （在打开的项目中）使用工作区窗口顶部的下拉菜单
 选择适合所使用的目标硬件的构建配置
 。
3. 按 F7 构建项目。构建项目时，
 不应报错或出现警告（使用远端内存模型时）。

### 对微控制器进行编程和调试

1. 确保目标板以合适方式连接到主机。
 一些开发平台内置 J-Link 接口，
 只需要一根 USB 线缆即可。其他平台则需要
 [Renesas E1 调试接口](http://www.renesas.eu/products/tools/emulation_debugging/onchip_debuggers/e1/index.jsp)。
2. 从 Embedded Workbench 的 "Project" 菜单中选择 "Download and Debug"。
 IAR 可能会提示您配置调试器接口，
 在此之后，对闪存进行编程时会出现短暂延迟，
 再接着调试器进入 main() 函数时会出现中断。

---

### 配置和使用详情

### RTOS 移植专用配置

此演示的相关配置项目位于
[FreeRTOS/Demo/RL78_multiple_IAR/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization)中。您可以根据应用程序的需求，
编辑本文件中定义的常量。

各移植将 "BaseType_t" 定义为
对处理器而言最有效的数据类型。此移植将 BaseType_t 定义为短整型。

请注意，vPortEndScheduler() 尚未实现。

### 内存模型

FreeRTOS 移植将在近端和远端内存模型之间自动切换，
具体取决于 IAR 项目选项中的设置。我们已使用两种内存模型组合对该移植进行了测试，
分别是：

1. 都设置为近端的数据和代码模型。
2. 都设置为远端的数据和代码模型。

### 编写中断服务程序

无法切换上下文的中断服务程序无特殊要求，
可根据 IAR 编译器文档编写。

通常情况下，上下文切换需要中断服务程序。
例如，正在接收的串行端口字符可以解除对高优先级任务（在阻塞状态下等待该字符到达）的阻塞
。如果已解除阻塞任务的
优先级高于当前任务
（被 ISR 中断的任务），则 ISR 应直接返回
至已解除阻塞的任务。要使用 IAR 工具，
则必须使用汇编文件包装器输入此类中断服务程序。请参阅
如下示例，另一示例在 main.c 中提供。首先是
汇编文件包装器。

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

 ; Ensure the vector table segment is used. 
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

### RTOS 内核使用的资源

默认情况下，RTOS 内核使用间隔定时器生成 RTOS 滴答 (Tick)。
应用程序编写者可以定义 configSETUP_TICK_INTRUP()
（位于 FreeRTOSConfig.h 中) ，以便使用自己的 Tick 中断配置
代替默认值。例如，如果应用程序写入器
创建了一个名为 MyTimerSetup() 的函数，该函数配置了一个备用定时器，
以按所需频率生成中断，则将以下代码添加到 FreeRTOSConfig.h 中
会导致调用 MyTimerSetup() 以代替默认定时器配置：

```c

#define configSETUP_TICK_INTERRUPT() MyTimerSetup()

```

**注意：**无论使用哪种中断
生成 RTOS Tick，都必须将 vPortTickISR() 安装为处理程序。

RTOS 内核还需要独占使用 BRK 软件中断指令。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

演示应用程序项目中包含 SourcePortableMemMangheap_1.c，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
