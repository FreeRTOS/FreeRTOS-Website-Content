---
title: "NEC V850ES RTOS 移植 使用 IAR 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR 编译器](https://www.iar.com/products/architectures/renesas/iar-embedded-workbench-for-renesas-rh850/)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/NEC-V850ES-Target-Board.jpg)  

本页介绍的 FreeRTOS 演示适用于 NEC V850ES 32 位微控制器。 

演示项目中包含的配置适用于以下设备：

* [V850ES/Fx3](http://www2.renesas.com/micro/en/promotion/v850/fx3.html) 应用板
* V850ES/Jx3 目标板
* V850ES/Jx3L 目标板
* V850ES/Jx2 目标板
* V850ES/Hx2 目标板

V850ES/Fx3 项目可配置使用 
[MINICUBE](http://www2.renesas.com/micro/en/development/tool-details.php?tool=QB-V850MINI) 
进行闪存编程并作为调试接口。所有其他项目都配置为使用 
[MINICUBE2](http://www.renesas.com/minicube2)。

V850ES/Fx3 应用板包括多种用于串行接口的线路驱动器，以及有限数量的
按钮输入和 LED 输出。

V850ES 目标板包含微控制器以及必要的复位、时钟、电源和调试电路，能够将 
所有微控制器引脚转接到 PCB 边缘的连接器安装点，有助于轻松评估微控制器。目标板
本身的 IO 功能非常有限。 

**注意：**如果项目构建失败，很可能是使用的 IAR
Embedded Workbench 版本过低。如果是这种情况， 
则项目文件也很可能（在无提示的情况下）已经损坏，
即使已更新 IAR 版本，也需要将项目文件恢复到初始状态，才能构建项目。

---

### 重要！NEC V850 RTOS 移植使用注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
下载文件的描述和有关创建新项目的信息。

NEC V850ES 演示的 IAR Embedded Workbench 工作区名为 RTOSDemo.eww，位于
FreeRTOS/Demo/NEC_V850ES_IAR 目录中。 

---

### 演示应用程序

#### 演示应用程序硬件设置 — 应用板（V850ES/Fx3 移植）

需要连接线将应用板 LED 连接到微控制器输出。连接线如本页顶部的图片中所示。 
需建立如下连接：

|  |  |  |
| --- | --- | --- |
| **连接器 CN24 上的引脚** |  | **连接器 CN50/CN51 上的引脚** |
| 1 | **连接到** | CN51 pin 2 |
| 3 | **连接到** | CN51 pin 4 |
| 5 | **连接到** | CN50 pin 2 |
| 7 | **连接到** | CN50 pin 4 |

将应用板 LED 连接到微控制器输出端

演示应用程序包括中断驱动的 UART 测试，其中一个任务传送字符， 
随后另一个任务接收此类字符。为正确操作此功能，必须将环回连接器安装到 CN 63 上的下部 9 路插头
（9 路连接器上的引脚 2 和 3 必须连接在一起）。此外，必须使用跳线将 CN63 低压插头连接到微控制器，
如《应用板用户手册》（NEC 文档编号 EASE-UM-0019-2.1）中所述。

#### 演示应用程序硬件设置 — 目标板（所有其他移植）

演示应用程序使用直接安装在目标板上的两个 LED，
因此无需额外的硬件设置。

#### 功能

本节介绍在 V850ES/Fx3 应用板上运行的完整演示的功能。目标板没有
完整演示所需的 IO 接口或内存，因此仅执行所述任务的子集。

在启动 RTOS 调度器之前，完整演示项目会创建 32 个任务。这些任务大多数是“标准演示”任务，目的
是演示 RTOS API 和测试 RTOS 移植。这些任务内部并不执行任何实质性的功能。

除标准演示任务之外，演示还会创建两个“寄存器测试”任务。这些任务用已知值填充微控制器寄存器， 
然后不断检查每个寄存器是否仍包含其预期值 
（每个任务使用不同的值）。任务的优先级很低， 
因此会被定期抢占。寄存器测试任务
在其中一个寄存器中发现意外值表明抢占上下文切换机制中
存在错误。

最后， “检查”任务用于提供系统状态的可见反馈。该任务 
每三秒钟才执行一次，但由于优先级高，因此可以保证获得处理时间。 
每次执行时，该任务都会检查系统中其他所有任务的状态，查看
是否有任务报告了错误。检查任务将每三秒钟切换一次 LED 状态，
前提是其他所有任务都按预期运行。如果在任何任务发现了错误，
LED 状态切换速率将更改为 500 毫秒切换一次。

如果正确执行，该演示将实现以下效果： 

* LD3 到 D5 由标准“闪烁”任务控制。每个 LED 由不同的任务切换。LED 将以固定频率切换， 
 每个 LED 使用不同的频率。
* LED D2 由“检查”任务控制。如果系统中的所有其他任务继续按预期运行
 并且从不报告任何错误，则该 LED 将每 3 秒切换一次。这项机制可以
 通过从 CN63 中移除环回连接器来进行测试，这样做会故意导致
 串行端口任务标记错误。

更多信息请参阅源代码相关注释。

#### 构建演示应用程序

1. 在 IAR Embedded Workbench IDE 中打开 FreeRTOS/Demo/NEC_V850ES_IAR/RTOSDemo.eww 工作区。
2. 选择与正在使用的应用板或目标板匹配的配置，如下图所示。

![](/media/2018/Selecting-the-V850-configuration.jpg)  

为正在使用的应用板或目标板选择配置。
3. **重要！**确保 FreeRTOSConfig.h 中的 configDATA_MODE 设置与编译器项目选项匹配。 
 如果编译器选项设置为使用小型或大型内存模型，则 configDATA_MODE 必须设置为 0。 
 如果编译器选项设置为使用微小数据模型，则 configDATA_MODE 必须设置为 1。
4. 按 F7 后不出现错误或警告，则项目构建成功。

#### 对微控制器进行编程和调试

1. 如果使用 MinICUBE2：
	* 使用 V850ES/HG2 目标板时，请确保 MINICUBE2 开关设置为 "M2" 和 "M5"。
	* 对于所有其他目标板， MINICUBE2 开关设置为 "M2" 和 "M3"。
2. 将 MINICUBE 或 MINICUBE2 连接到目标主板和主机计算机之间。
3. 从 Embedded Workbench 的 "Project" 菜单中选择 "Download and Debug"。闪存被编程时会有短暂延迟，
 之后调试器会在进入 main() 函数时中断。

---

### 配置和使用详情

#### RTOS 移植专用配置

此演示的特定配置项位于 [FreeRTOS/Demo/NEC_V850ES_IAR/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中。可根据 
应用程序的需要，编辑本文件中定义的常量。

ConfigDATA_MODE 配置常量特定于 V850ES 移植。如果编译器选项设置为使用小或大内存模型，
则 configDATA_MODE 必须设置为 0。 如果编译器选项设置为使用微小数据模型，则 configDATA_MODE 必须设置为
1。

每个移植 #defines 'BaseType_t' 等于该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，尚未实现 vPortEndScheduler ()。

#### 编写中断服务程序

不会引起上下文切换的中断服务程序没有特殊要求，可以按照
IAR 编译器文档中的描述编写。

通常，上下文切换需要中断服务程序。例如，一个正在接收的串行端口字符可对高优先级任务解除阻塞， 
因为该任务正在等待该字符的到来。如果已解除阻塞的任务的优先级高于当前任务，
则 ISR 应直接返回 
至已解除阻塞的任务。由于 IAR 内联汇编器的限制，此类中断服务程序必须使用 
汇编文件包装器。本演示包含 UART 驱动程序，用于演示该机制。接收处理程序
已复制到下方。

首先是汇编文件包装器。

---

```c

; ISR_Support.h defines the portSAVE_CONTEXT and portRESTORE_CONTEXT 
; macros.
#include "ISR_Support.h"

 PUBLIC vUARTRxISRWrapper
 EXTERN vUARTRxISRHandler

 RSEG CODE:CODE

; The wrapper is the interrupt entry point.
vUARTRxISRWrapper:

 ; The ISR must start with a call to the portSAVE_CONTEXT() macro to save 
 ; the context of the currently running task.
 portSAVE_CONTEXT

 ; Once the context is saved the C portion of the handler can be called.
 ; This is where the interrupting peripheral is actually serviced.
 jarl vUARTRxISRHandler, lp

 ; Finally the ISR must end with a call to portRESTORE_CONTEXT() to restore
 ; the context of which ever task is selected to run - which may be
 ; different to the task that was running before the interrupt started. 
 portRESTORE_CONTEXT

```

---

用于中断处理程序的示例汇编文件包装器。

中断处理程序的 C 部分只是一个标准 C 函数。

---

```c

/* This standard C function is called from the assembly wrapper above. */
void vUARTRxISRHandler( void )
{
char cChar;
long lHigherPriorityTaskWoken = pdFALSE;

 /* Send the received character to the Rx queue. */
 cChar = UD0RX;
 xQueueSendFromISR( xRxedChars, &cChar, &lHigherPriorityTaskWoken );

 /* If sending a character to the Rx queue caused a task to unblock, and
 the unblocked task has a priority higher than the currently running task,
 then lHigherPriorityTaskWoken will have been set to true and a context
 switch should occur now. */
 portYIELD_FROM_ISR( lHigherPriorityTaskWoken ); 
}

```

---

示例中断处理程序的 C 部分。

#### RTOS 内核使用的资源

RTOS 内核使用 TM0 生成 RTOS 滴答。函数 prvSetupTimerInterrupts() 在
FreeRTOSSourceportableIARV850ESport.c 可以修改为使用任何方便的定时器源。

RTOS 内核还需要独占使用 TRAP 0 指令。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

SourcePortableMemMangheap_2.c 包含在演示应用程序中，以提供 
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分， 
获取完整信息。
