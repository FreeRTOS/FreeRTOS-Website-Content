---
title: "ColdFire V2 (MCF52221) RTOS 演示 使用 CodeWarrior 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/FreeScale-ColdFire-M52221DEMO.jpg)

本页介绍的 FreeRTOS CodeWarrior 移植和演示应用程序
适用于 [V2 ColdFire](http://www.freescale.com/webapp/sps/site/taxonomy.jsp?nodeId=0162468rH3YTLC00M95448) 核心
（来自 Freescale）。

移植亮点包括完全中断嵌套支持，并且在编写中断服务程序时无特殊编码要求。

移植和演示已预配置为使用：

* [MCF52221 ColdFire MCU](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=MCF5222X&webpageId=1113331549638725695448&nodeId=0162468rH3YTLC00M95448&fromPage=tax)。
* [M52221DEMO 评估板](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=M52221DEMO)（如果希望使用其他开发板，请参考此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。
* [CodeWarrior for ColdFire 特别版](http://www.freescale.com/webapp/sps/site/overview.jsp?nodeId=01272600610BF1)工具链（免费）。

---

### 重要！关于使用 CodeWarrior V2 ColdFire 移植的说明 RTOS

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解下载文件的描述和有关创建新项目的信息。

ColdFire MCF52221 演示的 CodeWarrior 项目包含在 FreeRTOS/Demo/ColdFire_MCF52221_CodeWarrior 目录下。请注意，这是一个
项目文件，而不是工作区文件。

---

### 演示应用程序

#### 演示应用程序硬件设置

M52221DEMO 硬件包括 PE Micro BDM 接口电路，允许评估板
直接通过 USB 连接线连接到主机 PC。通过
将标记为 PWR_SEL 的跳线设置为 VB，可通过同一 USB 接口供电。

演示应用程序包括中断驱动的 UART 测试，其中一个任务传输字符，
随后另一个任务接收此类字符。为正确操作此功能，必须将环回连接器安装到
M52221DEMO 硬件的 COM 连接器（引脚 2 和 3 必须连接在 9 路连接器上——
通常情况下，使用回形针便能实现此目的）。

演示应用程序使用内置在评估板上的 LED，因此不需要进一步设置硬件。

#### 功能性

在启动 RTOS 调度器之前，演示项目会创建 24 个任务和 3 个协程。这些任务不执行
演示和测试 ColdFire / CodeWarrior 移植以外的任何特定函数。

如果正确执行，该演示将实现以下效果：

* 标为 LED1、LED2 和 LED3 的 LED 由非常简单的 'flash' 协程控制。各个 LED
 以恒定频率闪烁，其中 LED1 频率最高， LED3 频率最低。协程
 从空闲任务挂钩函数内调度。
* 大多数任务不会更新 LED ，因此没有明确迹象表明它们运行正常。
 因此，创建了一个“检查”任务，用于确保其他任务中没有检测到任何错误
 。检查任务每隔几秒才执行一次，但具有高优先级，因此可以保证在需要时
 获得处理时间。如果所有演示任务都按预期执行，
 检查任务将每隔 5 秒切换一次标记为 LED4 的 LED。如果在任何任务中检测到错误，切换速率将增加到 500 毫秒
 。将环回连接器从 COM 连接器上移除以故意产生错误，
 便可以测试该机制。

更多信息请参阅源代码相关注释。

由于所提供的演示配置了使用中断优先级 1  的 RTOS 内核和使用中断优先级 3 的 UART，因此
UART 中断可以嵌套在内核中断中。允许的嵌套层次越深，消耗的堆栈大小
就越大——需要将 configCHECK_FOR_STACK_OVERFLOW 的值设置为 2，以捕获深层嵌套引起的溢出，但该操作应当
仅用于调试目的，因为它会减慢上下文切换操作。演示应用程序默认为每个任务分配
相同的堆栈大小，而不是调整每个堆栈以确保不会浪费 RAM。

#### 构建演示应用程序

1. 在 CodeWarrior IDE 中打开 DemoColdFire_MCF52221_CodeWarriorRTOSDemo.mcp 项目文件（请注意，
 此为项目文件，而不是工作区文件，因此应使用 "File | Open" 菜单项打开，而不是 "File | Open Workspace" 菜单项）。
2. 按 F7 后不出现错误或警告，则项目构建成功。

已知 CodeWarrior 会将项目中包含的 port.c 和 portasm.S 文件随机更改为 PC 版本。
如果发现这两个文件出现大量错误和警告，请确保实际构建的 port.c 和 portasm.S 文件
位于 FreeRTOSSourceportableCodeWarriorColdFire_V2 目录下。

#### 对微控制器闪存进行编程

1. 从 IDE "Tools" 菜单中选择 "Flash Programmer"，打开闪存编程实用程序。
2. 单击 "Load Settings" 按钮（如下红色高亮显示）以打开 XML 文件列表，
 该列表用于描述每个受支持的设备。选择名为 "MCF52221_INTFLASH.xml" 的 XML 文件（假设
 使用的是 MCF52221 微控制器）。

![](/media/2018/CodeWarrior-flash-programmer-load-settings.jpg)

 打开 MCF52221 配置 xml 文件
3. 单击闪存编程窗口中的 "Erase / Blank Check"（如下红色高亮显示）以显示 "Erase" 按钮。

![](/media/2018/CodeWarrior-flash-programmer-erase.jpg)

 单击 "Erase / Blank Check" 以显示 "Erase" 按钮
4. 单击 "Erase" 按钮，几秒钟后，您将收到一条消息，提示擦除成功。
5. 点击 "Program / Verify" （如下红色高亮显示）以显示 "Program" 按钮。

![](/media/2018/CodeWarrior-flash-programmer-program.jpg)

 单击 "Program / Verify" 以显示 "Program" 按钮
6. 单击 "Program" 按钮，几秒钟后，您将会收到一条消息，提示
 演示应用程序已正确编程到 ColdFire 闪存中。

#### 启动调试会话

首先按照说明对闪存进行编程并关闭闪存编程窗口，然后单击
如下高亮显示的 "Run" 速度按钮。打开标准 CodeWarrior 调试窗口，从中可以执行所有标准调试操作。

![](/media/2018/CodeWarrior-run-speed-button.jpg)

 用于启动调试会话的 "Run" 速度按钮

---

### 配置和使用详情

#### RTOS 移植特定配置

此演示的特定配置项位于 [FreeRTOS/Demo/ColdFire_MCF52221_CodeWarrior/sources/FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中。可编辑
本文件中定义的常量，以适配您的应用程序。尤其是以下常量：

* **configKERNEL_INTERRUPT_PRIORITY** 和 **configMAX_SYSCALL_INTERRUPT_PRIORITY**
请参阅 RTOS 内核配置文档的[中断配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)章节以了解
 这些选项的完整信息。

 configKERNEL_INTERRUPT_PRIORITY 设置 RTOS 内核自身使用的中断优先级。configMAX_SYSCALL_INTERRUPT_PRIORITY 设置
 可以调用队列和信号量 API 函数的最高中断优先级。请注意，只有以 FromISR() 结尾的 API 函数才能在 ISR 中调用。

 configKERNEL_interrupt_PRIORITY 应设置为最低优先级。

 在硬件本身施加的限制范围内，configMAX_SYSCALL_INTRUPT_PRIORITY 以上级别的中断不会被 RTOS 内核关键部分掩盖，因此不受
 RTOS 内核活动的影响。

 通过演示，演示应用程序将 configMAX_SYSCALL_INTRUPT_PRIORITY 定义为 4 ，并将configKERNEL_INTRUPT_PRIORITY 定义为 1。

每个移植 # 定义 'BaseType_t' 等于该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，尚未实现 vPortEndScheduler ()。

#### 编写中断服务程序

中断服务程序可以使用标准的 CodeWarrior __declspec(interrupt) 函数修饰符用 C 语言编写。
提供宏 portEND_SWITCHING_ISR()，以允许中断程序请求执行上下文切换。
如下代码示出一个 UART 中断处理程序。请注意，此示例并不旨在演示高效的中断实现！

---

```c

/* The __declspec qualifier is used to tell the compiler the function is an ISR. */
__declspec(interrupt:0) void vUART0InterruptHandler( void )
{
unsigned char ucChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE, xDoneSomething = pdTRUE;

  while( xDoneSomething != pdFALSE )
  {
    xDoneSomething = pdFALSE;

    /* Does the tx buffer contain space? */
    if( ( MCF_UART0_USR & MCF_UART_USR_TXRDY ) != 0x00 )
    {
      /* Are there any characters queued to be sent? */
      if( xQueueReceiveFromISR( xCharsForTx, &ucChar, &xHigherPriorityTaskWoken )
                                                                      == pdTRUE )
      {
        /* Send the next char. */
        MCF_UART0_UTB = ucChar;
        xDoneSomething = pdTRUE;
      }
      else
      {
        /* Turn off the Tx interrupt until such time as another character
 is being transmitted. */
        MCF_UART0_UIMR = serRX_INT;
        xTxHasEnded = pdTRUE;
      }
    }

    if( MCF_UART0_USR & MCF_UART_USR_RXRDY )
    {
      ucChar = MCF_UART0_URB;
      xQueueSendFromISR( xRxedChars, &ucChar, &xHigherPriorityTaskWoken );
      xDoneSomething = pdTRUE;
    }
  }

  /* If using the xQueueReceiveFromISR() or xQueueSendFromISR() API
 functions caused to be unblocked, and the unblocked task has a higher priority than
 the interrupted task, then a context switch should be performed.
 portEND_SWITCHING_ISR() is used for this purpose. */
  portEND_SWITCHING_ISR( xHigherPriorityTaskWoken );
}

```

---

### RTOS 内核使用的资源

RTOS 内核使用 PIT0 定时器生成 RTOS 滴答 (tick)。可以更改函数 vApplicationSetupInterrupts() 以使用任何适宜的定时器源。

RTOS此外，RTOS 内核还需要一个额外的中断向量。因为使用了中断控制器 0 上的递送矢量 16，而  MCF5222x 上的矢量 16
未由任何外围设备使用，因此作为备用。RTOS 内核将此向量与中断强制寄存器 0 (INTFRCL0) 结合使用。
出于效率原因， 假设 RTOS 内核具有 INTFRCL0 寄存器的独占访问权限，因此不会尝试保持其状态，尽管
通过使用寄存器上的位集和清除，而非写入整个寄存器，可轻松改变改变此行为。

为确保用户可以灵活更改向量分配，PIT0 和向量 16 配置都在名为 FreeRTOS_tick_setup.c 的文件中执行，
这是用户应用程序的一部分，而非固定 RTOS 内核代码的一部分。

### 临界区

退出临界区将始终设置中断优先级，以便启用所有中断，无论输入临界区时的级别如何
。FreeRTOS API 函数本身将使用临界区。

### 执行上下文

出于效率原因，任务以主管权限运行。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/ColdFire_MCF52221_CodeWarrior/sources/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，即可使用抢占式内核；设置为 0
则可以使用协同式内核。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ColdFire 演示应用程序项目中，以提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。

