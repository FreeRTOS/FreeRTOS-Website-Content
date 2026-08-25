---
title: "使用 GCC 和基于 IDE 的 Atollic TrueStudio Eclipse 的 STM32F100 ARM Cortex-M3 FreeRTOS 演示"
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
| <br />![](/media/2018/FreeRTOS-running-on-a-SMT32-value-line-STM32F100-discovery-board.jpg)<br /> |

### 引言

这个简单的演示项目在 [STM32 Discovery 板](http://www.st.com/stm32-discovery)上运行，
该板装有 [STM32F100RB](http://www.st.com/internet/mcu/product/216844.jsp)
Cortex-M3 微控制器，由 [STMicroelectronics](http://www.st.com/) 提供。

其低成本使得 Discovery 板成为理想的评估平台，但 8K
的可用 RAM 也意味着可演示的 FreeRTOS 内核功能数量
有限。因此，这个简单的演示仅积极
演示了任务、队列、软件定时器和中断功能。该演示还
配置为包括 malloc 失败、空闲和堆栈溢出挂钩
函数。

FreeRTOS 下载内容包括其他功能更全面的演示应用程序，
适用于 STM32 微控制器系列中的大型部件。

演示已经过预先配置，可使用免费版本的

[Atollic TrueStudio for STM32](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html) 基于 Eclipse 的
IDE，以及 FreeRTOS GCC 移植。

---

### *重要提示！使用 STM32F100 ARM Cortex-M3 演示的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未
运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码，因此
包含的文件比此演示所需更多的文件。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
了解关于已下载文件的说明
和新项目创建的信息。

适用于 FreeRTOS STM32 Discovery 板演示的 TrueStudio 项目位于
FreeRTOS/Demo/CORTEX_STM32F100_Atollic 目录下。此项目
应该导入到 TrueStudio 工作区。下文
[准备 Eclipse 项目](#构建和运行演示应用程序)部分
描述了关于设置演示项目目录，
以及将演示项目导入到 TrueStudio 中的重要信息。

---

### 演示应用程序

### 演示应用程序硬件设置

演示使用的 LED 和按钮均集成于 STM32 Discovery
主板硬件上。因此，无需进行硬件设置。

### 准备 TrueStudio (Eclipse) 项目目录

Eclipse 项目既可以是标准 makefile 项目，也可以是托管 make 项目。
STM32F100 项目使用托管 make 项目。因此意味着
以下两种情况：

1. 构建项目所需的所有源文件必须位于
 包含项目文件本身的文件夹/目录，或
2. 需要配置 Eclipse 工作区（注意是工作区，而非项目）
 来定位硬盘上其他位置的文件。

本示例采用第一种。为此，目录 FreeRTOS/Demo/CORTEX_STM32F100_Atollic
包含一个名为 CreateProjectDirectoryStructure.bat 的批处理文件，
该文件会将所有必需的 FreeRTOS 源文件复制到
演示项目目录内的子目录中。

**CreateProjectDirectoryStructure.bat 必须在将 TrueStudio
 项目导入 Eclipse 工作区之前执行**。 

CreateProjectDirectoryStructure.bat 不能在
在 TrueStudio Eclipse IDE 中执行。

### 将演示应用程序项目导入 TrueStudio Eclipse 工作区

要将 STM32 TrusStudio 项目导入现有或新的 Eclipse 工作区：
1. 从 TrueStudio 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "Existing Projects into Workspace"。  

![将 STM32 TrueStudio 项目导入 Eclipse 工作区](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)

**首次点击 "Import" 时显示的对话框**
2. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_STM32F100_Atollic
 作为根目录。然后，确保在 "Project" 区域已勾选 FreeRTOS-Simple-Demo 项目，
 **并确保未勾选 "Copy Projects Into
 Workspace" 选项**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态，
 图片中不包含 "Finish" 按钮）。

![选择要导入 Eclipse 的 FreeRTOS STM32 项目](/media/2018/selecting-the-FreeRTOS-STM32-project-to-import-into-Eclipse.jpg)

**确保已勾选 FreeRTOS-Simple-Demo，且不勾选 "Copy projects into workspace"**

### 构建和运行演示应用程序

1. 使用标准 USB 线将 STM32 Discovery 板连接到主机。系统可能会提示您安装某些 USB 驱动器。
2. 确保 CreateProjectDirectoryStructure.bat 已执行，
 并确保项目已正确导入到 Eclipse 工作区。
3. 在 IDE 的 "Project" 菜单中选择 "Rebuild All"。
4. 在 IDE 的 “Run” 菜单中选择 "Debug"。如果调试会话启动，则进程完成。如果调试会话未启动，请按照此列表中的其余说明操作。
5. 有时，在第一次调试之前需要创建调试配置。从 IDE 的 "Run" 菜单中选择 "Debug Configurations..."。
6. 在出现的对话框中，单击 "New Launch Configuration" 速度按钮，如下图中红色突出显示部分。
7. 一个新的调试配置将被创建，出现的对话框应如下图所示。单击 "Debug" 按钮开始调试。

![创建 STM32 Value Line Discovery 板调试配置](/media/2018/Creating-the-STM32-Discovery-board-debug-configuration.jpg)

**用于创建调试启动配置的对话框，在按下   
"New Launch Configuration" 速度按钮（红色突出显示部分）后出现。**

### 功能

* **空闲钩子函数：** 

 空闲钩子函数会查询 FreeRTOS 堆空间的剩余量
 （见 main.c 中定义的 vApplicationIdleHook()）。演示
 应用程序被配置为使用 7K RAM (可用为 8K) 作为 FreeRTOS 堆。
 在初始化过程中内存仅从此堆分配，并且此演示
 实际上仅使用 1.6K 字节（共配置 7K 可用堆空间），剩下 5.4K
 字节的堆空间未被分配。
* **main() 函数：** 

 main() 会创建一个软件定时器、一个队列和两个任务。然后它会启动
 调度器。
* **队列发送任务：** 

 队列发送任务由 main.c 中的 prvQueueSendTask() 函数实现。
 prvQueueSendTask() 处于一个循环中，它会反复阻塞
 200 毫秒，然后才发送值 100 至
 main() 中创建的队列。一旦值发送成功，任务就会再次循环，
 再次被阻塞 200 毫秒。
* **队列接收任务：** 

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现。
 prvQueueReceiveTask() 位于一个循环中，
 它会反复阻塞试图从队列中读取数据的操作，该队列创建于 main () 中。接收到数据时，
 任务会检查数据的值，如果该值等于
 预期的 100，则切换绿色 LED。传递给队列接收函数的“阻塞时间”参数规定，
 此任务应当无限期地保持在“已阻塞”状态，
 直到队列上有可用数据为止。只有当
 队列发送任务写入队列时，队列接收任务才会解除“已阻塞”
 。由于队列发送任务每 200 毫秒向队列写入一次，
 队列接收任务每 200 毫秒解除一次“已阻塞”状态，
 因此绿色 LED 每 200 毫秒切换一次。
* **LED 软件定时器和按钮中断：** 

 将用户按钮 B1 配置为每次按下后生成一个中断
 。中断服务程序会打开红色 LED，并重置
 LED 软件定时器。该 LED 定时器的周期为 5000 毫秒（5 秒），并且
 会使用回调函数，该函数被定义为仅关闭红色 LED。
 因此，按下用户按钮将开启红色 LED，并且 LED 将
 保持开启状态，持续 5 秒（如果不按下按钮）。

---

### RTOS 配置和使用详情

### RTOS 移植特定配置

这些演示的特定配置项位于 FreeRTOS/Demo/CORTEX_STM32F100_Atollic/Simple_Demo_Source/FreeRTOSConfig.h 中。您可
编辑 FreeRTOSConfig.h 中定义的常量，使其适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 此常量可用于设置 RTOS 滴答中断的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 有关这些配置常量的完整信息，请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档。

注意！请务必牢记 ARM Cortex-M3 核心使用的
数字越小表示中断优先级越高。这
似乎有悖直觉，而且很容易忘记！如果希望
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值），
因为这实际上可能会导致该中断在系统中具有最高优先级，
因此，如果此优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能导致系统崩溃。另外，请勿忘记
分配中断优先级，因为默认情况下，中断优先级为 0，
这可能导致其处于最高优先级。

ARM Cortex-M3 核心的最低优先级实际上是 255，但是不同的
Cortex-M3 供应商实现了不同数量的优先级，
并提供了期望以不同方式指定优先级的库函数。例如，
在 STM32 上，您可以在 ST 驱动函数库调用中指定的最低优先级
实际上是 15，这是由常量
configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的，它位于 FreeRTOSConfig.h。可指定的最高优先级
始终为零。

我们还建议您确保将所有四个优先级位
都设置为抢占式优先级位。要确保如此，可以将
"NVIC_PriorityGroup_4" 传递到 ST 库函数 NVIC_PriorityGroupConfig() 中。
在演示项目中，这是由函数 prvSetupHardware() 完成的，
它在 main.c 中定义。

每个端口将 #defines 'BaseType_t' 定义为对处理器来说
。此移植将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

与大多数移植不同，导致上下文切换的中断服务程序
没有特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 中请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

此演示项目提供了中断服务程序示例，
即 main.c 中定义的 EXTI0_IRQHandler()。

请注意，以下行包括在 FreeRTOSConfig.h 中：

```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler

```

这些定义将 FreeRTOS 内核中断处理程序函数名映射到
CMSIS 中断处理程序函数名上；如此一来，无需任何修改，
就可以使用 Atollic 提供的链接器脚本和启动文件。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_STM32F100_Atollic/Simple_Demo_Source/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1 即可使用抢占式机制，或设置为 0
即可使用协同式机制。

### 内存分配

Source/Portable/MemMang/heap_1.c 包含在 ARM Cortex-M3 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
