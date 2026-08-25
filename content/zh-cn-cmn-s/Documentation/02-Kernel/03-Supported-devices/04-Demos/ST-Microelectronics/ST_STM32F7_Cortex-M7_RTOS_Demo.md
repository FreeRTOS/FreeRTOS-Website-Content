---
title: "ST ARM Cortex-M7 STM32 F7 RTOS演示，含 IAR 和 ARM Keil 嵌入式编译器项目"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[IAR](http://www.iar.com/ewarm)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### 简介

本页面记录了针对 STM32756G-EVAL 评估套件的 FreeRTOS 演示，
该套件包含
[STM32F7 ARM Cortex-M7 微控制器](http://www.st.com/web/en/catalog/mmc/SC1169/SS1858)
（[STMicroelectronics](http://www.st.com/)开发），还提供了适用于
[IAR](http://www.iar.com/ewarm)
和 ARM Keil 工具的预配置构建项目。

---

### *重要提示！使用 STM32F7 Cortex-M7 RTOS 演示 *的注意事项

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#st-arm-cortex-m7-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和用法详情)

另请参阅常见问题 [我的应用程序未运行，哪里出错了?](/Why-FreeRTOS/FAQs/Troubleshooting)
请特别注意，
在开发时使用[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
（在 FreeRTOSConfig.h 中定义）。

---

### 源代码组织

本网站提供的 FreeRTOS 发行版包含所有 FreeRTOS 移植的源文件，
以及所有 FreeRTOS 演示应用程序的项目，因此，它的文件数量
比使用 STM32 F7 微控制器所需的要多得多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
获取目录结构的介绍以及有关创建
新 FreeRTOS 项目的信息。

STM32F7 演示应用程序的 ARM 工作区的 IAR 嵌入式工作台名为
RTOSDemo.eww，位于 FreeRTOS/Demo/CORTEX_M7_STM32F7_STM32756G-EVAL
目录下。

STM32F7 演示应用程序的 ARM Keil 项目名为
RTOSDemo.uvprojx，位于 FreeRTOS/Demo/CORTEX_M7_STM32F7_STM32756G-EVAL
目录下。

---

### ST ARM Cortex-M7 演示应用程序

### 硬件设置

演示使用 LED ，该 LED 通过定位跳线 JP24 连接到端口 F 的引脚 10，
因此跳线连接了引脚 2 和引脚 3。

![将 LED 连接到 Cortex-M7 设备的跳线设置](/media/2018/STM32F7_Cortex_M7_Jumper_Setting.png)

**JP24 用于连接引脚 F10 和 LED**

### 功能

可以构建 STM32 F7 演示应用程序来创建简单的 blinky 演示，
或综合测试和演示应用程序。常量
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，定义于 main.c 的顶层，
用于在二者之间进行切换。

### mainCREATE_SIMPLE_Blinky_DEMO_ONLY设置为 1 时的功能

要构建简单的 blinky 演示，将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，
生成 main_blinky()。main_blinky() 创建一个非常简单的演示，如下：
* **main_blinky() 函数：**
RTOSmain_blinky() 会在启动调度器之前创建两个任务和一个队列
 。
* **队列发送任务：**

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask () 执行。
 每 200 毫秒向队列写入一次。
* **队列接收任务：**

 队列接收任务由 main_blinky.c 中的  prvQueueReceiveTask () 实现
 。它阻止队列读取以等待来自
 队列发送任务的消息，每次收到消息时会切换一次 LED。
 由于队列发送任务每 200 毫秒向队列写入一次，
 队列接收任务每 200 毫秒接收一条消息，并切换 LED
 。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

要构建综合测试和演示，将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
这样 main() 就会调用 main_full()。综合测试和
演示应用程序演示了：

* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)

创建的任务大多来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)集
除了演示如何使用
FreeRTOS API 和测试 RTOS 移植外，没有其他特定目的。

还创建了一个“检查”任务，
定期检查标准演示任务，以确保它们按预期执行。检查任务也会切换 LED
。**如果检查任务确定
演示正在按预期执行，LED 将每 3 秒切换一次；如果检查任务检测到
任何标准演示任务中的潜在错误**，LED 将每 200 毫秒切换一次。

### 构建并执行演示应用程序 - IAR

1. 打开 FreeRTOS/DEMO/CORTEX_M7_STM32F7_STM32756G-EVAL/RTOSDemo.eww
 （从 IAR 嵌入式工作台 IDE 中打开）。
2. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 以根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
3. 确保目标硬件使用
 合适的调试器接口连接至主机——演示是使用 J-Link
 进行开发和调试的。
4. 从 IDE 的 '**Project**' 菜单中选择 '**Rebuild All**'，
 RTOS 演示项目构建时不应报错或出现警告。
5. 构建完成后, 从 IDE 的 '**Project**' 菜单选择 '**Download and Debug**'
 对 Cortex-M7 微控制器进行编程，启动调试会话，
 并使调试器在输入 main() 函数时中断。

### 构建和执行演示应用程序 — Keil

1. 打开FreeRTOS/DEMO/CORTEX_M7_STM32F7_STM32756G-EVAL/RTOSDemo.uvprojx
 （从 Keil uVision IDE 内打开）。
2. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 以根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
3. 确保目标硬件使用
 合适的调试器接口连接至主机——演示是使用 J-Link
 进行开发和调试的。
4. 从 IDE的 '**Project**' 菜单中选择 '**Build Target**'。
 RTOSDemo 项目应该在没有任何错误或警告的情况下构建。
5. 构建完成后，从 IDE 的“**Debug**”菜单中选择"**Start/Stop Debug Session**"，
 对 Cortex-M7 微控制器进行编程，启动调试会话，
 并使调试器在输入 main() 函数时中断。

---

### RTOS 配置和用法详情

### ARM Cortex-M7 FreeRTOS 端口特定配置

此演示的特定配置项位于 FreeRTOS/Demo/cortex_M7_STM32F7_STM32756G-EVAL/FreeRTOSConfig.h。
[可以编辑此文件中定义的常量，以适合您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ**

 此常量可用于设置 RTOS 滴答中断的频率。提供的值 (1000 Hz) 对于
 测试 RTOS 内核功能，但此频率比大多数应用程序所需的频率都要高。
 降低频率会提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY**

 鉴于 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的八位未移位值，并且被定义为作为原始数据直接在
 ARM CORTEX-M7 NVIC 寄存器中用作原始数字，configLIBRARY_lowest_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 是仅使用 STM32F7 NVIC 中实现的 4 个优先位定义的等效物
 NVIC 中实现。
 提供这些值是因为 CMSIS 库函数 NVIC_SetPriority()
 需要未偏移的 4 位格式。

请注意！请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记! 如果希望
为中断分配低优先级，请勿将其优先级指定为 0(或其他较小数值)，
因为这实际上可能会导致该中断在系统中具有最高优先级，
因此，如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

ARM Cortex-M 核心的最低优先级实际上是 255，但是不同的
ARM Cortex-M 微控制器制造商实现的优先级位数不同，
并且提供的库函数要求以不同的方式指定优先级。例如，
ST STM32F7 ARM Cortex-M7 微控制器上可以指定的最低优先级实际上为 15，
这是由 FreeRTOSConfig.h中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。

我们还建议确保将所有优先级位指定为
抢占式优先级位，不要将任何优先级位指定为次优先级位，
正如在演示项目中通过函数调用 **\`\`\`c 进行这样的设置

HAL_NVIC_SetPriorityGrouping (NVIC_PRIORITYGROUP_4);

```**

Each port #defines 'BaseType_t' to equal the most efficient data type for that
processor. This port defines BaseType_t to be of type long.

### Interrupt service routines

Unlike many FreeRTOS ports, interrupt service routines that cause a context switch have
no special requirements, and can be written as per the compiler documentation.
The macro portEND_SWITCHING_ISR() can be used to request a context switch from
within an interrupt service routine.

Note that portEND_SWITCHING_ISR() will leave interrupts enabled.

The following source code snippet is provided as an example. The interrupt
uses a [direct to task notification](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
to synchronise with a task (not shown), and calls portEND_SWITCHING_ISR
to ensure the interrupt returns directly to the task.

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A task notification is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for the notification
 then sending the notification will have removed the task from the Blocked
 state. If the task left the Blocked state, and if the priority of the task
 is higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into the
 portEND_SWITCHING_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portEND_SWITCHING_ISR() has no effect. */
    portEND_SWITCHING_ISR( lHigherPriorityTaskWoken );
}

```

只有以 "FromISR" 结尾的 FreeRTOS API 函数才能
中断服务程序中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。

### FreeRTOS使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

### 在抢占式和协同式 RTOS 内核之间切换

在 FreeRTOSConfig.h 中将 configUSE_PREEMPTION 设置为 1，即可使用抢占式调度；设置为 0，
即可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

ARM Cortex-M7 演示应用程序项目中包含的 Source/Portable/MemMang/heap_4.c 可用于提供
RTOS 内核所需的内存分配。
请参阅 API 文档的 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。
