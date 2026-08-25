---
title: "支持 IAR、Keil、GCC 和 Tasking 编译器的 Infineon XMC4000 ARM Cortex-M4F 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[XMC4000](http://www.infinion.com/xmc4000/)]
[[Cortex-M4F](http://www.arm.com/products/processors/cortex-m/cortex-m4-processor.php)]
[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Infineon XMC4500 Hexagon 开发套件 CPU 板](/media/2018/Infineon-XMC4000-Cortex-M4-Hexagon-kit.jpg)

### 简介

此页面记录的演示应用程序面向 ARM Cortex-M4F 微控制器的 Infineon XMC4000
系列。

此演示为以下 ARM Cortex-M4 编译器提供了预配置项目：

* [适用于 ARM 的任务 VX-toolset](http://www.tasking.com/products/arm/)
* [IAR](http://www.iar.com/ewarm)
* [GCC](https://launchpad.net/gcc-arm-embedded)（使用 [DAVE](https://www.infineon.com/cms/en/product/microcontroller/legacy-microcontroller/xc800-development-tools-software-and-kits/) Eclipse 项目）
* [ARM Keil](http://www.keil.com/arm/mdk.asp)

四个项目每个均包含三个构建配置，
每个构建配置均针对以下 XMC4000 Hexagon 应用程序套件中的一个：

* [XMC4500 Hexagon](https://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-cortex-m/32-bit-xmc4000-industrial-microcontroller-arm-cortex-m4/)
* [XMC4400 Hexagon](http://www.infineon.com/cms/en/product/channel.html?channel=db3a30433cd75ebf013cf6cc170d2ddd)
* [XMC4200 Hexagon](http://www.infineon.com/cms/en/product/channel.html?channel=db3a30433cd75ebf013cf6e3d83c2e88)

各构建配置均可编译以创建简单的 blinky 演示，
或全面的测试和演示应用程序。构建说明见下文
。

![FreeRTOS 内核感知调试器，可与 IAR 编译器结合使用](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)

 FreeRTOS 状态查看器插件的屏幕截图

 该插件为 IAR IDE 附带

**注意 1：**FreeRTOS 下载中的项目包括特殊设置，
目的是解决 XMC4000 芯片勘误表。请参阅
[构建说明](#构建和运行-arm-cortex-m4f-rtos-应用程序)，
了解各编译器的更多信息。

**注意 2：**IAR 项目将无法构建并会损坏（因此无法再
与任何 IAR 版本一起使用）的情况为：打开该项目的 EWARM 版本比
最初创建项目时所用版本更低。
。

---

### *重要！使用 XMC4000 ARM Cortex-M4F 演示的注意事项*

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序功能)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法
运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，
因此包含的文件远多于 XMC4000 演示所需的文件。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
了解关于已下载文件的说明
和创建新项目的信息。

* IAR 嵌入式工作区项目称为 RTOSDemo.eww，位于
 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_IAR 目录下。
* Keil 项目称为 RTOSDemo.uvproj，位于
 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_Keil 目录下。
* Dave 项目采用常见的 Eclipse 项目名称 .project，
 位于 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_GCC_Dave
 目录下。
* Tasking 项目采用常见的 Eclipse 项目名称 .project，
 位于 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_GCC_Tasking
 目录下。

---

### 构建和运行 ARM CORTEX-M4F RTOS 应用程序

RTOS 演示项目可进行配置，以构建
简单的 "blinky" 项目，或全面的测试和演示应用程序。常量
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，定义于 main.c 的顶层，
用于在二者之间进行切换。如果将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则会创建简单演示。
如果将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
则会创建全面示例。

演示使用内置在每个 Hexagon 应用程序套件板上的 LED，
因此不需要任何硬件设置。

XMC4200 和 XMC4400 Hexagon 套件具有内置的 J-Link 调试器接口。这些板
可以通过 USB 线直接连接到主计算机，
无需其他连接。这些 Hexagon 板各有两个 USB 连接器，
因此需小心使用标记着“调试 USB” 的连接器。

XMC4500 Hexagon 套件没有内置的 J-Link，
因此需要两个连接：

1. 为调试器提供接口的连接：

 连接一个外部调试器接口，
 使其介于主计算机和 XMC4500 Hexagon 印刷电路板的两个调试端口中的一个之间。由于所提供的
 项目被配置为使用 J-Link，因此如果使用任何其他
 兼容设备，将需要对项目选项进行
 适当更新。
2. 为硬件提供电源的连接：

 请在 XMC4500 Hexagon 印刷电路板的 USB OTG 连接器和任何方便的 USB 主机之间
 连接一条 USB 电缆线。

以下各小节提供了四个
支持 ARM CORTEX-M4 编译器的使用说明。

1. [使用 IAR Embedded Workbench 构建](#使用-iar-embedded-workbench-构建)
2. [使用 ARM Keil 构建](#使用-arm-keil-构建)
3. [使用 DAVE Eclipse IDE 与 ARM GCC 构建](#使用-dave-eclipse-ide-与-arm-gcc-构建)
4. [使用 Tasking ARM VX-toolset 构建](#使用-tasking-arm-vx-toolset-构建)

#### 使用 IAR Embedded Workbench 构建

**注意：**如果目前使用的 XMC4000 设备包含勘误表号 PMC_001，
则必须在 FreeRTOSConfig.h 中将 WORKOUND_PMU_CM001 定义（#define）为 1，
在启动文件中也进行同样的设置。FreeRTOS 下载中的项目已包含
这些设置。
1. 打开 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_IAR/RTOSDemo.eww
 （位于 IAR Embedded Workbench IDE 中）。
2. 为目标硬件的构建配置设置正确选项。
 为 XMC4200、XMC4400 和 XMC4500 Hexagon 应用程序套件
 提供了构建配置。使用 EWARM IDE 工作区窗口顶部的下拉列表
 设置活动构建配置。
3. 从 IAR Embedded Workbench 的 "Project" 菜单中选择 "Rebuild All"（或按 F7）
 以构建演示项目。
4. 从 IAR Embedded Workbench 的 "Project" 菜单中选择 "Download and Debug"，
 对微控制器闪存进行编程并启动调试会话
 。

#### 使用 ARM Keil 构建

**注意：**如果目前使用的 XMC4000 设备包含勘误表号 PMC_001，
则必须在 FreeRTOSConfig.h 中将 WORKOUND_PMU_CM001 定义（#define）为 1，
在启动文件中也进行同样的设置。FreeRTOS 下载中的项目已包含
这些设置。
1. 在 Keil IDE 中打开 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_Keil/RTOSDemo.uvproj
 。
2. 为目标硬件的构建配置（在 Keil IDE 中称为*目标*）
 设置正确选项。
 为 XMC4200、XMC4400 和 XMC4500 Hexagon 应用程序套件
 提供了构建配置。活动构建配置通常
 显示在 IDE 菜单工具栏的下拉列表中。
3. 从 Keil 的 "Project" 菜单中选择 "Rebuild Target"（或按 F7）来构建
 演示项目。
4. 从 Keil 的 "Project" 菜单中选择 "Start/Stop Debug Session"，
 对微控制器闪存进行编程并启动调试会话
 。

#### 使用 DAVE Eclipse IDE 与 ARM GCC 构建

**注意：**如果目前使用的 XMC4000 设备包含勘误表号 PMC_001，
则必须在 FreeRTOSConfig.h 中将 WORKOUND_PMU_CM001 定义（#define）为 1，
在启动文件中也进行同样的设置。FreeRTOS 下载中的项目已包含
这些设置。
1. 执行 CreateProjectDirectoryStructure.bat
 批处理文件（位于 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_GCC_Dave
 目录下），**然后再打开项目**。
 该操作会将所需的文件复制到本地目录中。
2. 启动 DAVE Eclipse IDE，根据提示创建一个新的或选择一个现有的
 工作区。
3. 在 IDE 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "General->Existing Project into Workspace"，如下所示。

![将 ARM CORTEX-M4 RTOS 演示项目导入 DAVE Eclipse IDE](/media/2018/Importing-the-STM32-TrueStudio-project-into-the-Eclipse-workspace.jpg)

**首次点击 "Import" 时显示的对话框**
4. 在下一个对话框中，选择 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_GCC_Dave
 作为根目录。确保在 "Projects" 区域中已勾选 RTOS 演示项目，
 **并且确保未勾选 'Copy Projects Into
 Workspace' 复选框**，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。

![导入到 Eclipse CDT 时选择 RTOS 源代码](/media/2018/Selecting_RTOSDemo_In_Eclipse.jpg)

**确保已勾选 RTOS 演示，并且确保未勾选 "Copy projects into workspace"**
5. 导入项目后，右键单击 DAVE Eclipse 项目资源管理器窗口中的项目名称，
 然后在弹出菜单中选择
 "Build Configurations->Set Active"，
 为目标硬件的构建配置设置正确选项。
 为 XMC4200、XMC4400 和 XMC4500 Hexagon 应用程序套件
 提供了构建配置。
6. 从 DAVE Eclipse "Project" 菜单中选择 "Rebuild Project"
 以构建演示项目。
7. 从 Eclipse 的 "Run" 菜单中选择 "Debug"，
 以进行启动配置，
 用于对微控制器闪存进行编程并启动调试会话。

**注意：** 
 在撰写本文时，DAVE 项目中的每个构建配置
 必须针对完全相同的微控制器部件号。然而，在交付的构建配置中
 可选择包含和排除芯片特定文件，
 因此项目会正确构建，
 尽管在启动调试会话时还需要额外的步骤；请检查调试启动
 配置，以确保配置适用于实际使用的硬件
 （请参阅下图）。调试会话启动时，调试器可能也会发出警告，
 只要启动配置是针对所使用的硬件正确配置的，
 就可以忽略这个警告
 。

![在 DAVE 中选择 ARM core](/media/2018/Selecting_The_Target_In_DAVE.jpg)

**在调试启动配置中选择目标**

#### 使用 Tasking ARM VX-toolset 构建

**注意：**如果目前使用的 XMC4000 设备包含勘误表号 PMC_001，
则链接器宏 SILICON_BUG_PMC_CM_001 必须在项目设置中。
FreeRTOS 下载中的项目已包含此设置。

1. 执行 CreateProjectDirectoryStructure.bat
 批处理文件（位于 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_GCC_Tasking
 目录下），**然后再打开项目**。
 该操作会将所需的文件复制到本地目录中。
2. DAVE 和 Tasking 都使用 Eclipse IDE，
 因此您可以[按照使用 DAVE 构建应用程序的说明](#使用-dave-eclipse-ide-与-arm-gcc-构建)，
 确保将项目导入 Eclipse 中，
 项目位于 FreeRTOS/Demo/CORTEX_M4F_Infineon_XMC4000_GCC_Tasking
 目录下。

### 演示应用程序功能

#### 简单 blinky 示例

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，会创建简单 blinky 示例。
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。

main() 会调用 main_blinky()：

* **The main_blinky() 函数：** 

 main_blinky() 在启动调度器前会创建队列、队列发送任务和队列接收任务
 。
* **队列发送任务：** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。

 prvQueueSendTask() 每 200 毫秒向  队列发送一次值 100。
* **队列接收任务：** 

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 实现。

 prvQueueReceiveTask() 在数据达到队列前保持阻塞状态。
 每次从队列接收值 100 后会切换 LED。
 每 200 毫秒发送数据至队列时，
 因此，LED 也将每 200 毫秒切换一次。

#### 全面测试和演示应用

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，将创建全面演示。
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。

main() 会调用 main_full()：

* **main_full() 函数：** 

 main_full() 创建了一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview) ，一些应用特定
 测试任务和一个定时器，然后再启动调度器。
* **“寄存器测试”任务：** 

 Reg Test 任务用于测试上下文切换机制，
 通过向 MCU 寄存器填入已知的值，然后连续检查每个
 寄存器在整个任务生命周期内是否保持其预期值。
* **“检查”软件定时器：** 

 “检查”软件定时器会监控系统中所有其他任务的状态，
 寻找停滞的任务或报告错误的任务。
 它每次被调用时都会切换 LED。

 如果 LED 每 3 秒切换一次，则表示检查任务
 未检测到任何停滞的任务或未收到任何错误报告。如果 LED
 每 200 毫秒切换一次，则表示至少发现了一个错误。

---

### RTOS 配置和使用详情

#### 中断服务程序

导致上下文切换的中断服务程序
无特殊要求。
portEND_SWITCHING_ISR() 宏可用于从 ISR 内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

在
main.c 的末端提供了名为 Dummy_IRQHandler() 的示例中断处理程序作为参考实现。
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
Infineon ARM Cortex-M4 微控制器上可以指定的最低优先级实际上为 63，这是由
FreeRTOSConfig.h中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义的。可指定的最高优先级
始终为零。

我们还建议确保将所有优先级位分配为
指定为抢占式优先级位，并且没有设置子优先级位，就像演示
中的一样。

请注意，FreeRTOSConfig.h 中包含了以下行，目的是将 FreeRTOS
中断处理程序函数映射到 CMSIS 中断处理程序函数名称上。
这使编译器工具供应商提供的链接器脚本可
在无需修改的情况下使用。

```c

	#define vPortSVCHandler      SVC_Handler
	#define xPortPendSVHandler   PendSV_Handler
	#define xPortSysTickHandler  SysTick_Handler

```

#### RTOS 移植特定配置

这些演示的特定配置项目位于 FreeRTOSConfig.h
文件中，该文件位于项目文件所在的目录。您可以
编辑 FreeRTOSConfig.h 中定义的常量，使其适合您的应用程序。尤其是以下常量：

* **configTICK_RATE_HZ**
 此常量设置了 RTOS 滴答中断的频率。提供的 500Hz 值可用于
 测试 RTOS 内核功能，但比大多数应用程序要求的速度更快。
 降低此值可提高效率。

每个移植都将 "BaseType_t" 定义为对该处理器而言最有效的数据类型
。所有 ARM Cortex-M4F 移植都将 BaseType_t 的类型定义为 long。

请注意 vPortEndScheduler() 尚未实现。

#### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM CORTEX-M4F 演示应用程序项目中，用以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。

