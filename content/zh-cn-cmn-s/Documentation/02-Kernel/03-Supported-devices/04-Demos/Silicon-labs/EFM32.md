---
title: "使用 IAR 开发工具的 FreeRTOS EFM32 演示"
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
| <br /><br /><br />![](/media/2018/EFM32.jpg) Silicon Labs Gecko 开发套件<br /><br /> |

**注意：**
本页记录了 EFM32 演示的原始版本（旧版本）。[现已推出包括低功耗无滴答操作演示的更新演示](EFM32-Giant-Gecko-Pearl-Gecko-tickless-RTOS-demo)。

本页面展示了基于 ARM Cortex-M3 的 [Silicon Labs](http://www.silabs.com/) EFM32 微控制器的第一个 FreeRTOS 演示。

EFM32 提供了 EM1 至 EM4 四种节能模式，其中 EM4 提供了最大节能效果。但本页面演示使用标准的 FreeRTOS
ARM Cortex-M3 移植。因此，RTOS 内核本身并不利用这些节能模式。相反，演示代码
（非 RTOS 内核代码）中添加了一些基本的节能功能，但这意味着只能演示 EM1。使用任何其他模式
均会导致滴答中断停止。有关使用 EM2 和 EM3 的其他演示的链接，请参阅[主要 Silicon Labs 列表](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#SILICONLABS)。

开发套件
配备 [EFM32G890F128](http://www.silabs.com/products/mcu/32-bit/efm32-gecko/pages/efm32g890f128-bga112.aspx) 微控制器，
该微控制器具有 128KB 闪存和 16KB 的 RAM。

演示使用：

* FreeRTOS IAR ARM Cortex-M3 移植。
* [适用于 ARM 的 IAR 嵌入式工作台](http://www.iar.com/ewarm)。

FreeRTOS ARM Cortex-M3 移植包括一个完全中断嵌套模型。必须按照
[自定义页面说明](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，设置中断优先级才能正确操作。

---

### *重要！使用 EFM32 ARM Cortex-M3 演示的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

EFM32G890F128 演示的 IAR 嵌入式工作台的工作区称为 RTOSDemo.eww，位于 FreeRTOS/Demo/CORTEX_EFMG890F128_IAR 目录。
请注意，该项目同时包含调试和释放配置，但仅对调试配置进行了配置。

下载的 FreeRTOS zip 文件包含所有移植文件和演示应用程序项目文件。因此，它包含的文件
远超此演示所用的文件。请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
获取下载文件的介绍以及有关创建新项目的信息。

---

### 演示应用程序

#### 构建和执行演示应用程序

1. 在嵌入式工作台 IDE 中打开 FreeRTOS/Demo/CORTEX_EFMG890F128_IAR/RTOSDemo.eww。
2. 确保已选择调试配置。

![](/media/2018/EFM32_IAR.jpg)
选择调试配置
3. 将开发套件连接到主机。可以通过以下任一方式完成：

	* 使用标准 USB 电缆直接将主机连接至开发套件，或
	* 使用 J-Link USB JTAG 接口。选择此选项时，还需要外部 5V 电源，
	 并且开发套件上的 JTAG 连接器的方向必须设置为 "IN"（后一项
	 设置是使用开发套件的 "CFG->Debug Control" 菜单选项实现的，
	 使用的是开发硬件本身而非在 IAR IDE 中的按钮和操纵杆）。
4. 从 "Project" 菜单中选择 "Download and Debug"，在编程至 EFM32 闪存之前，
 演示应用程序应成功架构，无错误或警告。调试器会在 main() 开始时中断。

#### 演示任务

main() 在启动RTOS调度程序之前创建 19 个任务。任务内容主要包括
标准演示任务（参见[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
部分，了解各个任务的详细信息）。各项任务的存在旨在示明如何使用 FreeRTOS API ，并
仅对 FreeRTOS 移植进行测试，但不包含应用程序特定的有用功能。

除了标准演示任务外，还创建了以下任务和测试：

* 检查任务
 检查任务包括提供系统状态的视觉反馈。
 检查任务会定时查询所有标准演示任务，之后再切换用户 LED
 0. 如果用户 LED 0 每五秒切换一次，则检查任务
 未发现任何错误。如果切换速率提升至每 200 毫秒，则
 已在至少一个任务中发现错误。

 每 5 秒中，检查任务就有 2 秒将微控制器
 置于节能模式 EM1 中。效果在本页[
 后文有述](#节能特性)。
* LCD 测试任务
 LCD 任务向 LCD 显示屏写入一系列
 不断重复的模式。由于检查任务将微控制器置于节能模式，
 因此，该模式将每五秒暂停两次。
* LED 测试任务
 这是一个极为简单的任务，
 只需依次打开用户 LED 8 到 LED 15，然后再将其关闭。
 由于检查任务将微控制器置于节能模式，
 因此 LED 模式将每五秒暂停两次。

#### 节能特性

如本页顶部所述，此演示使用标准 FreeRTOS
ARM Cortex-M3 移植，因此由演示应用程序执行所有节能功能（此时），
而非由 RTOS 内核。演示应用程序只能
使用节能模式 EM1 - 任何其他模式均会导致滴答中断
停止（请参阅[主要 Silicon Labs 列表](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#SILICONLABS)
了解关于使用 EM2 和 EM3 的其他演示的链接）。

演示应用程序在两个地方使用 EM1：

1. [空闲挂钩中](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)
 空闲任务调用空闲挂钩，只有在无较高优先级任务时
 才会运行（所有较高优先级任务均
 处于[阻塞或挂起状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)）。

 使空闲任务将微控制器置于低能耗状态
 是一种极为简单且几乎是自动式节能方式。但请注意，
 此演示包含共享空闲任务优先级
 且从不进入阻塞状态的任务。如果删除此类任务，
 将为空闲任务提供更多处理时间，从而更加节能（因为微控制器
 将更快更长时间地进入节能模式）。
2. 检查任务中
 检查任务
 是系统中的最高优先级任务。因此，
 当其未处于[阻塞或挂起状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)时，其始终是选择执行的任务。纯粹出于演示原因
 此演示中的检查任务将在其函数每次迭代期间
 循环停留两秒钟：每次
 循环执行检查任务，微控制器都会进入
 节能模式 EM1 - 每次滴答中断发生时
 微控制器将保留 EM1，循环将再次执行。这会降低
 每五秒中的两秒的能耗，
 但也有导致所有其他任务暂停执行整整两秒
 的副作用。可以使用开发套件主板控制器显示屏上的 Advanced Energy Monitor
 图查看实现的节能情况。

---

### RTOS配置和使用详情

#### RTOS 移植特定配置

FreeRTOS/Demo/CORTEX_EFMG890F128_IAR/FreeRTOSConfig.h 包含此演示的特定配置项。可以
本文件中定义的常量，以适配您的应用程序。特别是以下常量：

* **configTICK_RATE_HZ**
 这会设置 RTOS 滴答的频率。
* **configKERNEL_INTERRUPT_PRIORITY and configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，获取有关这些配置常量的完整信息。
 阅读和理解此文档至关重要！

注意：请记住 ARM Cortex-M3 核心使用低数值数字表示高
中断优先级越高，这似乎有悖直觉，而且很容易忘记！如果希望为中断分配低优先级，请勿将中断的
优先级指定为 0（或其他较小数值），因为这可能会导致中断实际上在系统中具有最高优先级，因此，如果该优先级高于
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，会导致系统崩溃。

如果中断服务程序使用 FreeRTOS API 函数，
则**必须**设置中断的优先级。如果将其保留为默认值
将导致最高可能优先级执行中断。

ARM Cortex-M3 核心的最低优先级实际上是 255，但不同的 ARM Cortex-M3 供应商采用了不同数量的优先位，
并提供了期望以不同方式指定优先级的库函数。

每个移植都会使用 #define 将 "BaseType_t" 定义为该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

在演示应用程序中，向量表保存在闪存。

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档编写。
可将宏 END_SWITCHING_ISR () 用于从 ISR 内请求上下文切换。下文提供了中断服务程序
模板示例。示例仅供参考。

请注意，portEND_SWITCHING_ISR() 将使中断保持启用状态。另请注意，
使用 FreeRTOS API 的任何中断优先级（
如以下模板）**必须**设置为等于或低于
confgiMAX_SYSCALL_INTRUPT_PRIORITY。如果中断优先级
低于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则必须在数值上高于
configMAX_SYSCALL_INTRUPT_PRIORITY，因为在 ARM Cortex-M3 上，
优先级数值低表示逻辑上的高中断优先级。

---

```c

/* The interrupt service routine can be written as a standard C function. */
void vAnExampleISR( void )
{
long lTaskWokenByPost = pdFALSE;
unsigned long ulDataValue;

 /* Remember to clear the interrupt source. */
 ....

 /* Assume the interrupting peripheral supplies a value that needs to be
 passed to a task. */
 ulDataValue = ulGetValueFromPeripheral();

 /* In this example, a queue is used to send data to a task. This could
 equally be a counting or other type of semaphore. Note that lTaskWokenByPost
 has already been initialised to pdFALSE. The queue must have already been
 created before this interrupt service routine executes for the first time!. */
 xQueueSendFromISR( xQueue, &ulDataValue, &lTaskWokenByPost );

 /* If sending to the queue caused a task to unblock, and the task that was
 unblocked has a priority equal to or above the currently executing task, then
 lTaskWokenByPost will have been set to pdTRUE. Passing pdTRUE as the
 parameter to portEND_SWITCHING_ISR() will cause a context switch to occur as
 soon as the interrupt completes. */
 portEND_SWITCHING_ISR( lTaskWokenByPost );
}
```

---

中断服务程序模板

#### 在抢占式和协同式 RTOS 内核之间切换

在 FreeRTOS/Demo/CORTEX_EFMG890F128_IAR/FreeRTOSConfig.h 中将定义 configUSE_PREEMPTION 设置为 1 以使用抢占式，或设置为 0
以使用协同式。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

Source/Portable/MemMang/heap_2.c 位于 ARM Cortex-M3 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。

