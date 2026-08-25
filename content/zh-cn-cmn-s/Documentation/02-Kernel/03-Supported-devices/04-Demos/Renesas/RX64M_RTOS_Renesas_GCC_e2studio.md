---
title: "适用于 Renesas RX64M 的 FreeRTOS，使用 e2studio 支持 Renesas 和 GCC 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### 引言

本页面记录了 RTOS 演示应用程序，
针对含有 RXv2 核心的 [Renesas RX64M](http://www.renesas.com/products/mpumcu/rx/rx600/rx64m/index.jsp)
系列微控制器。

提供了两个 [e2studio](http://www.renesas.com/e2studio) 项目，
其中一个预配置为使用
[Renesas
编译器](http://am.renesas.com/products/tools/coding_tools/c_compilers_assemblers/rx_compiler/downloads.jsp)，另一个预配置为使用 [GCC 编译器](http://www.kpitgnutools.com/)。

两个 RTOS 项目都面向 RX64M RSK（Renesas 入门套件）评估板。

---

#### *重要提示！RX64M e2studio 演示项目使用说明*

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#构建并运行-renesas-rx64m-演示应用程序)
3. [RTOS 配置和使用详情](#rtos配置和使用详情)

另请参阅常见问题“[我的应用程序无法
运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

#### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，
因此包含的文件比 RX64M e2studio 项目所需文件多得多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解关于已下载文件的说明
和新项目创建的信息。

e2studio 项目采用常见的 Eclipse 项目名称 .project。
使用 Renesas 编译器的项目位于
FreeRTOS/Demo/RX600_RX64M_RSK_Renesas_e2studio 目录中。使用 GCC 编译器
的项目位于 FreeRTOS/Demo/RX600_RX64M_RSK_GCC_e2studio
目录中。在将项目导入
到 Eclipse工作区时，必须选择这些目录。

---

### 构建并运行 Renesas RX64M 演示应用程序

RTOS 演示项目可进行配置，以构建
简单的 "blinky" 项目，或全面的测试和演示应用程序。常量
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，定义于 main.c 的顶层，
用于在二者之间进行切换。如果将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
会创建全面的演示。
如果将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，会创建简单演示。

演示使用 RSK 开发板上内置的 LED，
因此无需进行硬件设置。

#### 使用 e2studio 进行构建

**注意：**e2studio 项目构建的某些
源文件包含在使用项目相对路径的项目中，因此，
如果 FreeRTOS 目录结构与 .zip 文件中的目录结构不同，则项目将无法构建。

1. 启动 e2studio Eclipse IDE，根据提示创建一个新的或
 选择一个现有的工作区。
2. 在 IDE 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "General->Existing Project into Workspace"，如下所示。

**首次点击 "Import" 时显示的对话框**
3. 在下一个对话框中，选择 FreeRTOS/Demo/RX600_RX64M_RSK_Renesas_e2studio 作为根目录，
 如果使用 Renesas 编译器。
 如果使用 GCC 编译器，请选择 FreeRTOS/Demo/RX600_RX64M_RSK_GCC_e2studio
 。
 确保在 "Projects" 区域中已勾选 RTOS 演示项目，
 并确保 “Copy Projects Into Workspace”
 未勾选，然后单击
 "Finish" 按钮(请参阅下图查看正确的复选框状态)。

![导入到 Eclipse CDT 时选择 RTOS 源代码](/media/2018/Import_RX64M_Project.png)

**确保已勾选 RTOSDemo，并且确保未勾选 "Copy projects into workspace"**
4. 打开 main.c，找到 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 的定义，
 它靠近文件的顶部。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，
 以构建简单的 blinky 风格（入门）项目。将
 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
 以构建全面测试和演示应用程序。
5. 从 e2studio Eclipse 的 "Project" 菜单中选择 "Build All" 以构建
 演示项目，并等待构建完成。
6. 确保在 RX64M RSK 硬件和运行 e2studio 的计算机之间连接 E1 调试适配器
 。如果
 按照下方图片配置启动配置，
 则无需提供任何外部电源。
7. 从 Eclipse 的 "Run" 菜单中选择 "Debug Configurations"
 以进行启动配置，
 用于对微控制器闪存进行编程并启动调试会话。按照下方图片所示方式，
 配置调试启动配置。

|  |  |  |  |
| --- | --- | --- | --- |
| [![](/media/2018/RX64M_Launch_Configuration_1.png)](/media/2018/RX64M_Launch_Configuration_1.png) | [![](/media/2018/RX64M_Launch_Configuration_2.png)](/media/2018/RX64M_Launch_Configuration_2.png) | [![](/media/2018/RX64M_Launch_Configuration_3.png)](/media/2018/RX64M_Launch_Configuration_3.png) | [![](/media/2018/RX64M_Launch_Configuration_4.png)](/media/2018/RX64M_Launch_Configuration_4.png) |

**点击图片放大**

### 演示应用程序功能

#### 简单 blinky 示例

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，会创建简单 blinky 示例。
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。

main() 会调用 main_blinky()：

* **main_blinky() 函数：** 

 main_blinky() 在启动调度器前会创建 RTOS 队列、
 队列发送任务和队列接收任务。
* **队列发送任务：** 

 队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。

 prvQueueSendTask() 每 200 毫秒向 RTOS 队列发送一次值 100。
* **队列接收任务：** 

 队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
 实现。

 prvQueueReceiveTask() 在数据到达 RTOS 队列前保持阻塞状态。
 每次从队列接收值 100 后会切换 LED 0。
 由于数据每 200 毫秒发送到队列，
 因此，LED 也将每 200 毫秒切换一次。

#### 全面测试和演示应用

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，将创建全面演示。
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中定义。

main() 会调用 main_full()：

* **main_full() 函数：** 

 main_full() 会创建一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)、一些特定的应用程序测试任务、
 测试任务和伪随机化程序任务，然后再启动调度程序。
 伪随机发生器任务只是用来在测试任务的执行顺序中加入一些变化，
 并以此
 来提高测试覆盖率。
* **"Reg Test" 任务：** 

 Reg Test 任务用于测试上下文切换机制，
 通过向 MCU 寄存器填入已知的值，然后连续检查每个
 寄存器在整个任务生命周期内是否保持其预期值。
* **"Check" 任务：** 

 "Check" 任务监测系统内所有其他任务的状态，
 寻找停滞的任务或报告错误的任务。
 每次被调用时，都会切换 LED 3。

 如果 LED 每 3 秒切换一次，
 未检测到任何停滞的任务或未收到任何错误报告。如果 LED
 每 200 毫秒切换一次，则至少发现了一个错误。
* **标准 "Flash" 任务：** 

 LED 0、LED 1 和 LED 2 由标准 "Flash" 任务控制。每个
 LED 将以不同的固定频率切换。

---

### RTOS配置和使用详情

#### RX64M RTOS 移植特定配置

此演示的特定配置项目位于 FreeRTOS/Demo/RX600_RX64M_RSK_Renesas_e2studio/Source/FreeRTOSConfig.h
中（针对 Renesas 编译器），GCC 编译器项目位于 FreeRTOS/Demo/RX600_RX64M_RSK_GCC_e2studio/src/FreeRTOSConfig.h 中
。您可以根据应用程序的需求，
编辑此文件中定义的常量。特别是：

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS tick 的频率。提供的数值 1 KHz 可用于
 测试 RTOS 内核功能，但比大多数应用程序所需的频率更快。降低该频率有助于提高效率。
* **configKERNEL_INTERRUPT_PRIORITY**
 定义了 RTOS 内核用于定时器和软件中断的中断优先级。
 应始终将其设置为
 最低中断优先级，在 RX64M 中为 1。请参[阅配置页面](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，了解详细信息。
* **configMAX_SYSCALL_INTERRUPT_PRIORITY**
 此常量定义了可以调用 RTOS API 函数的
 。处于或低于此优先级的中断可以调用 FreeRTOS API
 函数，**前提是**该 API 函数以 "FromISR" 结尾。
 高于此优先级的中断不能调用任何 FreeRTOS API 函数，
 但不会受到 RTOS 内核正在执行的任何操作的影响。这使得它们
 适用于需要非常高时间精度的功能
 （例如电机控制）。

RX64M 移植层使用 #define 将 "BaseType_t" 定义长整型。

#### 编写中断服务程序 (ISR)

可以使用标准编译器语法编写中断。下面
提供了 Renesas 和 GCC 编译器的示例。

通常，ISR 希望触发上下文切换，因此
ISR 完成时返回的任务就与 ISR 最初中断的任务不同。如果 ISR 导致某个任务解除阻塞，
并且被解除阻塞的任务与已处于运行状态的任务相比具有更高的优先级，
就属于这种情况。这
可以通过调用 portYIELD_FROM_ISR() 来实现，该函数采用单个参数。
如果不需要上下文切换，则参数必须为 0；如果需要上下文切换，则参数必须为非零。
下方示例中使用的是 portYIELD_FROM_ISR()
。

|  |
| --- |
| <br/>```c< br/> < br/>/* Pragma used to install the interrupt. The 'enable' used in the pragma<br/>tells the compiler to enable interrupts before executing the user code. */<br/>#pragma interrupt ( Excep_PERIB_INTB128( vect = 128, enable ) )<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Interrupts are already enabled here. See comment above. */<br/><br/>    /* [xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the semaphore has already been created. If giving the semaphore<br/> unblocks a task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the xSemaphoreGiveFromISR()<br/> function. */<br/>    xSemaphoreGiveFromISR( xSemaphore, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**使用 Renesas 编译器语法的中断服务程序示例** <br/><br/> |

|  |
| --- |
| <br/>```c<br/><br/>/* The function prototype uses the interrupt attribute. */<br/>static void vT0_1_InterruptHandler( void ) __attribute__((interrupt));<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Unlike when using the Renesas compiler, interrupts must be explicitly<br/> re-enabled inside the interrupt service routine. */<br/>    __asm volatile( "SETPSW	I" );<br/><br/><br/>    /* [xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the semaphore has already been created. If giving the semaphore<br/> unblocks a task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the xSemaphoreGiveFromISR()<br/> function. */<br/>    xSemaphoreGiveFromISR( xSemaphore, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**使用 GCC 编译器语法的中断服务程序示例** <br/><br/> |

#### FreeRTOS 使用的资源

FreeRTOS 需要独占使用软件中断。
FreeRTOS 还需要独占使用定时器，该定时器能够生成周期性嘀嗒中断，但是
要由应用程序编写者定义使用哪个定时器。要做到这一点
应用程序必须定义一个名为 vApplicationSetupTimerInterrupt() 的函数，
然后将 vTickISR() 安装
到中断向量表内的相应位置。

建议使用比较匹配定时器来生成 tick 中断，
例如，vApplicationSetupTimerInterrupt() 的实现使用了比较匹配定时器 0，
包含在此演示应用程序的 main.c 中。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

RX64M 演示应用程序项目中内置 Source/Portable/MemMang/heap_4.c，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。
