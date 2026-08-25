---
title: "使用 GCC，针对 LPCXpresso 硬件和 IDE 的 NXP LPC1114 ARM Cortex-M0 演示"
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
| <br />![](/media/2018/LPCXpresso-LPC1114.jpg)<br /> |

### 引言

本页所述项目演示了 FreeRTOS ARM CORTEX-M0 GCC 移植。
该项目配置是为了在 [LPC1114](http://ics.nxp.com/products/lpc1000/all/~LPC1114/) 版本的
[LPCXpresso 开发板](http://ics.nxp.com/lpcxpresso/)上运行，使用基于 Eclipse 的免费
[LPCXpresso IDE](https://www.nxp.com/design/design-center/development-boards-and-designs/lpcxpresso-boards:LPCXPRESSO-BOARDS)。

使用编译时间选项（如下所述） ，可以将项目配置为
创建基本 blinky 风格的演示，或配置为创建更全面的测试和演示应用程序
（其中包括执行中断嵌套行为的任务）。

[![与 LPCXpresso 一起使用的 FreeRTOS 内核感知调试器](/media/2018/LPCXpresso-FreeRTOS-kernel-aware-debugger.jpg)](/media/2018/LPCXpresso-FreeRTOS-kernel-aware-debugger.jpg)

 FreeRTOS 感知状态查看器的屏幕截图

 LPCXpresso IDE 标准装附带的

 插件。**点击图像放大**。

---

### *重要提示！使用 LPC1114 LPCXpresso ARM Cortex-M0 演示的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法
运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，
因此其中包含的文件远比演示所需的文件多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
了解关于已下载文件的说明
和新项目创建的信息。

FreeRTOS 演示应用程序依赖于 CMSIS 库，
该库已作为单独的 LPCXpresso 项目提供。演示应用程序项目和 CMSIS 项目
都必须导入到 LPCXpresso 工作区中。两个项目均位于
FreeRTOS/Demo/CORTEX_M0_LPC1114_LPCXpresso 目录的子目录中，
可一并导入 LPCXpresso 。下面的
[准备 Eclipse 项目](#构建和运行演示应用程序)部分
包含关于如何设置演示项目目录
并将演示项目导入 LPCXpresso IDE 的重要信息。

---

### 演示应用程序

#### 演示应用程序硬件设置

该演示采用了集成在 LPCXpresso 开发板上的 LED ，
因此不需要任何硬件设置。

#### 准备 Eclipse 项目目录

Eclipse 项目既可以是标准 makefile 项目，也可以是托管 make 项目。
FreeRTOS LPCXpresso ARM CORTEX-M0 项目使用托管 make 项目。这
反过来又意味着：

1. 构建项目所需的所有源文件必须位于
 包含项目文件本身的文件夹/目录，或
2. 需要配置 Eclipse 工作区（注意是工作区，而非项目）
 来定位硬盘上其他位置的文件。

此演示采用上方的选项 1。因此，目录 FreeRTOS/Demo/CORTEX_M0_LPC1114_LPCXpresso/RTOSDemo
包含一个名为 CreateProjectDirectoryStructure.bat 的批处理文件，
该文件将所需的所有 FreeRTOS 源文件和一些标准的演示应用程序文件
复制到演示项目目录下的子目录中。

**CreateProjectDirectoryStructure.bat 必须在将 LPCXpresso
 项目导入 Eclipse 工作区之前执行**。

CreateProjectDirectoryStructure.bat 不能在
在 LPCXpresso IDE 内部执行。

#### 将演示应用程序和 CMSIS 项目导入 LPCXpresso Eclipse 工作区

要想将必要的项目导入现有或新的 Eclipse 工作区：
1. 在 LPCXpresso 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "Existing Projects into Workspace"。  

![将 ARM CORTEX-M0 项目导入 Eclipse 工作区](/media/2018/Importing-an-existing-project-into-LPCXpresso.jpg)

**首次单击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_M0_LPC1114_LPCXpresso
 作为根目录。然后，确保在 “Projects” 区域勾选了 RTOSDemo 和 CMSISv2p00_LPC11xx 项目，
 **并确保未勾选 "Copy Projects Into
 Workspace" 复选框**，
 然后才能单击 "Finish" 按钮(若要查看正确的复选框状态，请参阅下图)。

![选择要导入到 Eclipse 的 ARM Cortex-M0 RTOSDemo 和 CMSIS 项目](/media/2018/Selecting-the-Cortex-M0-RTOSDemo-and-CMSIS-projects.jpg)

**确保两个项目都已选中，并且 "Copy projects into workspace" 未勾选**

#### 构建和运行演示应用程序

单个 RTOSDemo 项目提供了两种配置。可配置
为简单的 blinky 风格的项目，或配置为更全面的测试和演示应用程序。main.c 中的
main.c 中的 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
设置用于在两者之间进行选择。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，
以创建基本的 "Blinky" 风格演示。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
以创建更全面的测试和演示应用程序。

1. 设置 mainCREATE_SIMPLE_Blinky_DEMO_ONLY 常量以生成所需的演示功能，如上所述。
2. 使用标准 USB 缆线将 LPCXpresso LPC1114 开发板连接到您的主机。系统可能会提示您安装某些 USB 驱动器。
3. 确保 CreateProjectDirectoryStructure.bat 已执行，且项目已正确导入 Eclipse 工作区。
4. 在 IDE 的 "Project" 菜单中选择 "Build All" 后， CMSIS 和 RTOSDemo 项目都应当正确构建，无报错或警告。
5. 按下 "Debug" 速度按钮，或在 IDE 的快速启动面板中按下 "Debug 'RTOSDemo'" 按钮，可启动调试会话。程序将写入微控制器闪存，并且调试器将在进入 main() 函数时中断。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

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
 预期值 100，则切换 LED。传递给队列接收函数的“阻塞时间”参数规定，
 此任务应当无限期地保持在“已阻塞”状态，
 直到队列上有可用数据为止。只有当
 队列发送任务写入队列时，队列接收任务才会解除“已阻塞”
 。由于队列发送任务每 200 毫秒向队列写入一次，
 队列接收任务每 200 毫秒解除一次“已阻塞”状态，
 因此 LED 每 200 毫秒切换一次。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 会导致 main() 调用 main_full()。
main_full() 会创建更全面的测试和演示应用程序，
请参阅下文。

* **main_full() 函数：** 

 main_full () 创建一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)（包括一组
 测试中断嵌套行为的任务），一些应用程序专用的
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
 任务已停顿，或报告了错误，便会将
 检查定时器的周期从最初的三秒钟更改为仅 200 毫秒。每次调用回调函数时，
 也会切换 LED。这可直观体现
 系统状态指示：**如果 LED 每三秒切换一次，
 则表示未发现任何问题。如果 LED 每 200 毫秒切换一次，则表示
 已发现至少一个任务存在问题**。

---

### RTOS 配置和使用详情

#### 中断服务程序

导致上下文切换的中断服务程序
无特殊要求。
portEND_SWITCHING_ISR() 宏可用于从 ISR 内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

中断嵌套测试任务要求配置两个定时器，
以生成中断。中断服务例程在
IntQueueTimer.c 中定义，并且可用作应用程序编写器的示例。但是，
此类任务不能直接演示 FreeRTOS 安全 API 函数的使用
（函数以 "FromISR" 结尾）。因此，在 main.c 的末尾
提供了名为 Dummy_IRQHandler() 的虚拟中断实现，并复制于下文。

```c

void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. Only FreeRTOS API functions
 that end in "FromISR" can be called from an ISR. */
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
CMSIS 中断处理程序函数名中（或是未修正的向量表中使用的任何名称，向量表由编译器提供）。这样，
就可以使用 Code Red 提供的链接器脚本和启动文件，且不加修正。

请注意！请参阅[专门介绍如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。请记住，ARM Cortex-M 核心中，
数字越小，中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值），
（或其他低数字值），因为这会导致该中断在系统中
实际上具有最高优先级。另外，请勿忘记指定中断优先级，
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

#### RTOS 移植专用配置

这些演示的特定配置项目包含在 FreeRTOS/Demo/CORTEX_M0_LPC1114_LPCXpresso/RTOSDemo/Source/FreeRTOSConfig.h 中。main.c 顶部的
编辑 FreeRTOSConfig.h 中定义的常量，使其适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 此常量可用于设置 RTOS 滴答中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但比大多数应用程序要求的速度更快。
 降低此值可提高效率。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
。此移植将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_M0_LPC1114_LPCXpresso/RTOSDemo/Source/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为1，可使用抢占式调度；
设置为0，可使用协同式调度。

#### 内存分配

Source/Portable/MemMang/heap_1.c 包含在 ARM Cortex-M0 演示应用程序项目中，用于
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
