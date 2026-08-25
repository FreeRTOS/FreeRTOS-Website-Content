---
title: "使用面向 Code Composer (CCS) 的 FreeRTOS Cortex-M 移植的 TI SimpleLink CC3220 RTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Texas Instruments CC3220 SimpleLink WiFi Launchpad 开发套件](/media/2018/CC3220-SimpleLink-WiFi.jpg)

 SimpleLink CC3220 LaunchPad 开发套件

### 简介

此页面记录的 Code Composer Studio (CCS) 演示应用程序面向
Texas Instruments SimpleLink CC3220 WiFi MCU。CC3220SF 部件具有一个 ARM Cortex-M4
核心、1 MB 闪存、256 KB RAM 和增强的安全功能。

注意：即使 CC3220 具有 ARM Cortex-M4 核心，也不使用
浮点单元 (FPU) ，因此它使用 FreeRTOS Cortex-M3 移植。

演示项目已预先配置为在 [SimpleLink Wi-Fi CC3220SF
 无线微控制器 LaunchPad 开发套件](http://www.ti.com/tool/cc3220sf-launchxl)上运行，并且可以配置为
创建简单的 blinky 演示或全面的测试和演示应用程序。
blinky 演示使用 FreeRTOS 的无滴答空闲模式来降低功耗。

### “无滴答”低功耗操作

通过停止 RTOS 滴答中断，微控制器可以维持在节能状态，
直到中断发生，或者到了 RTOS 内核
将任务转换为“就绪”状态的时间。请注意，本文仅演示了通用
ARM Cortex-M 无滴答实现。通过定制无滴答实现，
使用特定于 CC3220 的时钟和低功率模式将显著提升节能成效
。

请参阅[低功耗支持](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
和[适用于 ARM Cortex-M MCU 的低功耗 RTOS](/low-power-ARM-cortex-rtos)
页面，了解更多信息。

---

### *重要提示！使用 TI CC3220 SimpleLink ARM Cortex-M4F 演示的注意事项*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序功能)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未
运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含每个 FreeRTOS 移植的源代码和
所有演示应用程序，因此包含的文件数量远多于 CC3220 SimpleLink
演示的要求。请参阅此网站有关[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)
了解有关下载文件的描述。

CCS 使用 [Ecliplse IDE](http://www.eclipse.org/ide/)，
因此 CCS 项目采用常用的 Eclipse 项目名称 .project。该
项目位于
/FreeRTOS/Demo/CORTEX_M4_SimpleLink_CC3220SF_CCS 目录下。

---

### 构建和运行 CCS3220 SimpleLink RTOS 应用程序

RTOS 演示项目可以被配置为构建
一个简单的 blinky 项目，同时演示 FreeRTOS 的通用 ARM Cortex-M 无滴答低功耗模式，
或者一个全面的测试和演示应用。常量
configCREATE_SIMPLE_TICKLESS_DEMO 位于
项目的 FreeRTOSConfig.h 文件顶部，
用于在二者之间进行切换。

* 如果 configCREATE_SIMPLE_TICKLESS_DEMO
 设置为 1，则创建简单的无滴答演示。
* 如果 configCREATE_SIMPLE_TICKLESS_DEMO
 设置为 0，则创建全面演示。

请注意本页顶部包含的[注释](#无滴答低功耗操作)，
了解使用所演示的通用
无滴答实现与使用特定于 CC3220
的无滴答实现时的节能效果区别。

此演示使用了在 Launchpad 开发套件上构建的 LED，
因此无需进行硬件设置。

#### 使用基于 TI Eclipse 的 Code Composer Studio (CCS) 构建

**注意：**CCS 项目通过相对路径引用文件。如果目录路径已更改或文件已移动，
则无法构建项目。Eclipse
的 'export' 功能可用于将项目转换为独立项目，
此项目只能使用 .project 文件所在目录下的目录。

1. 使用硬件的 USB 连接器将 Launchpad 开发套件直接连接到主机
 （运行 CCS 的计算机），无需其他调试
 接口。
2. 启动 CCS Eclipse IDE，然后按照提示创建一个新的或选择一个现有的
 工作区。
3. 在 IDE 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "Code Composer Studio->CCS Projects"（如下所示）。

![将 ARM Cortex-M4 RTOS 演示项目导入 CCS Eclipse IDE](/media/2018/import_code_composer_studio.jpg)

**首次点击 "Import" 时显示的对话框**
4. 在下一个对话框中，选择 /FreeRTOS/Demo/CORTEX_M4_SimpleLink_CC3220SF_CCS
 作为根目录。确保在 "Projects" 区域中已勾选 RTOS 演示项目，
 **并且确保未勾选 'Copy Projects Into
 Workspace' 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。

![导入到 Eclipse CDT 时选择 RTOS 源代码](/media/2018/Import_SimpleLink_CC3220_CCS.jpg)

**确保已勾选 RTOS 演示，并且确保未勾选 "Copy projects into workspace"**
5. 从 CCS Eclipse 的 "Project" 菜单中选择 "Build All"，以构建
 演示项目。
6. 从 Eclipse 的 "Run" 菜单中选择 "Debug"，
 对微控制器闪存进行编程并启动调试
 会话。

### 演示应用程序功能

#### 使用无滴答操作的简单 blinky 示例

当 configCREATE_SIMPLE_TICKLESS_DEMO 设置为
1 时创建简单的无滴答示例。configCREATE_SIMPLE_TICKLESS_DEMO 定义于 FreeRTOSConfig.h 顶部。

FreeRTOS 无滴答闲置模式在闲置期间（没有可执行的应用程序任务的期间）停止周期性 RTOS 滴答中断
。
此 blinky 示例创建了两个任务，它们每秒只取消阻塞一次，
因此在大部分执行时间内都会停止滴答中断。

通过停止 RTOS 滴答中断，微控制器可以维持在节能状态，
直到中断发生，或者到了 RTOS 内核
将任务转换为“就绪”状态的时间。

请注意本页顶部包含的[注释](#无滴答低功耗操作)，
了解使用所演示的通用
无滴答实现与使用特定于 CC3220
的无滴答实现时的节能效果区别。通用无滴答闲置
模式使用 SysTick 时钟，该 24 位系统时钟速度较快，因此
会在演示任务进入和随后退出阻塞状态之间发生多次溢出，
每次溢出都会产生一个中断。

将 configCREATE_SIMPLE_TICKLESS_DEMO 设置为 1 会导致 main() 调用
main_blinky()：

* **main_blinky() 函数：**

 main_blinky() 在启动调度器前会创建队列、队列发送任务和队列接收任务
 。
* **队列发送任务：**

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。

 prvQueueSendTask() 每秒向队列发送一次值 100。
* **队列接收任务：**

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 实现。

 prvQueueReceiveTask() 在数据达到队列前保持阻塞状态。
 该任务每次从队列接收值 100 后闪烁 LED。
 由于任务每秒向到队列发送一次数据，因此 LED
 每秒闪烁一次。

#### 全面测试和演示应用

当 configCREATE_SIMPLE_TICKLESS_DEMO 设置为
0 时创建全面示例。configCREATE_SIMPLE_TICKLESS_DEMO 定义于 FreeRTOSConfig.h。

将 configCREATE_SIMPLE_TICKLESS_DEMO 设置为 0 会导致 main() 调用
main_full()：

* **main_full() 函数：**

 main_full() 创建了一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)、
 Register Test 任务，并启动
 调度器。
* **"Reg Test" 任务：**

 Reg Test 任务通过对每个通用微控制器寄存器填充已知值来测试上下文切换机制，
 然后
 持续检查每个寄存器是否在任务的生命周期内保持其预期值
 。
* **"Check" 任务：**

 "Check" 任务监测系统内所有其他任务的状态，
 寻找停滞的任务或报告错误的任务。
 它每次被调用时都会切换 LED。

 如果 LED 每 3 秒钟切换一次，则 check 任务确定
 演示正在按预期运行。如果 LED
 每 200 毫秒切换一次，则表示至少发现了一个错误。

---

### RTOS 配置和使用详情

#### 中断服务程序

##### 优先级分配

请注意！请参阅[专门介绍如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值），
因为这实际上可能会导致该中断在系统中具有最高优先级，
因此，如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

ARM Cortex-M 核心上的最低优先级实际上是 255，但不同
ARM Cortex-M 微控制器制造商会实现不同数量的优先级位，
并且提供的库函数要求以不同的方式指定优先级。例如，
TI CC3220 ARM Cortex-M4 SimpleLink MCU 实现了 3 优先级位，
允许使用最多 8 个不同的优先级（0 到 7，含 0 和 7）。最低优先级对应
最大数字。某些库函数会使用数值 7 作为
最低优先级，而其它函数则会使用数值 224 作为最低优先级（
即 7 \<\< 5，这样 ARM Cortex-M 才能在中断控制器中看到该值）。
这两个数字分别由
FreeRTOSConfig.h 中的 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configKERNEL_INTERRUPT_PRIORITY 定义。可指定的最高优先级
始终为零。

我们还建议确保将所有优先级位指定为
抢占式优先级位，不要将任何优先级位指定为子优先级位。

##### 实施中断服务程序

导致上下文切换的中断服务程序
无特殊要求。参见以下示例：

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

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

#### RTOS 移植特定配置

专用于此类演示的[配置项](/Documentation/02-Kernel/03-Supported-devices/02-Customization)包含在 FreeRTOSConfig.h
文件中，该文件位于项目文件所在的目录。您可以
编辑 FreeRTOSConfig.h 中定义的常量，使其适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 此常量设置了 RTOS 滴答中断的频率。提供的数值 1 Hz 可用于测试
 RTOS 内核功能，但比大多数应用程序要求的速度更快。
 降低此值可提高效率。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
。所有 ARM Cortex-M4F 移植都将 BaseType_t 的类型定义为 long。

请注意 vPortEndScheduler() 尚未实现。

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM CORTEX-M4F 演示应用程序项目中，用以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。

