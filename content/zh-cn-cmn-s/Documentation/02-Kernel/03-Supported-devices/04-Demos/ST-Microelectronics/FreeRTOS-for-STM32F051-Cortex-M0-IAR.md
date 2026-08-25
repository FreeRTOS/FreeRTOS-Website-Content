---
title: "使用 IAR 开发工具的 STM32F051 ARM Cortex-M0 演示"
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
| <br />![](/media/2018/STM32_F0_generic.jpg)<br /> |

### 引言

此页面上的项目介绍了 FreeRTOS ARM Cortex-M0 IAR 移植。
它配置为在 STM320518-EVAL 评估板上运行，该评估板配有一个
STM32F051 微控制器。

该项目可以配置为创建基本的 "blinky" 风格的演示，
或配置为更全面的测试和演示应用程序，
应用程序中包括一些 FreeRTOS 标准演示任务。

![FreeRTOS 内核感知调试器，可与 IAR 编译器结合使用](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)

 FreeRTOS 状态查看器插件的屏幕截图

 （此插件是 IAR IDE 的 标准配件）。

**注意：**如果项目构建失败，则可能是使用的 IAR
嵌入式工作台版本过低。如果构建失败，
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。

---

### *重要提示！使用 IAR ARM Cortex-M0 演示*的注意事项

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未
运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，
因此其中包含的文件远比演示所需的文件多。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，
了解关于已下载文件的说明
和新项目创建的信息。

FreeRTOS STM32F0 演示应用程序的 IAR EWARM 工作区名为 RTOSDemo.eww，
位于 FreeRTOS/Demo/CORTEX_M0_STM32F0518_IAR 目录下。请注意，
此工作区创建于 STM32F0 支持加入 EWARM 之前，
因此，该项目配置为使用通用 ARM Cortex-M0 内核，
本页上提供了相应说明，介绍了对微控制器闪存进行编程所用的独立 ST-Link
实用程序。

---

### 演示应用程序

### 演示应用程序硬件设置

该演示采用了集成在 STM320518-EVAL 板上的 LED，
因此不需要任何硬件设置。

### 构建和运行演示应用程序

单个 RTOS 演示
项目可配置为运行简单的 "blinky" 风格的项目或者更全面的测试和演示应用程序。main.c 顶部的
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
设置用于在两者之间进行选择。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，
以创建基本的 "Blinky" 风格演示。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
以创建更全面的测试和演示应用程序。

1. 打开 FreeRTOS/Demo/CORTEX_M0_STM32F0518_IAR/RTOSDemo.eww
 （位置：IAR 嵌入式工作台 IDE）。
2. 在构建项目之前，设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
 常量以生成所需的演示功能（如上所述）。
3. 给 STM320518-EVAL 板通电，然后用 USB 数据线将标记为
 ST-LINK/V2 (SN3) 的 USB 移植连接到主机。
4. 打开 FreeRTOS/Demo/CORTEX_M0_STM32F0518_IAR/Debug/RTOSDemo.bin
 （STM320518-EVAL 硬件的随机 CD
 上也有一个这样的程序），
 然后对微控制器闪存进行编程。更高版本的 IAR 嵌入式工作台或许可以从
 IAR IDE 内部对闪存进行编程，
 无需再单独使用 ST-LINK 实用程序。
5. **从 ST-LINK 实用程序的 "Target" 菜单中选择 "Disconnect"。**ST-LINK 实用程序连接到硬件时，
 无法从 IAR IDE
 启动调试会话。
6. 回到 IAR 嵌入式工作台 IDE，
 从 IDE 的 "Project" 菜单中选择 "Debug without Downloading"，启动调试会话。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 会导致 main() 调用 main_blinky()。
main_blinky() 创建了一个非常简单的演示程序，
如下所示。

* **main_blinky() 函数：** 

 main_blinky() 会创建一个队列和两个任务。然后它会启动
 调度器。
* **队列发送任务:** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。
 prvQueueSendTask() 位于一个循环中，
 在将值 100 发送到
 在 main_blinky() 中创建的队列之前，该任务会被反复阻塞 200 毫秒。一旦值发送成功，任务就会再次循环，
 再次被阻塞 200 毫秒。
* **队列接收任务：** 

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现。
 prvQueueReceiveTask() 位于一个循环中，
 它会反复阻塞试图从队列中读取数据的操作，该队列创建于 main_blinky() 中。接收到数据时，
 任务会检查数据的值，如果该值等于
 预期值 100，则切换 LED LD1。传递给队列接收函数的“阻止时间”参数规定，
 此任务应当无限期地保持在“已阻塞”状态，
 直到队列上有可用数据为止。只有当
 队列发送任务写入队列时，队列接收任务才会解除“已阻塞”
 。由于队列发送任务每 200 毫秒向队列写入一次，
 队列接收任务每 200 毫秒解除一次“已阻止”状态，
 因此 LED LD1 每 200 毫秒切换一次。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 会导致 main() 调用 main_full()。
main_full() 会创建更全面的测试和演示应用程序，
请参阅下文。

* **main_full() 函数：** 

 main_full() 创建了一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) ，
 测试任务和一个定时器。然后它会启动
 调度器。
* **“寄存器测试”任务：** 

 这些任务用已知值填充寄存器，然后检查
 每个寄存器在整个任务生命周期内是否保持其预期值
 。每个任务使用不同的值集。寄存器测试任务以非常低的优先级执行，
 因此经常被抢占。包含意外值的寄存器
 表示上下文切换机制中存在错误
 。
* **“检查”软件定时器：** 

 检查软件定时器的周期最初设置为三
 秒。其回调函数检查所有标准演示任务和
 寄存器检查任务是否仍在执行，
 且执行时是否报告任何错误。如果检查定时器回调发现
 任务已停顿，或报告了错误，之后它会将
 检查定时器的周期从最初的三秒钟更改为仅 200 毫秒。每次调用回调函数时，
 也会切换 LED LD4。这可直观体现
 系统状态指示：**如果 LED 每三秒切换一次，
 则表示未发现任何问题。如果 LED 每 200 毫秒切换一次，
 则至少有一项任务中发现了问题**。

---

### RTOS 配置和使用详情

### 中断服务程序

导致上下文切换的中断服务程序
无特殊要求。
portEND_SWITCHING_ISR() 宏可用于从 ISR 内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

在
main.c 的末端提供名为 Dummy_IRQHandler() 的虚拟中断处理程序作为参考实现。
此外，还将 Dummy_IRQHandler() 复制到了下方。

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
 that end in "FromISR" can be called from an ISR! */
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

请注意，以下行包含在 FreeRTOSConfig.h 中。

```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler

```

这些定义将 FreeRTOS 内核中断处理程序函数名映射到
CMSIS 中断处理程序函数名上；如此一来，无需任何修改，
就可以使用 ST 或 IAR 提供的链接器脚本和启动文件。

请注意：请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值），
（或其他低数字值），因为这会导致该中断在系统中
实际上具有最高优先级。另外，请勿忘记指定中断优先级，
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

### RTOS 移植特定配置

专用于此类演示的配置项包含在 FreeRTOS/Demo/CORTEX_M0_STM32F0518_IAR/FreeRTOSConfig.h 中。可以
编辑 FreeRTOSConfig.h 中定义的常量，使其适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 此常量可用于设置 RTOS 滴答中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但比大多数应用程序要求的速度更快。
 降低此值可提高效率。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_M0_STM32F0518_IAR/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，以使用抢占式调度，或设置为 0
以使用协同式调度。

### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ARM Cortex-M0 演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
