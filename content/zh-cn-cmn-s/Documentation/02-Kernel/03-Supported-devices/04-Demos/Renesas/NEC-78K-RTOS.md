---
title: "使用 IAR 编译器的 NEC 78K0R RTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR 编译器](https://www.iar.com/products/iar-embedded-workbench-for-renesas-78k)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/NEC-78K0R-Kx3-Target-Board.jpg)  

本页展示了 NEC 78K0R 16 位微控制器的 FreeRTOS 演示。 
注：自此页面编写以来， NEC 已与 Renesas 合并，
本页的链接已相应更新。

演示项目包含 
[78K0R/KG3](http://www2.renesas.com/micro/en/promotion/78k0r/kx3/index.html) 和 78K0R/KE3L 目标板配置。A
[MINICUBE2](http://www.renesas.com/minicube2)
用于 IAR 嵌入式工作台和目标板之间的接口。MINICUBE2 既可用于闪存编程，又可用于
调试。

通过在目标板上包含微控制器本身以及必要的复位、时钟、电源和调试电路（该电路将 
所有微控制器引脚路由到沿 PCB 边缘的连接器安装点），78K0R 目标板可用于轻松评估微控制器。

**注意：**如果项目构建失败，则可能是使用的 IAR
嵌入式工作台版本过低。如果构建失败， 
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。

---

### 重要提示！NEC 78K0R RTOS 移植使用注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，了解
下载文件的描述和有关创建新项目的信息。

NEC 78K0R 演示的 IAR Embedded Workbench 工作区名为 RTOSDemo.eww，位于
FreeRTOS/Demo/NEC_78K0R_IAR 目录中。 

---

### 演示应用程序

### 演示应用程序硬件设置

演示应用程序使用直接安装在目标板上的两个 LED 和按钮，
因此无需进行硬件设置。

该按钮用于在 INTP0 上生成中断。

### 功能

本节介绍 78K0R/KG3 演示的功能。78K0R/KE3L 演示创建的任务较少，因此占用的 RAM 较少。

演示项目在启动 RTOS 调度程序之前会创建 22 个任务。这些任务大多数是“标准演示”任务，目的
是演示 RTOS API 和测试 RTOS 移植。这些任务内部并不执行任何实质性的功能。

除了标准演示任务外，还创建了以下特定演示任务：

* **寄存器测试任务**
 创建了两个寄存器测试任务。这些任务用已知值填充微控制器寄存器， 
 然后不断检查每个寄存器是否仍包含其预期值 
 （每个任务使用不同的值）。任务的优先级很低， 
 因此会被定期抢占。寄存器测试任务
 在其中一个寄存器中发现意外值表明抢占上下文切换机制中
 存在错误。
* **按钮推送任务和 ISR**
 大多数 FreeRTOS 演示使用串行
 端口环回 'com test' 在中断内切换上下文。78K0R 目标板不包括 RS232 端口，
 因此使用直接安装在目标板上的按钮生成的中断
 来演示从中断内部切换的上下文。 

 按钮推送 ISR 和相应的任务都非常基本。每次按下按钮时，
 ISR 只需每次“给出”信号量任务只是在信号量上阻塞，
 然后在每次 ISR 给出信号量时切换 LED，有效地将任务与中断同步。
* **检查任务**
 检查任务用于提供系统状态的可见反馈。该任务 
 每三秒钟才执行一次，但由于优先级高，因此可以保证获得处理时间。 
 每次执行时，该任务都会检查系统中其他所有任务的状态，查看
 是否有任务报告了错误。检查任务将每三秒钟切换一次 LED 状态，
 前提是其他所有任务都按预期运行。如果在任何任务发现了错误，
 LED 状态切换速率将更改为 500 毫秒切换一次。

正确执行时，演示设置如下： 

* LED1 (P76) 每 3 秒钟切换一次。
* 每次按下按钮（SW1，INTP0）时，LED2 (P77) 切换。

更多信息请参阅源代码相关注释。

### 构建演示应用程序

1. 在 IAR Embedded Workbench IDE 中打开 FreeRTOS/Demo/NEC_78K0R_IARRTOS/Demo.eww 工作区。
2. 选择与正在使用的目标板匹配的配置，如下图所示。

![](/media/2018/NEC-78K-RTOS-SelectConfiguration.jpg)  

为正在使用的目标板选择配置。
3. **重要提示！**确保 FreeRTOSConfig.h 中的 configMEMORY_MODE 设置与 IAR 项目选项中的设置匹配。
 如果编译器选项设置为使用“近端”代码模型和“近端”数据模型，
 则 CONFIGDATA_MODE 必须设置为 0。如果编译器选项设置为使用“远端”代码模型和“远端”数据模型，
 则 configMEMORY_MODE 必须设置为 1。这些是唯一经过测试的设置组合。
4. 按 F7 后不出现错误或警告，则项目构建成功。

### 对微控制器进行编程和调试

1. 确保 MINICUBE2 开关正确设置在 "M1" 和 "3" 位置。
2. 将 MINICUBE2 连接到目标主板和主机计算机之间。
3. 从 Embedded Workbench 的 "Project" 菜单中选择 "Download and Debug"。闪存被编程时会有短暂延迟，
 之后调试器会在进入 main() 函数时中断。

---

### 配置和使用详情

### RTOS 移植特定配置

此演示的特定配置项目位于 [FreeRTOS/Demo/NEC_78K0R_IAR/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中。根据 
应用程序的需要，编辑本文件中定义的常量。

NEC 78K0R 移植和演示有两个特定的常量：

* **configMEMORY_MODE**
 必须将此设置为与所选编译器选项匹配。如果编译器选项设置为使用“近端”代码模型和“近端”数据模型，
 则 CONFIGDATA_MODE 必须设置为 0。如果编译器选项设置为使用“远端”代码模型和“远端”数据模型，
 则 configMEMORY_MODE 必须设置为 1。这些是唯一经过测试的设置组合。
* **configCLOCK_SOURCE**
 将 configCLOCK_SOURCE 设置为 0 以使用外部时钟源，或设置为 1 以使用高速内部时钟源（通常为 8MHz）。
 更改任何时钟配置时，请确保 configCPU_CLOCK_HZ 设置正确。

每个移植 #defines 'BaseType_t 等于该处理器的最有效数据类型。本端口将
BaseType_t 定义为短整型。

请注意，vPortEndScheduler() 尚未实现。

### 编写中断服务程序

不会引起上下文切换的中断服务程序没有特殊要求，可以按照
IAR 编译器文档中的描述编写。

通常，上下文切换需要中断服务程序。例如，一个正在接收的串行端口字符可对高优先级任务解除阻塞， 
因为该任务正在等待该字符的到来。如果已解除阻塞的任务的优先级高于当前任务，
则 ISR 应直接返回 
至已解除阻塞的任务。由于 IAR 内联汇编器的限制，此类中断服务程序必须使用 
汇编文件包装器。此演示包含简单的按钮按下中断，以演示该机制。示例
已复制到下方：

首先是汇编文件包装器。

---

```c

; ISR_Support.h defines the portSAVE_CONTEXT and portRESTORE_CONTEXT 
; macros.
#include "ISR_Support.h"

 PUBLIC vButtonISRWrapper
 EXTERN vButtonISRHandler

 RSEG CODE:CODE

; The wrapper is the interrupt entry point.
vButtonISRWrapper:

 ; The ISR must start with a call to the portSAVE_CONTEXT() macro to save 
 ; the context of the currently running task.
 portSAVE_CONTEXT

 ; Once the context is saved the C portion of the handler can be called.
 ; This is where the interrupting peripheral is actually serviced.
 call vButtonISRHandler

 ; Finally the ISR must end with a call to portRESTORE_CONTEXT() followed by
 ; a reti instruction to return from the interrupt to whichever task is 
 ; now the task selected to run (which may be different to the task that 
 ; was running before the interrupt started).
 portRESTORE_CONTEXT
 reti

```

---

用于中断处理程序的示例汇编文件包装器。

中断处理程序的 C 部分只是一个标准 C 函数。

---

```c

/* This standard C function is called from the assembly wrapper above. */
void vButtonISRHandler( void )
{
short sHigherPriorityTaskWoken = pdFALSE;

 /* The code in this handler is just a copy of the button push interrupt code
 for demonstration only. */

 /* 'Give' the semaphore to unblock the button task. */
 xSemaphoreGiveFromISR( xButtonSemaphore, &sHigherPriorityTaskWoken );

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

RTOS 内核使用 TAU 的通道 5 来生成 RTOS 滴答。位于
FreeRTOSSourceportableIAR78K0Rport.c 中的 prvSetupTimerInterrupts() 可以更改为使用任何方便的定时器源。

RTOS 内核还需要独占使用 BRK 软件中断指令。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

演示应用程序项目中包含 SourcePortableMemMangheap_1.c， 
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分， 
获取完整信息。
