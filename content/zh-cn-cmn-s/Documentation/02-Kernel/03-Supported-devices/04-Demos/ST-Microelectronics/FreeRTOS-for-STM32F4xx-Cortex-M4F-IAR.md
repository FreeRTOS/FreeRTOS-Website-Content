---
title: "ST STM32F4xx ARM Cortex-M4F 演示使用 IAR EWARM 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ST STM32F4 ARM Cortex-M4F 入门套件](/media/2018/STM32F407ZG-SK.jpg)  
STM32F407ZG_SK 入门套件板

本页记录的 FreeRTOS ARM Cortex-M4F 演示应用程序面向 STMicroelectronics
[STM32F4xx 微控制器](http://www.st.com/internet/mcu/product/252136.jsp)。
本页提供的 IAR 项目预配置为
在 [STM32F407ZG-SK](https://www.iar.com/dev-dynamic-custom-objects/iar-systems-delivers-complete-starter-kit-for-high-performance-stm32f407zg-microcontroller-05b70486) 入门套件中提供的开发板上运行。

FreeRTOS ARM CORTEX-M4F 移植支持完整的中断嵌套模型，从不
完全禁用中断。仅当
在用于构建源文件的项目编译时间选项中打开硬件浮点支持时
才能使用此移植。不包含浮点单元的 ARM Cortex-M4 设备
不应使用此移植，而应使用 FreeRTOS ARM Cortex-M3 移植层。

**注意：**本页上的演示会测试 FreeRTOS 浮点支持，
方法是将使用浮点单元的中断强制嵌套
到三层。嵌套起始于 tick 钩子函数，
该函数从 FreeRTOS tick 中断代码调用。若删除测试的这一部分，
可大大提高 RTOS 内核效率，
在 FreeRTOSConfig.h中将 configUSE_TICK_HOOK 设置为零即可实现。

**注意 2：** 如果项目构建失败，可能是使用的 IAR
Embedded Workbench 版本过低。如果构建失败，
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。

---

### *重要提示！关于使用 FreeRTOS IAR STM32F4 演示项目的说明*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#stmicro-arm-cortex-m4f-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS zip 下载文件中包含所有 FreeRTOS 移植
以及各演示应用程序项目的源代码。
因此，该下载包含的文件远多于构建和运行 ST STM32F407ZG 演示所需的文件。请参阅
[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节详细
了解已下载文件的描述以及关于创建新项目的信息。

适用于 STM32F4xx 演示的 IAR Embedded Workbench 工作区称为 RTOSDemo.eww，
位于 FreeRTOS/Demo/CORTEX_M4F_STM32F407ZG-SK 目录下，
该目录位于官方 FreeRTOS .zip 文件下载中。

---

### STMicro ARM Cortex-M4F 演示应用程序

### 功能

此演示应用程序会演示以下几个方面：

* 从任务中使用浮点指令。
* 从 3 层嵌套的中断中使用浮点指令。
 **注意：**嵌套起始于 tick 钩子函数，
 该函数从 FreeRTOS tick 中断代码调用。若删除测试的这一部分，
 可大大提高 RTOS 内核效率，
 在 FreeRTOSConfig.h中将 configUSE_TICK_HOOK 设置为零即可实现。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* Malloc 失败、堆栈溢出、tick 和空闲[钩子函数](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)。

可对演示应用程序进行配置，使其提供非常简单的 "blinky" 样式的功能，
或者提供
FreeRTOS 功能的完整全面测试和演示。常量 #define mainCREATE_SIMPLE_LED_FLASHER_DEMO_ONLY
定义于 main.c 中，用于在两种模式间切换。

演示应用程序任务分为标准演示任务
和演示特定任务。所有 FreeRTOS 移植和演示应用程序都使用标准演示任务。
这些任务仅用于演示 FreeRTOS API 和测试移植，不得用作其他用途。

|  |  |
| --- | --- |
| <br />**mainCREATE_SIMPLE_LED_FLASHER_DEMO_ONLY 设置**<br /> | <br />**描述**<br /> |
| <br /> 设置为 1<br />  | <br /> 这将创建一个**非常简单的示例**，<br /> 该示例下创建了三个标准的演示“闪烁”任务。这三个任务分别按固定的不同频率触发<br /> LED 的频率固定，但每个 LED 的频率不同。使用 LED STAT1、STAT2 和 STAT3<br /> 。<br /> <br /> |
| <br /> 设置为 0<br />  | <br /> 这是一个非常全面的演示，会创建 46 个任务，<br /> 然后启动 RTOS 调度器，接着会在应用程序执行期间不断地动态创建和<br /> 删除另外两个任务。<br /> <br /> 它会创建大量队列、软件定时器和不同类型的信号量。<br /> 这些任务主要由<br /> [标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务组成。<br /> <br /> 演示包含应用程序特定的“寄存器测试”任务。<br /> 这些是空闲优先级任务，<br /> 首先使用已知值填充所有通用寄存器和浮点寄存器<br /> 。然后，任务反复检查<br /> 寄存器在进入和退出运行状态时，<br /> 写入各寄存器的值在任务生命周期内是否维持不变。两个寄存器检查任务<br /> 使用的已知值不同，如果某个值突然改变，<br /> 说明上下文切换机制中<br /> 存在错误。<br /> <br /> 浮点中断嵌套测试起始于 tick 钩子<br /> 函数。tick 钩子函数是可选应用程序定义的函数，<br /> 可从实时内核 tick 中断调用该函数（此时<br /> 需在 FreeRTOSConfig.h 中将 configUSE_TICK_HOOK 设置为 1。tick<br /> 钩子函数会用已知值填充浮点寄存器，<br /> 然后强制中优先级中断来中断寄存器。中<br /> 优先级中断会用一个不同的值来填充浮点寄存器，<br /> 然后它也会强制高优先级中断去中断寄存器。<br /> 高优先级中断会用另一个值填充浮点寄存器<br /> 。当中断嵌套堆栈展开时，<br /> 首先中优先级中断会检查浮点寄存器<br /> 是否包含写入的值，然后 tick 钩子函数<br /> （最低优先级中断）会检查浮点寄存器<br /> 是否包含写入的值。<br /> <br /> 创建“检查”软件定时器，并开始定期检查标准<br /> 演示任务和寄存器测试任务，以确保全部正常运行，<br /> 且不报错。**检查定时器<br />回调函数会切换 LED STAT4，以提供<br />系统状态的视觉反馈。如果 LED STAT4 每 3 秒钟切换一次，则说明<br />检查软件定时器在执行测试和演示<br />任务时未发现任何问题。如果 LED STAT4 的切换速度增加到每 200 <br />毫秒一次，则说明检查软件定时器至少在一项任务中发现了问题<br />。**<br /><br /> 就像简单的闪光灯演示一样，<br /> 全面的演示会创建标准演示闪烁任务，该任务会<br /> 切换 LED3、LED2 和 LED1 这几个 LED。<br />  |

### 硬件设置

演示使用了内置在入门套件硬件上的 LED，
因此不需要进行硬件设置。

### 构建和执行演示应用程序

1. 确保已使用合适的调试器接口将目标硬件
 连接到主机。入门套件中提供了 J-Link lite。
2. 从 Embedded Workbench IDE 中打开 [RTOSDemo.eww](#源代码组织) Embedded Workbench 工作区
 。
3. 从 Embedded Workbench 的 "Project" 菜单中选择 "Build All"，
 演示应用程序的构建不应出错。
4. 构建完成后，从 Embedded Workbench 的 "Project" 菜单中选择 "Download and Debug"
 （或直接按 CTRL+D），即可对微控制器闪存进行编程，
 然后启动调试会话。应用程序将开始运行，然后
 在函数 main() 的开始处中断。

---

### RTOS 配置和使用详情

### Cortex-M4F FreeRTOS 移植特定配置

此演示的特定配置项位于 FreeRTOS/Demo/cortex_M4F_STM32F407ZG-SK/FreeRTOSConfig.h 中。
[可以编辑此文件中定义的常量，以适合您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ** 

 此常量可用于设置 RTOS 滴答中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY** 

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY** 

 鉴于 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的八位偏移原始值，定义为直接用于 ARM Cortex-M4F NVIC 寄存器，
 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 是等效物，定义为仅使用 STM32 上可用的 4 个优先级位。
 ST 标准外设库函数 NVIC_Init() 以及 CMSIS
 库函数 NVIC_SetPriority() 都需要未移动的 4 位格式。

请注意：请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
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
在 STM32 微控制器上，您可指定的最低优先级实际上是 15，这是由
FreeRTOSConfig.h中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。

我们还建议确保将所有四个优先级位分配为
抢占式优先级位，并且不设置子优先级位，就和演示
中的一样。

每个移植都会将 'BaseType_t' 定义为对该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长类型。

### 中断服务程序

与大多数移植不同，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

作为示例，此演示提供了一个中断服务程序，
称为 EXTI9_5_IRQHandler()，定义在 main.c 中。此中断是通过
按下入门套件硬件上的 “USER” 按钮触发的。中断
使用信号量与任务同步，并调用 portEND_SWITCHING_ISR
以确保中断直接返回到任务。函数显示如下：

```c

void EXTI9_5_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Only line 6 is enabled, so there is no need to test which line generated
 the interrupt. */
    EXTI_ClearITPendingBit( EXTI_Line6 );

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. First the handler releases a semaphore.
 lHigherPriorityTaskWoken has been initialised to zero. */
    xSemaphoreGiveFromISR( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than the currently executing task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE.
 Passing pdTRUE into the following macro call will cause this interrupt to
 return directly to the unblocked, higher priority, task. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}

```

只有以 "FromISR" 结尾的 FreeRTOS API 函数可以从
中断服务程序中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY 配置常量设置的
优先级。

### FreeRTOS 使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

### 在抢占式和协同式 RTOS 内核之间切换

将 RTOSDemo/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式调度；
设置为 0 以使用协作式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点,
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ARM Cortex-M4F 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。
