---
title: "Renesas RZ/T RTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

包括 FreeRTOS-Plus-CLI，
使用 IAR 和 GCC 嵌入式编译器

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![用于 RTOS 演示的 Renesas RZ/T1 RSK](/media/2018/rsk_rzt1.jpg)

## 简介

此页面记录了一个 FreeRTOS 演示应用程序，
[适用于 Renesas RZ/T 嵌入式处理器](http://www.renesas.eu/products/mpumcu/rz/rzt/index.jsp)，该处理器具有 ARM Cortex-R4F 核心。提供了 2 个项目，
允许使用
[IAR 嵌入式工作台](http://www.iar.com/ewarm)或
GCC 嵌入式开发工具构建演示。演示面向 Renesas
[RZT1 RSK](https://www.renesas.com/us/en/products/microcontrollers-microprocessors/rz-cortex-a-mpus/rzt1-starter-kit-plus-renesas-starter-kit-rzt1)
(Renesas 入门套件)。

两个项目都包含生成选项，允许创建简单的 blinky 演示
并使用：

- FreeRTOS Cortex-R4F 内核移植（用于不包含
  ARM 通用中断控制器 (GIC) 的嵌入式处理器版本），
  支持中断嵌套。
- IAR 嵌入式工作台或 e2studio IDE
  （取决于所使用的项目文件）
- [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
  命令行接口。
- 标准演示任务，包含测试中断嵌套的任务

---

### _重要提示！关于使用 RTOS Renesas RZ/T 演示项目_的说明

_使用此 RTOS 移植前,请阅读下述所有要点。_

1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#renesas-rzt-arm-cortex-r4-演示应用程序)
3. [构建说明（适用于嵌入式工作台和 e2studio ） ](#构建说明)
4. [RTOS 配置和使用详情，特别是：](#rtos-配置和使用详情)
   - [编写中断](#编写-isr-的-c-部分iar-和-gcc)
   - [生成 RTOS tick 中断](#生成-rtos-tick-中断)
   - [包含 IRQ 处理程序](#包含-irq-处理函数)

另请参阅常见问题：[我的应用程序未运行，可能出了什么问题？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

## 源代码组织

FreeRTOS zip 文件包含所有 RTOS 移植和所有
RTOS 演示应用程序的源代码。这些文件中只有一小部分要用于
Renesas RZ/T ARM Cortex-R4F 演示。[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面描述
FreeRTOS zip 文件下载包的结构，并提供
关于如何创建新 RTOS 项目的信息。

用于使用 GCC 构建演示的 e2studio Eclipse 项目文件以及 IAR嵌入式工作台项目文件
（用于使用 IAR 编译器构建演示），
均位于 FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR
目录下。

E2studio GCC 和 IAR 项目会构建相同的 RTOS 演示应用程序，并且都会包含
/FreeRTOS-Plus 目录下的文件，
如果 /FreeRTOS-Plus 目录已删除或移出默认位置，则不会构建项目
默认位置移动，项目将无法构建。

---

## Renesas RZ/T ARM Cortex-R4 演示应用程序

### 硬件和软件设置

此页面上记录的演示使用了 RZT1 RSK 内置的 UART 到 USB 转换器和 LED，
因此无需进行硬件设置。

### 功能

####

简单的 blinky 示例

当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中设置为 1 时，
会构建 blinky 示例。完成此操作后， main() 调用 main_blinky() ：

- **main_blinky() 函数：**

main_blinky() 会创建 RTOS 队列、
队列发送任务和队列接收任务，然后启动调度器。

- **队列发送任务：**

队列发送任务由 main_blinky.c 中的 prvQueueSendTask() 函数实现。

prvQueueSendTask() 每 200 毫秒向 RTOS 队列发送一次值 100。

- **队列接收任务：**

队列接收任务由 main_blinky.c 中的 prvQueueReceiveTask() 函数实现
实现。

prvQueueReceiveTask() 在数据到达 RTOS 队列前保持阻塞状态。
每次从队列接收值 100 后会切换 LED 0。
由于数据每 200 毫秒发送到队列，
因此，LED 也将每 200 毫秒切换一次。

####

综合测试和演示应用

![RTOS CLI](/media/2018/Renesas_CLI_Session.jpg)
当 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 中设置为 0 时，
会构建综合示例。完成此操作后， main() 调用 main_full()：

- **main_full() 函数：**

main_full() 会创建一组[标准演示任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)、一些特定的应用程序测试任务、
一项命令行接口 (CLI) 任务、一项伪随机发生器任务，
然后启动调度器。
伪随机发生器任务只是用来在测试任务的执行顺序中加入一些变化，
并以此
来提高测试覆盖率。

- **命令行接口 (CLI)**

CLI 是通过 [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/03-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
可扩展的命令行接口来实现，
并使用 UART 到 USB 转换器l连接器 (J8)，
以19200 baud 的速率进行输入和输出。与 FreeRTOS-Plus-CLI 一样，键入 "help"
可以查看已注册命令的列表。

- **“寄存器测试”任务：**

寄存器测试任务用于测试上下文切换机制，
它向每个嵌入式处理器寄存器填入已知的值，然后持续检查每个
寄存器在整个任务生命周期内是否保持其预期值。

- **"Check" 任务：**

"Check" 任务监测系统内所有其他任务的状态，
寻找停滞的任务或报告错误的任务。
它每次围绕其实现循环进行迭代时，都会切换 LED 0。

如果 LED 每 3 秒切换一次，
则表示检查任务未检测到任何停滞的任务或未检测到任何错误。如果 LED
每 200 毫秒切换一次，则至少发现了一个错误。

---

## 构建说明

### 构建和执行演示应用程序 - IAR Embedded Workbench

请注意，IAR 项目会引用位于 /FreeRTOS-Plus
和 /FreeRTOS/Demo/Common 目录中的通用文件，因此
项目将无法编译。

1. 打开 FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/RTOSDemo.eww
   （从 IAR 嵌入式工作台 IDE 中打开）。
2. 打开项目的 main.c 文件，设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，以根据需求生成
   简单的 blinky 演示或完整的测试和演示应用程序
   。
3. 在 IDE 的 "Project" 菜单中选择 "Build All" 以构建 RTOS 演示。
4. 确保已使用适当的调试接口
   将目标硬件连接至主机。
5. 在 IDE 的 "Project" 菜单中选择 "Options" ，将出现选项窗口
   。在选项窗口中，首先选择 "Debugger" 类别，
   然后确保 "driver" 设置对于您的调试器连接（J-Link，I-Jet 等）是正确的，
   设置正确后关闭 Options 窗口。
6. 在 IDE 的 "Project" 窗口中选择 "Download and Debug"，
   将构建的可执行文件下载到 ARM Cortex-R4F，并启动调试会话。

### 构建和执行演示应用程序 - e2studio

请注意，e2studio Eclipse 项目[同时使用虚拟文件夹和链接](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)，这些虚拟文件夹和链接引用了 /FreeRTOS-Plus 和 /FreeRTOS/Demo/Common 目录下的文件
。在 Eclipse 项目资源管理器中查看的[虚拟]文件结构与
磁盘上查看的[实际]文件结构不一致，如果任一引用的目录丢失或被移动，
项目将无法构建。

1. 打开 e2studio，根据提示新建工作区或选择现有工作区
   。
2. 在 IDE 的 "File" 菜单中选择 "Import"，
   打开导入对话框。
3. 在 Import 对话框中，选择 "General->Existing Projects Into Workspace"，
   然后浏览并选择 FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR
   目录，您将看到一个名为 "RTOSDemo" 的项目。
4. 确保 RTOSDemo 已勾选，**且 Copy Projects Into Workspace 选项
   在**点击 "Finish" 之前未勾选。

![导入到 Eclipse CDT 时选择 RTOS 源代码](/media/2018/Import_RX64M_Project.png)

将 FreeRTOS_Demo 导入到 Eclipse 工作区，而**无需**
将其复制到工作期。打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 以根据需要生成
构建简单的 blinky 演示或完整的测试和演示应用程序。
6\. 确保已使用合适的调试接口
（例如：J-Link）来连接主机。7. 在 IDE 的 "Project" 菜单中选择 "Build All"。8. 构建完成后，
从 IDE 的 "Debug" 菜单中选择 "Debug Configurations..."，
并配置和运行适合您所选连接方法的调试配置。
下方可点击的屏幕截图显示了使用 J-Link
JTAG 接口的配置。

|                                                                                                   |                                                                                               |                                                                                               |
| ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [\![](/media/2018/RX64M_Launch_Configuration_1.png)](/media/2018/RX64M_Launch_Configuration_1.png) | [\![](/media/2018/RZT_Launch_Configuration_2.jpg)](/media/2018/RZT_Launch_Configuration_2.jpg) | [\![](/media/2018/RZT_Launch_Configuration_3.jpg)](/media/2018/RZT_Launch_Configuration_3.jpg) |

**点击图片放大**

---

## RTOS 配置和使用详情

### 中断服务程序

中断发生时，RZ/T 实时嵌入式处理器硬件将
直接指向外设特定中断处理程序，
而不是 ARM Cortex-R IRQ 向量。因此，应用程序安装的每个中断处理程序必须包含汇编文件包装器，
该汇编文件包装器执行一些内务管理，
然后分支到 FreeRTOS 中断条目代码。FreeRTOS 中断条目代码
管理中断条目，包括中断嵌套，
然后调用标准 C 函数，提供中断外设服务。

本示例中，假定中断处理程序的 C 部分
称为 InterruptHandler()，如下所示。完整示例提供在
演示如何编写汇编文件包装器的章节之后。

```c


void InterruptHandler( void )

{

    /* Write the interrupt handler code here. */

}



		The C portion of the interrupt handler - this is where the interrupting peripheral is serviced


```

本示例中，
假定汇编包装器称为 InterruptHandlerWrapper()。该
包装器必须将指向处理程序函数 C 部分的指针保存在称为
pxISRFunction 的变量中，然后分支到称为
FreeRTOS_IRQ_Handler 的函数 (由 RTOS 提供)。

将汇编文件包装器添加到每个 C 中断处理程序函数所需的语法
取决于使用的编译器（IAR 或 GCC）。下方提供了示例和进一步参考
。

####

为 ISR 编写汇编包装器：IAR

使用 IAR 工具时，汇编包装器必须在汇编文件中实现
。下方提供了通用示例，其他示例可以
在 /FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/System/IAR/Interrupt_Entry_Stubs.asm 中找到。

```c


    SECTION intvec:CODE:ROOT(2)

    ARM



    /* Variables and functions from the RTOS port. */

    EXTERN pxISRFunction

    EXTERN FreeRTOS_IRQ_Handler



    /* The C portion of the interrupt handler. */

    EXTERN InterruptHandler



    /* Functions implemented in this file. */

    PUBLIC InterruptHandlerEntry



    /* The implementation of InterruptHandlerEntry. */

InterruptHandlerEntry:

    /* Save used registers (probably not necessary). */

    PUSH    {r0-r1}

    /* Save the address of the C portion of this handler into pxISRFunction. */

    LDR     r0, =pxISRFunction

    LDR     R1, =InterruptHandler

    STR     R1, [r0]

    /* Restore used registers. */

    POP     {r0-r1}

    Branch to the RTOS IRQ handler. */

    B        FreeRTOS_IRQ_Handler



The assembly wrapper for the C interrupt handler function - IAR


```

####

为 ISR 编写汇编包装器：GCC

使用 GCC 工具时， GCC 内联汇编器和“裸”函数属性
可用于将汇编包装器列入 C 文件中。下方提供了通用示例
，其他示例可以在
/FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOS_tick_config.c、
/FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/cg_src/r_cg_scifa_user.c 和
/FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/full_demo/IntQueueTimer.c
源文件中找到。

```c


#include "FreeRTOS.h"



/* The prototype for the function that implements the assembly file wrapper must

use the naked attribute - which prevents the compiler from adding any function

prologue or epilogue assembly code. */

void InterruptHandlerWrapper( void ) __attribute__((naked));



/* The implementation of InterruptHandlerEntry. This is a naked function and

must not include and C code! */

void InterruptHandlerWrapper( void )

{

    __asm volatile (

        /* Save used registers (probably not necessary). */

        "PUSH   {r0-r1}                               tn"

        /* Save the address of the C portion of this handler in pxISRFunction. */

        "LDR    r0, =pxISRFunction                    tn"

        "LDR    r1, =InterruptHandler                 tn"

        /* Restore used registers. */

        "STR    r1, [r0]                              tn"

        "POP    {r0-r1}                               tn"

        Branch to the RTOS IRQ handler. */

        "B       FreeRTOS_IRQ_Handler                     "

    );

}



The assembly wrapper for the C interrupt handler function - GCC


```

#### 编写 ISR 的 C 部分：IAR 和 GCC

如果 ISR 使得一个与当前执行的任务具有相同或比当前执行的任务具有更高优先级的任务
并因 ISR 而解除阻塞状态，则 ISR 必须请求上下文切换，
方可退出。此时，中断服务程序会中断一项 RTOS 任务，
但返回另一项 RTOS 任务。

宏 portYIELD_FROM_ISR()（或 portEND_SWITCHING_ISR()）可用于
从 ISR 内部请求上下文切换。
下列源代码片段仅作为示例提供。ISR 示例
使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
以同步任务（未显示），并调用 portYIELD_FROM_ISR()，
以确保中断直接返回到任务。

```c


void InterruptHandler(void)

{

long lHigherPriorityTaskWoken = pdFALSE;



    /* Clear the interrupt if necessary. */

    Dummy_ClearPendingInterrupt();



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



The C portion of an interrupt service routine


```

只有以 "FromISR" 结尾的 FreeRTOS API 函数可以从
中断服务程序调用。

### 生成 RTOS tick 中断

RTOS Cortex-R 移植是通用移植，
为使用宏和回调函数的特定嵌入式处理器实现量身定制。RTOS tick
中断通过以下两个宏来配置，
这两个宏定义在随 RTOS 演示应用程序提供的 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 文件中：

1. **configSETUP_TICK_INTERRUPT()**

这必须调用配置定时器以生成 tick 中断的函数，
并安装 FreeRTOS_Tick_Handler() 作为定时器中断服务程序
（通过如上所述的汇编包装器）。

提供的演示应用程序中，
设置此宏来调用
vConfigureTickInterrupt()，它定义在
FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOS_tick_config.c 中，
且此宏配置了比较匹配定时器 5 (CMT5) 以生成 RTOS
tick。2. **configCLEAR_TICK_INTERRUPT()**

这必须清除用于生成
RTOS tick 的任何一个定时器中的待处理中断。

提供的演示应用程序中，设置此宏来清除
CMT5 中的中断，因为 RTOS tick 中断是由 CMT5 生成的。

### 包含 IRQ 处理函数

RTOS Cortex-R 移植是通用移植，
为使用宏和回调函数的特定嵌入式处理器实现量身定制。在 RZ/T RTOS 移植中，
通用 IRQ 处理代码（管理中断条目的代码）调用
vApplicationIRQHandler()，vApplicationIRQHandler() 必须由应用程序提供
。

提供的演示应用程序中， vApplicationIRQHandler()
在 FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOS_tick_config.c 中实现，
复制如下：

```c


/* The function called by the FreeRTOS IRQ handler, after it has managed

interrupt entry. This function creates a local copy of pxISRFunction before

re-enabling interrupts then calling the handler pointed to by pxISRFunction.

pxISRFunction is set by the assembly wrapper added to each interrupt handler. */

void vApplicationIRQHandler( void )

{

ISRFunction_t pxISRToCall = pxISRFunction;



	portENABLE_INTERRUPTS();



	/* Call the installed ISR. */

	pxISRToCall();

}

The implementation of vApplicationIRQHandler() for the RZ/T RTOS port


```

### FreeRTOS ARM Cortex-R4F 移植演示应用程序特定配置

此演示的特定配置项目位于 FreeRTOS/Demo/CORTEX_R4F_RZ_T_GCC_IAR/src/FreeRTOSConfig.h。
[可以编辑此文件中定义的常量，以适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。

### FreeRTOS使用的资源

FreeRTOS 需要独占使用 SVC 中断。

### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-R4 RTOS 演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。
