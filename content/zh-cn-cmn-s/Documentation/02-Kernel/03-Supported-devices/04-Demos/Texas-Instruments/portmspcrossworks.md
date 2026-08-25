---
title: "TI MSP430 (MSP430F449) RTOS 移植，适用于 CrossWorks 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ES449.gif](/media/2018/ES449.gif)

该移植在 [ES449开发/原型开发板](http://www.softbaugh.com/ProductPage.cfm?strPartNo=ES449)
（来自 [SoftBaugh](http://www.softbaugh.com/)）上开发而成（如果您希望使用其他开发板，请参阅此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)），
使用 [CrossWorks
MSP430 编译器](http://www.rowley.co.uk/msp430/index.htm)和 SoftBaugh [FETP 并行
端口 JTAG 接口](http://www.softbaugh.com/ProductPage.cfm?strPartNo=FETP)

ES449 是一款小巧的、基于 MSP430F449 的原型板，可用于轻松访问 MSP430 外设，随附
LCD 显示屏，非常适合调试！FETP 与 CrossWorks 可无缝连接，速度流畅，使得 ES449 成为易于使用的
开发平台。

FreeRTOS V5.1.0 升级了此移植和演示，允许任务使用 MSP430 的 1 至 3 低功耗模式。

---

### 重要提示！CrossWorks MSP430 RTOS 移植使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)
4. [选择要使用的端口](#使用-msp430f449-以外的部件)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码，因此包含的文件远多于运行此演示所需的文件。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
下载文件的描述和有关创建新项目的信息。

用于构建 MSP430 FreeRTOS 演示的 CrossWorks 项目位于 Demo/msp430_CrossWorks 目录中。

---

### 演示应用程序

### 功能

ES449 原型板包括一个内置 LCD 显示屏和一个内置
用户 LED 灯。使用此硬件时，标准演示任务中一般会闪烁 LED 灯，而不是
在 LCD 显示屏上闪烁 '*' 字符。最左边的 '*' 代表 LED 0，
往右一个是 LED 1，以此类推。

其中一个 ComTest 任务会使用板载 LED。每次串行端口上接收到一个字符时，
LED 就切换一次。

演示应用程序创建 10 个任务，其中包括 9 个 [标准演示应用程序任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
和 1 项空闲任务。正确执行时，
演示应用程序表现如下：

* LCD 显示屏上的前三个 '*' 字符受 'flash' 任务的控制。每个字符
 以固定频率闪烁，第一个 '*' 闪烁最慢，第三个
 最快。
* 串行端口上收到字符时，原型版中内置的 LED 便会闪烁（请参阅下文“硬件设置”部分）。
* 并非所有的任务都会更新 LCD，因此没有可见的迹象表明它们是否正常运行。因此，我们创建了一项 'Check' 任务，
 旨在确保在所有其他任务中都未检测到错误。

 LCD 显示屏上第五个 '*' 受 'Check' 任务的控制。
 'Check' 任务每 3 秒钟便会检查一次系统中的所有任务，确保任务正确执行，没有出现错误。
 然后切换 '*' 5。如果 '*' 5 每 3 秒切换一次，
 那么就说明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 发现了至少一个错误。

### 演示应用程序硬件设置

演示应用程序需执行通过串行端口发送和接收字符的任务。字符由
一项任务发送，被另一项任务接收。如有字符丢失或接收顺序不正确，则会标记错误状态。
通常情况下，此机制需要环回连接器才能运行（这样才能保证 UART 发送的所有字符也能
由其接收）。这种情况下会使用 MSP430 UART  的 'loopback' 模式，不需要其他外部连接器。

演示应用程序使用 LCD 显示屏代替 LED 灯，因此不需要其他硬件设置。

### 构建

要构建演示应用程序：
1. 从 CrossStudio IDE 中打开项目文件 FreeRTOS/Demo/MSP430_CrossWorks/RTOSDemo.hzp。
2. 选择所需构建（调试或发布）。![](/media/2018/crossstudio.gif)

 选择所需构建

- 从 CrossStudio Project 菜单中选择 "Build Solution"，或直接按 F7。

### 下载和执行

要将应用程序下载到目标硬件：

	1. 连接目标板与主机之间的 FETP JTAG 接口。目标板将通过 FETP JTAG 接口供电，不需要连接
	 其他电源。
	2. 从 CrossStudio "Target" 菜单中选择 "Connect MSP430 Flash Emulation Tool"。
	3. 从 CrossStudio "Debug" 菜单中选择 "Start Debugging"。演示应用程序将对 MSP430 闪存
	 进行自动编程。

一旦应用程序被编入闪存，就可以在 CrossStudio 调试器中执行应用程序。或者，停止
调试器（关闭目标板电源），移除 FETP JTAG 接口，然后为目标板提供外部
电源。

---

### 配置和使用详情

### 串行端口驱动程序

根据规定串口驱动程序是为环回模式所配置。因此，虽然演示应用程序能够执行，但
如有其他用途，则需关闭环回模式。

此外还应注意，编写串行驱动程序是为了测试部分实时内核功能，而不是
提供优化解决方案。

### RTOS 移植特定配置

此移植的特定配置项位于 Demo/MSP430_CrossWorks/FreeRTOSConfig.h 中。您可编辑此文件中定义的常量，
确保适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS tick 的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。本端口将
BaseType_t 定义为短整型。

请注意，vPortEndScheduler() 尚未实现。

### 使用 MSP430F449 以外的部件

核心实时内核组件应
可在所有 MSP430F4xx 设备上移植，但需要考虑外接设备的设置和内存要求。
需要考虑的事项：

	* Source/portable/Rowley/MSP430F449/port.c 中的 prvSetupTimerInterrupt() 负责配置微控制器定时器，
	 以生成 RTOS tick。
	* 移植、内存访问和系统时钟配置由 Demo/MSP430_CrossWorks/main.c 中的 prvSetupHardware() 执行。
	* 串行端口驱动程序。
	* 寄存器位置定义由文件 msp430x44x.h 提供，该文件位于
	 Demo/MSP430_CrossWorks/FreeRTOSConfig.h 的顶部。
	* RAM 大小：参阅下文“内存分配”部分。
### 抢占式内核和协同式 RTOS 内核之间的切换

将 Demo/MSP430_CrossWorks/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式内核；设置为 0，可使用
则使用协作式内核。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是基于提供的演示应用程序项目
搭建您的应用程序。

### 内存分配

MSP430 演示项目中包含 Source/Portable/MemMang/heap_1.c，用于提供实时内核所需的
内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
获取完整信息。

---

### 中断服务程序

V5.1.0 之前的 FreeRTOS 版本包含两组 MSP430 的移植层文件：

	1. 官方支持的版本，使用 Rowley 编译器提供的扩展程序，完全使用 C 语言实现中断服务程序。
	2. 演示所提供的移植，要求中断服务程序具有汇编函数包装器。

FreeRTOS V5.1.0 仅包括官方支持的版本，但引入了预处理器宏和新的头文件，允许用户定义
编写中断服务程序的方法。以下部分将介绍使用这两种方法所需的步骤。
提供的演示应用程序中的 UART 驱动程序也演示了这两种方法。

方法 1 只需要 C 代码，因此比方法 2 更容易实现。只有在实际需要上下文切换时，该方法才保存和恢复任务上下文， 
因此也更高效。但是，中断内执行的上下文切换会导致一些处理器寄存器
被保存两次（一次在中断条目上，另一次用于上下文切换）。这意味着与方法 2 相比，使用方法 1 时，
需要为每项任务分配更大的堆栈。

### 编写 ISR：方法 1

要使用方法 1：

	1. 将预处理器宏 configINTERRUPT_EXAMPLE_METHOD 设置为 1。提供的演示应用程序在 FreeRTOSConfig.h 中定义 configINTERRUPT_EXAMPLE_METHOD。
	2. 使用 __interrupt[ ] 函数限定符，在 C 文件中实现中断服务程序。
	3. 如果使用低功耗模式，确保在退出中断服务程序之前，调用 __bic_SR_register_on_exit(SCG1 + SCG0 + OSCOFF + CPUOFF)。
	4. 如果中断程序内部需要上下文切换，请使用标准 taskYIELD() 宏。

以下是使用方法 1 编写的 UART Rx 中断示例。

---

```c

void vRxISR( void ) __interrupt[ UART1RX_VECTOR ]
{
signed char cChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Get the character from the UART and post it on the queue of Rxed
 characters. */
    cChar = U1RXBUF;

    xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );

    if( xHigherPriorityTaskWoken )
    {
        /*If the post causes a task to wake force a context switch
 as the woken task may have a higher priority than the task we have
 interrupted. */
        taskYIELD();
    }

    /* Make sure any low power mode bits are clear before leaving the ISR. */
    __bic_SR_register_on_exit( SCG1 + SCG0 + OSCOFF + CPUOFF );
}

```

---

使用方法 1 编写 ISR
### 编写 ISR：方法 2

要使用方法 2：

	1. 将预处理器宏 configINTERRUPT_EXAMPLE_METHOD 设置为 2。提供的演示应用程序在 FreeRTOSConfig.h 中定义 configINTERRUPT_EXAMPLE_METHOD。
	2. 提供作为中断处理程序例程安装的汇编函数。该函数所需的格式如下所示。请注意，汇编文件必须包含 portasm.h 头文件，才能访问所需的 portSAVE_CONTEXT 和 portRESTORE_CONTEXT 汇编宏。
	3. 提供由汇编文件包装器调用的标准 C 函数，以执行实际的中断处理工作。具体请参阅下文示例。
	4. 如果中断程序内部需要上下文切换，请使用 portYIELD_FROM_ISR() 宏。

以下是中断实现的汇编文件包装器和 C 函数部分的示例。

---

```c

/* Ensure the required header files are included. */
#include "FreeRTOSConfig.h"
#include "portasm.h"

.CODE

/* Example wrapper for the Rx UART interrupt. */
_vUARTRx_Wrapper:

    /* portSAVE_CONTEXT must be the first macro to be called. This is defined within
 portasm.h. */
    portSAVE_CONTEXT

    /* Following portSAVE_CONTEXT the C portion of the handler can be called. */
    call #_vRxISR

    /* Finally portRESTORE_CONTEXT must be called at the end of the wrapper. This too
 is defined within portasm.h. */
    portRESTORE_CONTEXT

/******************************************************************/

    /* The wrapper must be installed as the interrupt handler. */

    .VECTORS
    .KEEP

    ORG    UART1RX_VECTOR
    DW    _vUARTRx_Wrapper

    END

```

---

ISR 的汇编文件部分

---

```c

/* This is the standard C function called by the assembly file wrapper. */
void vRxISR( void )
{
signed char cChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Get the character from the UART and post it on the queue of Rxed
 characters. */
    cChar = U1RXBUF;

    xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );

    /*If the post causes a task to wake force a context switch
 as the woken task may have a higher priority than the task we have
 interrupted. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

```

---

从汇编文件包装器调用的 C 函数
