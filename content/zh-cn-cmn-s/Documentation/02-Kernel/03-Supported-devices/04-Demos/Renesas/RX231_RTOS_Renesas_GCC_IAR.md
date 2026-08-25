---
title: "适用于 Renesas RX231 (RXv2) 的 FreeRTOS 支持 GCC、IAR 和 Renesas 编译器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Renesas RX231 RXv2 内核](/media/2018/Renesas_Generic.jpg)

### 简介

本页介绍了 RTOS 演示应用
[Renesas RX231](http://www.renesas.eu/products/mpumcu/rx/rx200/rx231/index.jsp)
该系列微控制器采用 RXv2 内核。

提供了如下三个项目：

1. [e2studio](http://www.renesas.com/e2studio) 项目，
 该项目使用 GCC 编译器。
2. [e2studio](http://www.renesas.com/e2studio) 项目，
 该项目使用 Renesas 编译器。
3. [IAR Embedded Workbench](https://www.iar.com/products/architectures/renesas/iar-embedded-workbench-for-renesas-rx/) 项目，
 该项目使用 IAR 编译器。

所有三个项目都包含允许创建简单的 blinky 演示或综合演示的构建选项，
适用于 RX231 RSK (Renesas Start Kit) 评估
板。

---

### *重要提示！RX231 RTOS 演示项目的使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序功能)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未
运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 RTOS 移植的源代码，
所以包含的文件数量超过了 RX231 项目的要求。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，
。

IAR 项目称为 RTOSDemo.eww，位于
/FreeRTOS/Demo/RX200_RX231-RSK_GCC_e2studio_IAR 目录下。

e2studio 项目采用常见的 Eclipse 项目名称 .project。
使用 GCC 编译器的项目也位于
/FreeRTOS/Demo/RX200_RX231-RSK_GCC_e2studio_IAR 目录下，
使用 Renesas 编译器的项目位于
/FreeRTOS/Demo/RX200_RX231-RSK_Renesas_e2studio 目录下。将
项目导入到
到 e2studio Eclipse工作区时，必须选择这些目录。

---

### 构建和运行 Renesas RX231 RTOS 演示

RTOS 演示项目可进行配置，以构建
简单的“blinky”应用程序，或全面的测试和演示应用程序。
常量
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，定义于 main.c 的顶层，
用于在二者之间进行切换。当
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，将创建综合项目。当
mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，将创建简单的演示。

演示使用 RSK 开发板上内置的 LED，
因此无需进行硬件设置。

#### 使用 e2studio 构建（GCC 和 Renesas 编译器）

**注意：**一些由 e2studio 项目构建的 C
源文件使用
[项目相对路径](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)包含在项目中，
因此，如果 FreeRTOS 目录结构体已从
官方 .zip 文件下载内容中更改，项目将无法构建。

1. 启动 e2studio Eclipse IDE，根据提示创建一个新的或选择一个现有的
 工作区。
2. 在 IDE 的 "File" 菜单中选择 "Import"。系统将显示
 如下对话框。选择 "General->Existing Project into Workspace"，如下所示
 。

![将 RX64M 项目导入 e2studio Eclipse IDE](/media/2018/E2Studio_import.jpg)

**首次点击 "Import" 时显示的对话框**
3. 如果使用 GCC 编译器，请在下一个对话框中选择 /FreeRTOS/Demo/RX200_RX231-RSK_GCC_e2studio_IAR
 作为根目录；
 也可选择 /FreeRTOS/Demo/RX200_RX231-RSK_Renesas_e2studio
 （如果使用 Renesas 编译器）。
4. 确保在 "Projects" 区域中已勾选 RTOS 演示项目，
 并确保 "Copy Projects Into
 Workspace" 复选框未勾选 ，
 然后再点击 "Finish" 按钮（请参阅下图查看正确的复选框状态）。

![导入到 Eclipse CDT 时选择 RTOS 源代码](/media/2018/Import_RX64M_Project.png)

**确保已勾选 RTOS 演示，并且确保未勾选 "Copy projects into workspace"**
5. 打开 main.c，找到 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 的定义，
 它靠近文件的顶部。将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，
 以构建简单的 blinky 风格（入门）项目。将
 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0，
 以构建全面测试和演示应用程序。
6. 从 e2studio Eclipse 的 "Project" 菜单中选择 "Build All" 以构建
 演示项目，并等待构建完成。
7. 确保在 RX231 RSK 板和运行 e2studio 的计算机之间连接 E1 调试适配器
 （随 RSK 入门套件一起提供）。
 如果按照下方图片配置启动配置，
 则不需要使用独立电源。
8. 从 Eclipse 的 "Run" 菜单中选择 "Debug Configurations"
 来配置启动配置，该配置可用于
 对微控制器闪存进行编程并启动调试会话。按照下方图片所示方式，
 配置调试启动配置。

|  |  |  |  |
| --- | --- | --- | --- |
| [![](/media/2018/RX64M_Launch_Configuration_1.png)](/media/2018/RX64M_Launch_Configuration_1.png) | [![](/media/2018/RX231_Launch_Configuration_2.png)](/media/2018/RX231_Launch_Configuration_2.png) | [![](/media/2018/RX231_Launch_Configuration_3.png)](/media/2018/RX231_Launch_Configuration_3.png) | [![](/media/2018/RX231_Launch_Configuration_3.png)](/media/2018/RX231_Launch_Configuration_3.png) |

**点击图片放大**

### 演示应用程序功能

####  简单的 blinky 的示例

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中设置为 1 时，
会构建 blinky 示例。完成此操作后， main() 调用 main_blinky() ：
* **main_blinky() 函数：**

 main_blinky() 会创建 RTOS 队列、
 队列发送任务和队列接收任务，然后启动调度器。
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

####  全面测试和演示应用

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中设置为 0，
会构建综合示例。完成此操作后， main() 调用 main_full()：
* **main_full() 函数：**

 main_full() 会创建一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)、一些特定应用程序的测试任务、
 一个伪随机发生器任务，然后
 启动调度器。
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
 它每次围绕其实现循环进行迭代时，都会切换 LED 0。

 如果 LED 每 3 秒切换一次，
 则表示检查任务未检测到任何停滞的任务或未检测到任何错误。如果 LED
 每 200 毫秒切换一次，则表示至少发现了一个错误。

---

### RTOS 配置和使用详情

### RX231 RTOS 移植特定配置

此演示的特定配置项目位于 /FreeRTOS/Demo/RX200_RX231-RSK_GCC_e2studio_IAR/src/FreeRTOSConfig.h
（适用于 IAR 和 GCC 项目）；/FreeRTOS/Demo/RX200_RX231-RSK_Renesas_e2studio/src/FreeRTOSConfig.h（适用于 Renesas 编译器项目）
。可以编辑这些文件中定义的常量，
编辑此文件中定义的常量。特别是：

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS tick 的频率。提供的数值 1 KHz 可用于
 测试 RTOS 内核功能，但比大多数应用程序所需的频率更快。降低该频率有助于提高效率。
* **configKERNEL_INTERRUPT_PRIORITY**
 此常量定义了 RTOS 内核用于 RTOS tick
 定时器和软件中断的中断优先级。应始终将其设置为
 最低中断优先级，在 RX231 中为 1。请参[阅配置页面](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，了解详细信息。
* **configMAX_SYSCALL_INTERRUPT_PRIORITY**
 此常量定义了可以调用 RTOS API 函数的
 。处于或低于此优先级的中断可以调用 FreeRTOS API
 函数，**前提是**该 API 函数以 "FromISR" 结尾。
 高于此优先级的中断不能调用任何 FreeRTOS API 函数，
 但不会受到 RTOS 内核正在执行的任何操作的影响。这使得它们
 适用于需要非常高时间精度的功能
 （例如电机控制）。

RXv2 移植层使用 #define 将 "BaseType_t" 定义长整型。

### 编写中断服务程序 (ISR)

可以使用标准编译器语法编写中断。下方提供了三种支持的编译器示例
。

通常，ISR 想要引起上下文切换，因此
ISR 完成时返回的任务就与 ISR 最初中断的任务不同。如果 ISR 导致某个任务解除阻塞，
并且被解除阻塞的任务与已处于运行状态的任务相比具有更高的优先级，
就属于这种情况。这
可以通过调用 portYIELD_FROM_ISR() 来实现，该函数采用单个参数。
如果不需要上下文切换，则参数必须为 0；如果需要上下文切换，则参数必须为非零。
下方示例中使用的是 portYIELD_FROM_ISR()
。

|  |
| --- |
| <br/>```c< br/> < br/>/* Pragma used to install the interrupt. The 'enable' used in the pragma<br/>tells the compiler to enable interrupts before executing the user code. */<br/>#pragma interrupt ( Excep_PERIB_INTB128( vect = 128, enable ) )<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Interrupts are already enabled here. See comment above. */<br/><br/>    /* [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the task handle has already been stored. If notifying the task<br/> unblocks the task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the vTaskNotifyGiveFromISR()<br/> function. */<br/>    vTaskNotifyGiveFromISR( xTask, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}< br/> < br/>```<br/><br/><br/><br/>**使用 Renesas 编译器语法的中断服务程序示例** <br/><br/> |

|  |
| --- |
| <br/>```c<br/><br/>/* Pragma used to install the interrupt. */<br/>#pragma vector = VECT_TMR0_CMIA0<br/><br/>/* Function definition. */<br/>__interrupt void vT0_1_InterruptHandler( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Unlike when using the Renesas compiler, interrupts must be explicitly<br/> re-enabled inside the interrupt service routine. */<br/>    __enable_interrupt();<br/><br/>    /* [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the task handle has already been stored. If notifying the task<br/> unblocks the task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the vTaskNotifyGiveFromISR()<br/> function. */<br/>    vTaskNotifyGiveFromISR( xTask, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**使用 IAR 编译器语法的中断服务程序示例** <br/><br/> |

|  |
| --- |
| <br/>```c<br/><br/>/* The function prototype uses the interrupt attribute. The then function<br/>must be manually inserted into the interrupt vector table. */<br/>static void vT0_1_InterruptHandler( void ) __attribute__((interrupt));<br/><br/>/* Function definition. */<br/>void Excep_PERIB_INTB128( void )<br/>{<br/>long lHigherPriorityTaskWoken;<br/><br/>    /* Unlike when using the Renesas compiler, interrupts must be explicitly<br/> re-enabled inside the interrupt service routine. */<br/>    __asm volatile( "SETPSW	I" );<br/><br/><br/>    /* [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) is an interrupt safe FreeRTOS function. It is<br/> assumed the task handle has already been stored. If notifying the task<br/> unblocks the task, and the task that is unblocked has a priority above the<br/> priority of the currently executing task, then the lHigherPriorityTaskWoken<br/> parameter will get set to pdTRUE inside the vTaskNotifyGiveFromISR()<br/> function. */<br/>    vTaskNotifyGiveFromISR( xTask, &lHigherPriorityTaskWoken );<br/>    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );<br/>}<br/><br/>```<br/><br/><br/><br/>**使用 GCC 编译器语法的中断服务程序示例** < br/>< br/> |

### 生成 RTOS tick中断

FreeRTOS 需要独占使用能够生成 tick 中断的定时器，
要由应用程序编写者定义使用哪个定时器。要做到这一点,
应用程序必须定义一个名为 vApplicationSetupTimerInterrupt() 的函数，
该函数将定时器配置为以
[configTICK_RATE_HZ](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtick_rate_hz) 设置
该设置位于 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中指定的频率生成中断，然后将 RTOS tick
中断处理程序安装在中断向量表内的相应位置。

使用 IAR 和 Renesas 编译器时，要安装 RTOS tick 处理程序，
只需
在 FreeRTOSConfig.h 中将 configTICK_VECTOR 定义适当的向量编号。

使用 GCC 编译器时，RTOS tick 处理程序和 RTOS 软件中断处理程序
必须手动添加到向量表定义中的适当向量中。
RTOS tick 处理程序被称为 vPortTickISR()，RTOS 软件中断
处理程序被称为 vPortSoftwareInterruptISR ()。请参阅 GCC 项目中的源文件 vector_table.c
获取示例。

建议使用比较匹配定时器来生成滴答中断，
例如，vApplicationSetupTimerInterrupt() 的实现使用了比较匹配定时器 0，
包含在每个 RX200 演示应用程序的 main.c 中。

### FreeRTOS使用的资源

FreeRTOS 需要独占使用软件中断。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

RX231 演示应用程序项目中内置 Source/Portable/MemMang/heap_4.c，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。
