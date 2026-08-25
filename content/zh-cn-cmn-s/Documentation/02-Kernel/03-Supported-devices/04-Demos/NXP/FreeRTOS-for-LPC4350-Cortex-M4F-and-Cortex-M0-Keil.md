---
title: "NXP LPC43xx ARM Cortex-M4F 演示 使用 Keil MDK 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![NXP LPC4300 系列微控制器](/media/2018/NXP-LPC4300-Hitex-Development-Board.jpg)

本页记录的 FreeRTOS ARM Cortex-M4F 演示应用程序面向 NXP
[LPC43xx 微控制器](http://ics.nxp.com/products/lpc4000/lpc43xx/)。
提供的 Keil 项目预配置为可在 Hitex 的 LPC4350 开发板上
运行。LPC4350 演示项目将在未来几周内更新，
更新后也将支持 LPC4350 的基于 ARM Cortex-M0 的协处理器。

演示将 LPC4350 配置为以 204MHz 运行。请参阅下文“RTOS
配置和使用详情”部分的说明。

FreeRTOS ARM CORTEX-M4F 移植支持完整的中断嵌套模型，从不
完全禁用中断。仅当
在用于构建源文件的项目编译时间选项中打开硬件浮点支持时
才能使用此移植。不包含浮点单元的 ARM Cortex-M4 设备
不应使用此移植，而应使用 FreeRTOS ARM Cortex-M3 移植层。

请注意，需要 Keil MDK 4.2.2 或更高版本以确保 no_allow_fpreg_for_nonfpdata 编译器
选项可用。

---

### *重要！使用 FreeRTOS Keil LPC4300 演示项目的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#nxp-lpc4350演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS zip 下载文件中包含所有 FreeRTOS 移植
以及每个演示应用程序项目的源代码。
因此，该下载包含的文件远多于构建和运行 NXP LPC4350 演示所需的文件。请参阅
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
获取对已下载文件的描述以及关于创建新项目的信息。

LPC4350 上的 ARM Cortex-M4F 核心的 Keil MDK 演示项目称为 M4.uvproj，
位于 FreeRTOS/Demo/CORTEX_M4F_M0_LPC43xx_Keil/M4 目录中，
该目录位于官方 FreeRTOS .zip 文件下载中。FreeRTOS/Demo/CORTEX_M4F_M0_LPC43xx_Keil/M0
目录当前为空，并作为占位符，为不久的将来增加
对 LPC4350 协处理器核心的支持做准备。

---

### NXP LPC4350演示应用程序

#### 功能

此演示应用程序会演示以下几个方面：

* 浮点上下文切换。
* Malloc 失败、堆栈溢出、滴答和空闲[钩子函数](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。

可对演示应用程序进行配置，使其提供非常简单的 "blinky" 样式的演示，
或者提供
FreeRTOS 功能的完整全面测试和演示。配置构建的由常量
\#define mainCREATE_SIMPLE_LED_FLASHER_DEMO_ONLY 控制，该常量
在 main.c 中定义。

演示应用程序任务分为标准演示任务
和演示特定任务。所有 FreeRTOS 移植和演示应用程序都使用标准演示任务。
这些任务仅用于演示 FreeRTOS API 和测试移植，没有其他用途。

|  |  |
| --- | --- |
| <br />**mainCREATE_SIMPLE_LED_FLASHER_DEMO_ONLY 设置**<br /> | <br />**描述**<br /> |
| <br /> 设置为 1<br />  | <br /> 这将创建一个**非常简单的示例**，<br /> 该示例创建三个标准的演示“闪烁”任务。每个任务以固定但不同的频率<br /> 切换 LED，分别使用 LED3、LED2 和 LED1<br /> 。<br /> <br /> |
| <br /> 设置为 0<br />  | <br /> 这将创建一个非常全面的演示，会创建 46 个任务，<br /> 之后启动 RTOS 调度器。随后在应用程序执行过程中，<br /> 它会持续创建和删除另外两个任务。<br /> <br /> 此演示包含大量队列、一个软件定时器和各种类型的信号量。<br /> 任务主要由<br /> [标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务组成。<br /> <br /> 还创建了特定于应用程序的“寄存器测试”任务。<br /> 这些任务首先将所有通用寄存器和浮点寄存器填充为已知值<br /> 。然后，任务会重复检查<br /> 每个寄存器是否在任务的生命周期内保持写入的值<br /> 。这些任务按空闲优先级运行，因此经常会退出并重新进入<br /> 运行状态。两个寄存器检查<br /> 任务使用不同的值，如果寄存器包含意外值，<br /> 则表明上下文切换<br /> 机制中存在错误。<br /> <br /> 创建了一个“检查”软件定时器，用于定期检查标准<br /> 演示任务和寄存器测试任务，以确保所有任务<br /> 都按预期运行。**检查软件定时器的<br />回调函数切换 LED0。这可为系统运行状况提供直观反馈。<br /> 如果 LED0 每 3 秒钟切换一次，则表示<br />检查软件定时器未发现任何问题。如果 LED0<br />每 200 毫秒切换一次，则表示检查软件定时器<br />在一个或多个任务中发现问题。**<br /><br /> 与简单的闪烁演示一样，<br /> 全面演示也创建了标准演示闪烁任务，这些任务以固定但不同的频率<br /> 切换 LED3、LED2 和 LED1。<br />  |

#### 硬件设置

演示使用的是直接焊接到 Hitex 印刷电路板上的 LED，
因此不需要进行硬件设置。

#### 构建和执行演示应用程序

1. 确保已使用合适接口将目标硬件
 连接到主机。该项目已经过 ULINK2 和 ULINK ME 的测试。
2. 从 Keil IDE 中打开 [M4.uvproj](#源代码组织) Keil 项目
 。
3. 在 IDE 的 "Project" 菜单中选择 "Build" 或直接按 F7。此项目
 应该在没有任何错误或警告的情况下构建。
4. 构建完成后，从 IDE 的 "Debug" 菜单中选择 "Start/Stop Debug Session"
 （或直接按 CTRL+F5），即可对微控制器闪存进行编程，
 然后启动调试会话。执行将在进入 main() 函数时
 中断。

---

### RTOS 配置和使用详情

#### Cortex-M4F FreeRTOS 移植特定配置

此演示的相关配置项位于 FreeRTOS/Demo/CORTEX_M4F_M0_LPC43xx_Keil/M4/FreeRTOSConfig.h 中。
[可以编辑此文件中定义的常量，以适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ** 

 此常量可用于设置 RTOS 滴答中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY** 

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY** 

 尽管 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的 8 位偏移值，定义为原始数据，直接用于
 ARM Cortex-M4F NVIC 寄存器中，configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 是完全等效物，定义为仅使用 LPC4300 上可用的 5 个优先级位。
 CMSIS 库函数 NVIC_SetPriority() 需要未移动的 5 位格式。

请注意！请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值），
因为这实际上可能会导致该中断在系统中具有最高优先级，
因此，如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

ARM Cortex-M 核心上的最低优先级实际上是 255，但不同
Cortex-M 供应商会实现不同数量的优先级位，
提供期望以不同方式指定优先级的库函数。例如，
LPC ARM Cortex-M 微控制器上可以指定的最低优先级实际上为 31——这是由
FreeRTOSConfig.h 中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。

我们还建议确保将所有五个优先级位指定为
抢占式优先级位，并且不设置子优先级位，就和所提供的演示
中的一样。

每个移植都会将 'BaseType_t' 定义为对该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长整型。

#### 核心时钟配置

演示让 LPC4350 时钟以 204MHz 运行。要做到这一点，函数就必须
将并行闪存控制器配置为
在 RAM 不足时执行。这些函数的映射在链接器脚本（散点文件）中执行，
且 Hitex_fast_startup.c 中包含使核心时钟升至 204MHz 的代码。

#### 中断服务程序

与大多数移植不同，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

下列源代码片段仅作为示例提供。中断
使用信号量与任务（未显示）同步，并调用 portEND_SWITCHING_ISR
以确保中断直接返回到任务。

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
 portEND_SWITCHING_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND_SWITCHING_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}

```

只有以 "FromISR" 结尾的 FreeRTOS API 函数才能
中断服务程序中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY 配置常量设置的
优先级。

#### FreeRTOS 使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

#### 在抢占式和协同式 RTOS 内核之间切换

将 RTOSDemo/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式内核；
设置为 0，可使用协同式内核。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ARM Cortex-M4F 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。
