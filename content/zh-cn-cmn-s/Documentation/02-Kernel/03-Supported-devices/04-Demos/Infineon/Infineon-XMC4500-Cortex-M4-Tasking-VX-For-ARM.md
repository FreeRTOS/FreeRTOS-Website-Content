---
title: "Infineon XMC4500 ARM Cortex-M4 浮点演示 使用 Tasking VX-Toolset for ARM 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![使用 Tasking VX Toolset for ARM 编程的 XMC4500 微控制器开发板](/media/2018/Infineon-XMC4000-Cortex-M4-Hexagon-kit.jpg)

### 简介

**本页提供的演示已过时，[现已替换为新演示
和新文档页面](Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

本页记录的 FreeRTOS 演示应用程序
适用于 [XMC4500 ARM Cortex-M4 微控制器](http://www.infineon.com/xmc)
（来自 [Infineon](http://www.infineon.com/)）。该演示
使用 FreeRTOS Tasking VX-Toolset ARM Cortex-M4F 移植，
该移植要求应用程序启用 ARM Cortex-M4 硬件浮点单元，
以及需要为生成浮点指令而配置的项目选项
（此页面上描述的项目已正确配置）。

---

### *重要！FreeRTOS/Tasking XMC4000 演示项目使用注意事项*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#infineon-arm-cortex-m4-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS zip 文件包含所有 FreeRTOS的源文件
移植的源文件和所有演示应用程序，其中只有少数
是本项目需要的。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解关于已下载文件的说明
和创建新项目的相关信息。

XMC4500 演示应用程序的 Tasking VX-Toolset Eclipse 项目文件位于
FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4500_Tasking
目录下。本页的
[准备 Eclipse 项目](#构建并执行演示应用程序)部分
包含有关设置演示项目目录
以及将演示项目导入到 Tasking Eclipse IDE 的重要信息。

---

### Infineon ARM Cortex-M4 演示应用程序

可以使用 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 常量从两种配置中选择，
该常量位于 main.c 顶部附近。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 调用
main_blinky()，然后创建一个非常简单的演示，
请参阅下文。

* **main_blinky() 函数：**

 main_blinky() 会创建一个队列和两个任务。然后它会启动
 RTOS 调度器。
* **队列发送任务：**

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。
 prvQueueSendTask() 位于一个循环中，
 在将值 100 发送到
 在 main_blinky() 中创建的队列之前，该任务会被反复阻塞 200 毫秒。一旦值发送成功，任务就会再次循环，
 再次被阻塞 200 毫秒。
* **队列接收任务：**

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现。
 prvQueueReceiveTask() 在一个循环中运行，
 反复尝试从 main_blinky() 中创建的队列读取数据，并在读取过程中阻塞。接收到数据时，
 任务会检查数据的值，如果该值等于
 预期值 100，则切换 LED。传递给队列接收函数的“阻塞时间”参数规定，
 此任务应当无限期地保持在“已阻塞”状态，
 直到队列上有可用数据为止。只有当
 队列发送任务写入队列时，队列接收任务才会解除“已阻塞”
 。由于队列发送任务每 200 毫秒向队列写入一次，
 队列接收任务每 200 毫秒解除一次“已阻塞”状态，
 因此 LED 每 200 毫秒切换一次。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 调用
main_full()，然后创建全面测试和演示应用程序，
并演示以下内容：

* 浮点上下文切换。
* Malloc 失败和堆栈溢出[钩子函数](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)。
 main.c 中还包含 Tick 和 Idle 挂钩函数，但 FreeRTOSConfig.h 未进行配置
 以使用它们。参见 main.c 中函数实现中的注释。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。

部分已创建任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务，
而其他任务则
针对 XMC4500 Tasking 演示。所有 FreeRTOS 移植和演示应用程序都使用标准演示任务。
它们不具备特定功能，创建它们只是为了演示如何使用 FreeRTOS API，
以及测试 FreeRTOS 移植。

main()
之后启动 RTOS 调度器。然后，演示在运行期间动态地连续
和删除另外两个任务。

除了标准演示任务外，还创建了特定于应用程序的“寄存器测试”任务。
开始执行这些任务之前，需使用已知的值填充所有通用寄存器和浮点寄存器
。然后，任务反复检查
每个寄存器是否在任务的生命周期内均保持已写入的值不变
。寄存器检查任务按空闲优先级运行，因此经常会退出并重新进入
运行状态。这两个寄存器检查
任务分别使用不同的值填充 CPU 寄存器，如果寄存器包含意外值，
则表明上下文切换
机制中存在错误。

创建一个“检查”软件定时器，用于定期检查标准
演示任务和寄存器测试任务，以确保所有任务
都按预期运行。检查软件定时器的
回调函数可切换 XMC4500 Hexagon 开发工具包 CPU 板上的单用户 LED
。这直观地反映出了系统的
健康状况。**如果 LED 每 3 秒钟切换一次，则表示
检查软件定时器未发现任何问题。如果 LED 
每 200 毫秒切换一次，则表示检查软件定时器
在一个或多个任务中发现问题。**

#### 硬件设置

演示使用的是直接焊接到 CPU 板印刷电路板上的 LED，
因此不需要进行硬件设置。

#### 准备 Tasking VX-Toolset Eclipse 项目目录

Eclipse 项目既可以是标准的 makefile 项目，也可以是托管的 make 项目。
FreeRTOS Tasking ARM Cortex-M4F 项目使用一个托管的 make 项目。这
反过来又意味着：

1. 构建项目所需的所有源文件必须位于
 包含项目文件本身的文件夹/目录，或
2. 需要配置 Eclipse 工作区（注意是工作区，而非项目）
 来定位硬盘上其他位置的文件。

此演示采用上方的选项 1。因此，目录 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4500_Tasking
包含一个名为 CreateProjectDirectoryStructure.bat 的批处理文件，
该文件将所需的所有 FreeRTOS 源文件和一些标准的演示应用程序文件
复制到演示项目目录下的子目录中。

**CreateProjectDirectoryStructure.bat 必须在将 Tasking
 项目导入 Eclipse 工作区之前执行 。**

CreateProjectDirectoryStructure.bat 不能在
Tasking IDE 中执行。

#### 将演示应用程序导入到 Tasking Eclipse 工作区

要想将必要的项目导入现有或新的 Eclipse 工作区：
1. 在 Tasking 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "Existing Projects into Workspace"。

![Importing the ARM Cortex-M4 project into the Eclipse workspace](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)

**首次点击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4500_Tasking
 作为根目录。然后，确保在 "Projects" 区域勾选 RTOSDemo 项目（而非下图所示的
 "FreeRTOS-Simple-Demo"），
 **并确保未勾选 "Copy Projects Into
 Workspace" 复选框**，然后点击
 "Finish" 按钮（请参阅下图，查看正确的复选框状态）。

![选择 ARM Cortex-M4 RTOSDemo，以导入 Tasking Eclipse](/media/2018/selecting-the-FreeRTOS-STM32-project-to-import-into-Eclipse.jpg)

**确保勾选 RTOSDemo 项目（而非如图所示的 FreeRTOS-Simple-Demo），

 并且未勾选 "Copy projects into workspace"**

#### 构建并执行演示应用程序

1. 确保已按上述说明执行 CreateProjectDirectoryStructure.bat 批处理文件，
 项目已导入到 Tasking 工作区中，
 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 已完成设置以生成所需的
 演示功能。
2. 确保已使用合适接口将目标硬件
 连接到主机。该项目是使用 J-Link Lite 创建的。
3. 在 IDE 的 "Project" 菜单中选择 "Build All"，
 RTOSDemo 项目应该在没有任何错误或警告的情况下构建。
4. 项目构建完毕后，在 IDE 中单击 "Debug" 速度按钮
 对微控制器闪存进行编程并启动调试会话。

---

### RTOS 配置和使用详情

#### Cortex-M4F FreeRTOS 移植特定配置

此演示的特定配置项位于 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4500_Tasking/FreeRTOSConfig.h。
[可以编辑此文件中定义的常量，以适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ**

 此常量可用于设置 RTOS 滴答中断的频率。提供的值 (1000 Hz) 对于
 测试 RTOS 内核功能，但此频率比大多数应用程序所需的频率都要高。降低频率会提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY**

 尽管 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的 8 位偏移值，定义为原始数据，直接用于
 ARM Cortex-M4F NVIC 寄存器中，configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 是等效常量，其定义为仅使用 6 个优先级位，用于 XMC4000
 NVIC。
 提供这些值是因为 CMSIS 库函数 NVIC_SetPriority()
 需要未移位的 6 位格式。

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
Cortex-M 微控制器制造商会实现不同数量的优先级位，提供
预期以不同方式指定优先级的库函数。例如，
Infineon XMC4000 ARM Cortex-M4 微控制器上可以指定的最低优先级实际上为 63，这是由
FreeRTOSConfig.h 中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。

我们还建议确保将六个所有优先级位分配为
抢占式优先级位，并且不设置子优先级位，就和演示
中的一样。

每个移植都会将 'BaseType_t' 定义为对该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长类型。

#### 中断服务程序

与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
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
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。

#### FreeRTOS 使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

#### 抢占式内核和协同式 RTOS 内核之间的切换

将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
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

