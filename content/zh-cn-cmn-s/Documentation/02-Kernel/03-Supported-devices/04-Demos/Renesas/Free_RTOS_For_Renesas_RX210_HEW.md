---
title: "使用 Renesas 编译器 和 HEW IDE 的 Renesas RX200 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/Renesas-RSKRX210.jpg)  
Renesas RX210 入门套件 (RSK)

本页面记录 [Renesas RX210](http://www.renesas.eu/products/mpumcu/rx/rx200/rx210/rx210_root.jsp)
FreeRTOS 移植以及使用 [Renesas RX](http://www.renesas.com/compiler) 编译器
和 [HEW IDE](http://www.renesas.com/hew) 的演示应用程序。该项目被预置为在 RSKRX210 入门套件上运行。

此演示应用程序会演示以下几个方面：

* 使用[**永远不会r**
 被 RTOS 内核禁用的中断优先级的高频中断](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)。
* 中断嵌套的深度为 4 层。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* Malloc 失败、堆栈溢出和空闲[钩子函数](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)。

---

### *重要提示！关于使用 Renesas RX200 移植和演示应用程序*的说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#重要提示关于使用-renesas-rx200-移植和演示应用程序的说明)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题: [我的应用程序未运行，哪里出错了?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

RSK 开发板的 HEW 工作区名为 RTOSDemo.hws，位于
FreeRTOS/Demo/RX200_RX210-RSK_Renesas 目录。

FreeRTOS zip 文件下载内容包含所有 FreeRTOS 移植的实现和每个官方
演示应用程序项目。因此，包含的文件比此演示使用的文件多。请参阅
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节了解
下载文件的描述和有关创建新项目的信息。

---

### RX210 演示应用程序

#### 功能

该项目包括三项构建配置：

|  |  |
| --- | --- |
| **构建配置** | **描述** |
| <br /> Blinky<br />  | <br /> 这是一个**非常简单的示例**，它创建了两个任务和<br /> 一个队列。任务之间通过队列进行通信，<br /> 一个 LED is toggled on each successful queue receive. The main()<br /> 被 Blinky 构建配置使用的函数定义于<br /> main-blinky.c 中。另外两个构建配置使用的 main() 函数<br /> 定义于 main-full.c。<br />  |
| <br /> Debug<br />  | <br /> 该演示非常全面，<br /> 在启动 RTOS 调度器之前创建了 50 个任务，接着会在应用程序执行期间不断地动态创建和<br /> 删除另外两个任务。它还创建<br /> 许多队列和不同类型的信号量。该任务主要<br /> 由[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)任务组成。这类任务<br /> 仅测试移植和演示 FreeRTOS API 的使用方法，并不执行其他特定功能。<br /> 此表格下方提供创建的其他任务的信息。<br /> Debug 构建配置包括标准演示任务，该任务演示<br /> 中断嵌套，但不包含高频定时器中断。<br />  |
| <br /> Debug_with_optimisation<br />  | <br /> 该示例与 Debug 构建配置相似，但包含<br /> 高频定时器中断。该构建配置还对<br /> 编译器进行最大优化。<br />  |

Debug 和 Debug_with_optimisation 构建配置除了创建标准演示任务之外，还创建了以下任务、定时器和测试：

* 检查定时器和回调函数

 检查定时器是一种非常简单的监视定时器。它会监视
 其他所有标准演示任务和寄存器测试任务（如下所述），
 并使用 LED 为系统状态提供视觉反馈。

 检查定时器的周期最初设置为 5 秒。检查
 定时器回调函数检查所有标准演示任务和
 寄存器测试任务，不仅检查任务是否正在执行，还检查任务是否没有
 报告任何错误，然后切换 LED。

 如果检查定时器任务发现某个任务停止，或者报告了
 错误，那么它会将自己的周期从最初的 5 秒降低到
 只有 200 毫秒。因此，如果 LED 每 5 秒钟切换一次，那么没有发现任何问题，
 而如果 LED 每 200 毫秒切换一次，那么
 至少有一个任务存在问题。

 检查定时器使用 RSK 丝网上标有 LED3 的LED。
* 寄存器测试任务

 这两个任务会测试 RTOS 内核上下文切换机制：
 首先用已知的唯一值填充各个 RX200 寄存器，然后反复检查
 写入寄存器的原始值
 是否在整个任务周期内均保持在寄存器中。这些任务以尽可能低的优先级执行
 （空闲优先级），因此经常被抢占。这些
 任务的性质要求它们必须以汇编语言编写。
* 高频定时器测试

 此测试配置一个定时器，生成一个频率为 20 KHz 的中断。中断优先级高于
 [configMAX_SYSCALL_INTERRUPT_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，因此不会
 被 RTOS 内核禁用。中断定时中的抖动被测量
 并存储在变量中，可供调试器检查。
* 按钮输入中断和 LCD 演示

 该演示定义了三个由按钮点击触发的 IRQ 中断处理程序：
 一个任务控制 LCD 的顶行，一个任务
 控制 LCD 的底行以及一个队列用于
 中断处理程序和任务间通信。

 控制 LCD 顶行的任务仅来回滚动消息，
 当消息到达 LCD 末端，就改变消息的滚动方向
 。

 在按下 SW2 按钮之前，控制 LCD 底行的任务的行为与控制 LCD 顶行的任务相似
 。按下
 SW2 按钮生成中断。中断处理程序使用
 上述队列向任务发送指令，命令其暂停或重启
 滚动动作。滚动
 暂停时，按下 SW3 和 SW1 按钮导致中断，
 进而生成指令。这些指令通过同一个队列发送到任务，命令
 任务分别向左和向右移动消息（每次一个字符）
 。

演示应用程序执行时表现如下：

* LED 0、1 和 2 由标准 "flash" 任务控制。每个 LED 会以不同的固定频率切换：LED 0
 的频率最高，LED 2 的频率最低。
* LED 3 由 'check' 定时器任务控制。如果其他所有任务报告状态为正常，它将
 每 5 秒切换一次。如有任何任务报告了错误，它将每 200 毫秒切换一次。
* "http://www.FreeRTOS.org" 将沿着 LCD 顶行从左向右连续滚动，然后从右向左滚动。
* 描述 RX210 可用功能的长字符串将沿着 LCD 的底行从左向右滚动，然后从右向左滚动，
 直到按下 SW2 按钮。按下 SW2 按钮将暂停滚动，再次按下
 SW2 按钮将使字符串再次开始滚动。当字符串静止时，按下 SW3 按钮会将字符串
 向左移动，每次一个字符，而按下 SW1 按钮会将字符串向右移动，每次一个字符。

#### 构建和执行演示应用程序

1. 打开项目前，使用 RSK 套件提供的 [E1 FINE 接口](http://www.renesas.com/e1)将 RX210 RSK 连接到主机
 。连接之后，给开发板通电。
2. 在 HEW IDE 中打开 FreeRTOS/Demo/RTOSDemo.hws 工作区，打开项目时，按照提示
 连接到目标接口。
3. 在 HEW 的 "Build" 菜单中选择 "Build"，演示应用程序应当成功构建，没有任何实质错误或警告，
 尽管预处理器（莫名）查找构建中被预处理器命令省略的头文件时会产生依赖错误，
 但这些错误不会影响构建。
4. 构建完成后会出现一个对话框，询问是否要将生成的二进制文件下载到
 RX210 微控制器，选择 "yes" 对闪存进行编程并启动调试会话。调试器将在进入
 main() 函数时中断。

---

### RTOS 配置和使用详情

#### FreeRTOS RX200 RTOS 移植特定配置

此演示的特定配置项目位于 FreeRTOS/Demo/RX200_RX210-RSK_Renesas/RTOSDemo/FreeRTOSConfig.h。可以
根据您的应用需求来编辑常量。特别是：

* **configTICK_RATE_HZ** 

 设置 RTOS tick 的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但它高于大多数应用程序所需的频率。
 降低该频率有助于提高效率。
* **configKERNEL_INTERRUPT_PRIORITY** 

 定义 tick 和 yield 中断的中断优先级
 （RTOS 内核中断）。configKERNEL_INTERRUPT_PRIORITY 通常应设置为
 最低中断优先级，在 RX200 内核中为 1。请参阅
 [定制页面](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，了解更多信息。
* **configMAX_SYSCALL_INTERRUPT_PRIORITY** 

 定义可以据其调用 FreeRTOS API
 。处于或低于此优先级的中断可以调用 FreeRTOS API
 API 函数，**前提是**该 API 函数以 "FromISR" 结尾。
 高于此优先级的中断不能调用任何 FreeRTOS API 函数，
 但不会被 RTOS 内核禁用。因此，优先级高于
 configMAX_SYSCALL_INTERRUPT_PRIORITY
 的中断适用于定时精度要求极高的功能。此演示中的高频定时器测试
 使用的优先级高于
 configMAX_SYSCALL_INTERRUPT_PRIORITY 定义的优先级。请参[阅配置页面](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，了解详细信息。

RX200 移植层定义 (#define) "BaseType_t" 为 "long"。

#### 编写中断服务程序 (ISR)

可以使用标准 Renesas 编译器语法实现中断服务程序
。例如，演示应用程序使用以下方法定义高频定时器：

```c

/* The 'enable' in the following line causes the compiler to generate code that
re-enables interrupts on function entry. This will allow interrupts to nest
(although in this case the high frequency timer interrupt is the highest priority
interrupt in the demo). */
#pragma interrupt ( prvTimer2IntHandler( vect = _VECT( _CMT2_CMI2 ), enable ) )
static void prvTimer2IntHandler( void )
{
    /* ISR implementation goes here. */
}

```

请参阅 Renesas 提供的示例和编译器文档，了解详细信息。

通常，ISR 想要触发上下文切换，因此当 ISR
处理完成时，ISR 返回的任务不同于 ISR
最初中断的任务。如果 ISR 导致某个任务被解除阻止，
且该任务的优先级高于处于“运行”状态的任务（被中断的任务），
就会出现这种情况。为此，我们提供了 portYIELD_FROM_ISR()。
portYIELD_FROM_ISR() 采用单个参数：如果参数为
零，则不切换上下文；如果参数不为零，
则切换上下文。下列代码演示了上述内容，
这是 RX210 演示的一部分，并在
FreeRTOS/Demo/RX200_RX210-RSK_Renesas/RTOSDemo/ButtonAndLCD.c 中实现。

```c

/* The 'enable' in the following line causes the compiler to generate code that
re-enables interrupts on function entry. This will allow interrupts to nest. */
#pragma interrupt ( prvIRQ1_Handler( vect = 65, enable ) )

static void prvIRQ1_Handler( void )
{
static TickType_t xTimeLastInterrupt = 0UL;
static const unsigned char ucCommand = lcdSHIFT_BACK_COMMAND;
BaseType_t xHigherPriorityTaskWoken;

  /* prvSendCommandOnDebouncedInput() returns true or false, depending on
 whether the function unblocked a task that has equal or higher priority than the task
 that is already in the running state. */
  xHigherPriorityTaskWoken = prvSendCommandOnDebouncedInput( &xTimeLastInterrupt,
                                                             ucCommand );
  portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

```

#### FreeRTOS使用的资源

FreeRTOS 需要独占使用软件中断。
FreeRTOS 还需要独占使用定时器，该定时器能够生成周期性嘀嗒中断，但是
要由应用程序编写者定义使用哪个定时器。

应用程序必须定义一个名为 vApplicationSetupTimerInterrupt() 的函数，
来配置 tick 中断，然后定义 configTICK_VECTOR 为与所选定时器源相关的中断矢量号
。

建议使用比较匹配定时器来生成 tick 中断，
例如，vApplicationSetupTimerInterrupt() 的实现使用了比较匹配定时器 0，
包含在此演示应用程序的 main-full.c 和 main-blinky.c 中。
演示应用程序将 FreeRTOSConfig.h 中的 configTICK_VECTOR 定义为 _CMT0_CMI0（比较
匹配 0 中断向量号）。提供的示例实现可用于
任何自身不需要使用比较匹配 0 定时器/中断的应用程序。

#### 在抢占式和协同式 RTOS 内核之间切换

将 RTOSDemo/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式调度；
设置为 0 以使用协作式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

RX210 演示应用程序项目中内置 Source/Portable/MemMang/heap_2.c，以
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 部分，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。
