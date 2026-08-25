---
title: "Tensilica Xtensa 可定制处理器 RTOS 演示，使用 Xtensa Xplorer IDE"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[可定制处理器](https://ip.cadence.com/ipportfolio/tensilica-ip/xtensa-customizable)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Tensilica Xtensa 可定制处理器](/media/2019/Xtensa_Customizable_Processors.png)

 Tensilica Xtensa 可定制处理器

### 简介

此页面记录的演示应用程序面向
[Tensilica Xtensa 可定制处理器](https://ip.cadence.com/ipportfolio/tensilica-ip/xtensa-customizable)。
该项目面向 Xtensa 模拟器，并使用
[Xtensa Xplorer IDE](https://ip.cadence.com/swdev)
和 XCC 编译器构建。
可以编译项目以创建简单的 blinky 演示，或
全面的测试和演示应用程序。

[![适用于 RTOS 项目的 Xtensa Xplorer IDE](/media/2019/Xtensa_Xplorer_IDE.png)](/media/2019/Xtensa_Xplorer_IDE.png)

 Xtensa Xplorer IDE 的屏幕截图

---

### *重要提示！Tensilica Xtensa 可定制处理器演示使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#构建并运行-tensilica-xtensa-可定制处理器-rtos-应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序
未运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)特别注意建议
在开发时使用 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
（在 FreeRTOSConfig.h 中定义）。

---

### 源代码组织

FreeRTOS 下载文件包含每个 FreeRTOS 移植的源代码和
所有的演示应用程序。因此，它包含的文件比
Tensilica 演示所需的多很多。请参阅本网站的[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
章节，了解有关下载文件的描述。

Xtensa Xplorer 项目位于
/FreeRTOS/Demo/Tensilica_Simulator_Xplorer_XCC 目录，
且具有常用的 Eclipse 项目名称 .project。

---

### 构建并运行 Tensilica Xtensa 可定制处理器 RTOS 应用程序

RTOS 演示项目的配置可用于构建简单的 blinky 演示或
全面的测试和演示应用。常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
定义于 main.c 文件的顶部，可用于在两者间切换。

* 如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
 设置为 1，则创建简单的 blinky 演示。
* 如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
 设置为 0，则创建全面的演示。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 ，则 main ()
调用 main_blinky()。main_blinky() 创建一个非常简单的演示，如下：
* **main_blinky() 函数：** 
 main_blinky() 会创建一个队列、一个软件定时器和两个任务。然后
 它会启动 RTOS 调度器。
* **队列发送任务：** 
 队列发送任务由 prvQueueSendTask() 函数在
 main_blinky.c 文件中实现。它使用 vTaskDelayUntil() 每隔 200毫秒
 将值 100 发送到队列。
* **队列发送软件定时器：** 
 定时器是一个自动重新加载定时器，周期为两秒。定时器的
 回调函数将值 200 写入队列。回调函数
 由 main_blinky.c 文件中的 prvQueueSendTimerCallback() 实现。
* **队列接收任务：** 
 队列接收任务由 main_blinky.c 文件中的
 prvQueueReceiveTask() 实现。它等待数据到达队列。接收到数据时，
 任务检查数据的值，然后输出消息
 以说明数据来自队列发送任务还是队列发送
 软件定时器。

*请注意，这是唯一会输出消息的任务，因此不会尝试
 保障 printf 函数的线程安全。注意不要在多个任务中使用 printf
 函数。*

预期行为如下：
* 队列发送任务每隔 200 毫秒写入队列，因此每隔 200 毫秒
 队列接收任务将输出消息，指出已在队列发送任务的队列上
 接收了数据。
* 队列发送软件定时器有两秒钟的周期，因此每隔两秒钟
 队列接收任务将输出消息，指出已从队列发送任务定时器的队列上
 接收到数据。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main()
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序，
用于演示下列各项：

* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [事件组](FreeRTOS-Event-Groups.md)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)

创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务集。所有 FreeRTOS 移植演示应用程序使用标准演示任务，
它们没有特定的功能。它们用于演示如何使用
FreeRTOS API，并测试 RTOS 移植。

演示项目创建了一个“检查”任务，以定期按顺序检查演示项目中的标准演示任务，
以确保所有任务都按能运行。如果没有检测到错误，
检查任务定期输出“无错误” 、当前模拟的 tick 时间、
空闲堆大小和到目前为止的最小空闲堆大小。如果在执行任务时发现错误，
检查任务将输出适当的
错误消息。

*请注意，这是唯一会输出消息的任务，因此不会尝试
保障 printf 函数的线程安全。注意不要在多个任务中使用 printf
函数。*

中断队列测试（IntQueue.c 文件）执行中断嵌套并被观察到
干预模拟器上其他测试的正常运行。因此，
main_full.c 文件中提供的 mainENABLE_INT_QUEUE_TESTS macro 宏用于选择
是否启用中断队列测试或所有其他测试。

* 当 mainENABLE_INT_QUEUE_TESTS 设置为 1 时，启用中断队列测试
 并禁用所有其他测试。
* 当 mainENABLE_INT_QUEUE_TESTS 设置为 0 时，禁用中断队列测试
 并启用所有其他测试。

### 
使用 Xtensa Xplorer IDE 进行构建

1. 启动 Xtensa Xplorer IDE，然后按照提示创建一个新的或选择一个现有的
 工作区。
2. 在 IDE 的 "File" 菜单中选择 "Import"。系统将显示
 以下对话框。选择 “General-->Existing Projects into Workspace”，如下
 所示：

![Xtensa Xplorer IDE 文件导入对话框](/media/2019/Xtensa_Xplorer_File_Import.png)

**首次点击 "Import" 时显示的对话框**
3. 在下一个对话框中，选择 /FreeRTOS/Demo/Tensilica_Simulator_Xplorer_XCC
 作为根目录。确保在 "Projects" 区域中已勾选 RTOS 演示项目，
 **并且确保未勾选 'Copy Projects Into
 Workspace' 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。

![导入 Xtensa Xplorer IDE 时选择 RTOS 源代码](/media/2019/Xtensa_Xplorer_File_Import2.png)

**确保已勾选 RTOS 演示，并且确保未勾选 "Copy projects into workspace"**
4. 从 Active Project 下拉菜单中选择 “RTOSDemo”，如下所示（点击放大）：

[![Xtensa Xplorer IDE 选择活动项目](/media/2019/Xtensa_Xplorer_Select_Active_Project.png)](/media/2019/Xtensa_Xplorer_Select_Active_Project.png)

**选择活动项目**
5. 从 Build 下拉菜单中选择 “Build Active”（或按 Ctrl+Alt+B），
 如下所示（点击放大） ：

[![Xtensa Xplorer IDE 构建](/media/2019/Xtensa_Xplorer_Build.png)](/media/2019/Xtensa_Xplorer_Build.png)

**构建活动项目**
6. 从 Debug 下拉菜单中选择 “Debug” 以启动调试会话，
 如下所示（点击放大）：

[![Xtensa Xplorer IDE 调试](/media/2019/Xtensa_Xplorer_Debug.png)](/media/2019/Xtensa_Xplorer_Debug.png)

**调试活动项目**
7. 从 Console 下拉菜单中选择 "Simulator Console" 以查看演示输出，
 如下所示（点击放大） ：

[![Xtensa Xplorer IDE 模拟器控制台](/media/2019/Xtensa_Xplorer_Simulator_Console.png)](/media/2019/Xtensa_Xplorer_Simulator_Console.png)

**模拟器控制台**

---

### RTOS 配置和使用详情

### 中断服务程序

导致无特殊要求的上下文切换的中断服务程序
可以按照编译器文档编写。以下示例
显示了使用宏 portYIELD_FROM_ISR 请求在中断服务程序中
进行上下文切换。请参阅文件 FreeRTOS/Demo/Tensilica_Simulator_Xplorer_XCC/IntQueueTimer.c
以获得完整示例。

```c
void Dummy_IRQHandler( void *arg )
{
long lHigherPriorityTaskWoken = pdFALSE;

    ( void ) arg; /* Parameter not used. */

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A [task notification](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
 that end in "FromISR" can be called from an ISR! */
    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for a notification,
 and giving the notification caused the task to unblock, and the unblocked
 task has a priority higher than the current Running state task (the task that
 this interrupt interrupted), then lHigherPriorityTaskWoken will have been set
 to pdTRUE internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into
 the portYIELD_FROM_ISR() macro will result in a context switch being pended
 to ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

### RTOS 移植相关配置

这些演示的特定[配置项目](/Documentation/02-Kernel/03-Supported-devices/02-Customization)位于
FreeRTOSConfig.h 文件中，该文件位于项目文件所在的目录。
您可以编辑 FreeRTOSConfig.h 中定义的常量，以满足您的应用程序的需求
。特别是——

* **configTICK_RATE_HZ**
 此常量设置了 RTOS tick 中断的频率。提供的数值 1000 Hz 值可用于
 测试 RTOS 内核功能，但此频率比大多数应用程序所需的频率
 都要高。降低此值可提高效率。

 每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
 。此移植定义 BaseType_t 为 int 型。

### 在抢占式和协同式 RTOS 内核之间切换

 将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1
 可使用抢占式调度，设置为 0 可使用协同式调度。完整的演示应用程序可能无法
 正确执行，当选择了协同式 RTOS 调度器时。

### 编译器选项

 与所有移植一样，使用正确的编译器选项
 至关重要。若要确保这一点，最佳方法是基于
 提供的演示应用程序文件构建您的应用程序。

### 内存分配

Source/Portable/MemMang/heap_4.c 包含在演示应用程序项目中
 以提供 RTOS 内核所需的内存分配。请
 参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
 以获取完整信息。

### 其他事项

 请注意，vPortEndScheduler() 尚未实现

