---
title: "Spansion（原名Fujitsu）FM3 演示使用 Keil 和 IAR 开发工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Fujitsu SK-FM3-100PMC MB9BF506 开发和评估板](/media/2018/Fujitsu-SK-FM3-100PMC-MB9BF506-development-and-evaluation-board.jpg)  
Spansion SK-FM3-100PMC MB9BF506 入门套件评估板，  
同时还为 SK-FM3-64PMC1 入门套件提供了一个项目

本页记录的 FreeRTOS ARM Cortex-M3 演示应用程序面向 Spansion
[FM3 微控制器](http://www.spansion.com/Products/microcontrollers/32-bit-ARM-Core/fm3/Pages/overview_32fm3.aspx)。
IAR 和 Keil 项目已预先配置为
在 SK-FM3-100PMC 和
SK-FM3-64PMC1
入门套件评估板上运行。评估板上装有
MB9BF506N
和 MB9AF314 微控制器。

**注意：**如果项目构建失败，很可能是使用的IAR
嵌入式工作台版本过低。如果构建失败，
那么也可能是项目文件(在无提示的情况下)已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR 。

---

### *重要提示！FreeRTOS Keil 和 IAR FM3 示例项目使用说明*

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#spansion-fm3-mb9bf500mb9af300-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS zip 下载文件中包含所有 FreeRTOS 移植
以及各演示应用程序项目的源代码。
因此，该下载包中所包含的文件远多于构建和运行 FM3 MB9BF500 演示所需的文件。请参阅
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节详细
查阅已下载文件的描述以及关于创建新项目的信息。

下表提供了有关
在 FreeRTOS 官方下载中查找相关 FM3 项目的信息：

|  |  |  |  |
| --- | --- | --- | --- |
| **编译器**  | **目标板**  | **项目名称**  | **项目文件在FreeRTOS源树中的位置**  |
| <br /> IAR<br />  | <br /> MB9B500<br />  | <br /> RTOSDemo_IAR.eww<br />  | <br /> FreeRTOS/Demo/CORTEX_MB9B500_IAR_Keil<br />  |
| <br /> IAR<br />  | <br /> MB9A300<br />  | <br /> RTOSDemo_IAR.eww<br />  | <br /> FreeRTOS/Demo/CORTEX_MB9A310_IAR_Keil<br />  |
| <br /> ARM/Keil<br />  | <br /> MB9B500<br />  | <br /> RTOSDemo_Keil.uvproj<br />  | <br /> FreeRTOS/Demo/CORTEX_MB9B500_IAR_Keil<br />  |
| <br /> ARM/Keil<br />  | <br /> MB9A300<br />  | <br /> RTOSDemo_Keil.uvproj<br />  | <br /> FreeRTOS/Demo/CORTEX_MB9A310_IAR_Keil<br />  |

---

### Spansion FM3 MB9BF500/MB9AF300 演示应用程序

#### 功能

IAR 和 Keil 项目各自包含三项构建配置：

|  |  |
| --- | --- |
| **构建配置** | **描述** |
| <br /> Blinky<br />  | <br /> 此配置**非常简单**。此配置会创建两项任务，<br /> 一项为创建软件定时器，另一项为使用按钮中断。<br /> <br /> 两项任务通过队列进行通信，每次接收到一个值时，<br /> 接收任务都会切换其中一个七段显示 LED<br /> 。本文档页面的[“Blinky 演示功能”](#直观的-blinky-演示功能)<br /> 部分重点介绍了所使用的 LED。<br /> <br /> 按下用户按钮 SW2 会产生中断，中断服务程序<br /> 会在打开 LED 之前重置软件定时器。<br /> 软件定时器的周期为 5 秒，5 秒过后，<br /> 定时器回调函数会再次关闭 LED。<br /> 因此，按下 SW2 会打开 LED，<br /> 而且如果没有再次按下按钮，整个 5 秒钟内，<br /> LED 一直保持亮起状态。<br /> <br /> Blinky 构建配置使用<br /> main-blinky.c 源文件。另外两个构建配置则使用<br /> main-full.c 源文件。<br /> <br /> |
| <br /> Full<br />  | <br /> 这是一个全面的配置，会创建许多任务、<br /> 队列、（各种类型的）信号量和软件定时器。<br /> <br /> Full 配置创建的任务和定时器，<br /> 与 Blinky 构建配置创建的相同。除此之外，<br /> Full 配置还会根据<br /> [标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)<br /> 任务集创建许多任务。<br /> <br /> 标准演示任务并不执行任何特定函数。<br /> 其目的首先是测试 FreeRTOS 移植，其次是<br /> 举例说明如何使用 FreeRTOS API 函数。<br /> <br /> Full 构建配置还会创建一些定时器，<br /> 这些定时器既不属于 Blinky 配置，也不属于标准演示任务集。<br /> 本表下方简要介绍了这些额外任务。<br /> <br /> Full 配置总共创建了近 45 项任务！<br /> 如果需要更简单的演示，则请使用 blinky 构建配置。<br /> <br /> |
| <br /> Full_with_optimisation<br />  | <br /> Full_with_optimisation 配置的功能<br /> 与 Full 配置的功能相同。两者之间的唯一区别在于<br /> 编译器优化设置。<br /> Full 不使用优化，而 Full_with_optimisation 使用高度<br /> 优化。<br /> <br /> |

Full 构建配置可创建如下软件定时器
（既不属于 Blinky 演示，也不属于标准演示任务）：

* “检查”软件定时器和回调
 每次检查定时器过期时，其关联的回调函数
 都会查询所有正在运行的标准演示任务的状态。如果状态
 返回为“失败”，则检查定时器的周期
 会从其原始设置的 3 秒缩短到 500 毫秒。

 每次执行时，检查定时器回调都会
 切换七段显示中的 LED。本文档页面的[“Blinky 演示功能”](#直观的-blinky-演示功能)
 和 [Full 演示功能](#直观的-full-演示功能)部分
 部分重点介绍了所使用的 LED。因此，如果 LED 每 3 秒切换一次，
 则未报告错误。如果 LED 每 500 毫秒切换一次，则至少有一个
 标准演示任务报告了错误。报告错误的标准演示任务的名称
 记录在 pcStatusMessage 变量中，
 该变量在 main-full.c 中定义。
* “数字计数器”软件定时器和回调
 控制在两个七段显示器上
 递增数字的显示。

#### 硬件设置

演示应用程序包含通过 UART0 发送和接收字符的任务。
一个任务发送的字符必须由另一个任务接收。
如果任何字符丢失或接收到故障，则会标记错误情况。SK-FM3-100PMC 开发板上
标有 X4 的 9 芯 D 型插座上需要一个环回连接器，
才能进行此测试
（插座的引脚 2 和 3 必须连接在一起，通常使用回形针即可）。此外，标记为 JP4 和 JP5 的跳线
必须设置为将 UART0 信号路由到 X4 连接器。
这需要将跳线从默认位置旋转 90 度。JP4 和
JP5 与 X4 连接器相邻，其所需的位置请参见
此文件顶部的图片（跳线应指向连接器，
而不是与连接器平行）。

请注意，此演示中的 UART 驱动程序使用队列
分别将每个字符送入中断服务程序和提出中断服务程序
。这样做的目的，是为了演示在中断中使用的队列，
有意加载系统以测试FreeRTOS移植。这并非是要作为
高效驱动器实现的示例。一个有效的实现
应使用 FIFO 或 DMA（如可用），并且仅在接收到足够的数据FreeRTOS
以保证任务被解锁以处理数据时才使用
API 函数。

#### 使用 IAR 工具构建和执行演示应用程序

1. 打开 [RTOSDemo_IAR.eww](#源代码组织)嵌入式工作台工作区
 (从嵌入式工作台 IDE 中打开)。
2. 选择所需的构建配置。
3. 从嵌入式工作台的 "Project" 菜单中选择 "Build All",
 演示应用程序的构建不应出错。
4. 构建完成后，从嵌入式工作台的 "Project" 菜单中选择 "Download and Debug"
 （或直接按 CTRL+D），即可对微控制器闪存进行编程，
 然后启动调试会话。应用程序将开始运行，然后
 在进入 main() 函数时中断。

#### 使用 Keil 工具构建和执行演示应用程序

1. 从 Keil IDE 内打开[RTOSDemo_Keil.uvproj](#源代码组织)
 项目。
2. 选择所需的构建配置。构建配置
 在 uVision IDE 中名为 "target"。
3. 从 IDE 的 "Project" 菜单中选择 "Build Target"，
 演示应用程序应能成功构建，没有错误。
4. 构建完成后，从 IDE 的 "Debug" 菜单中选择 "Start/Stop Debug Session"
 （或直接按 CTRL+F5），即可对微控制器闪存进行编程，
 然后启动调试会话。

#### 直观的 blinky 演示功能

![SpansionFM3FreeRTOSblinky 烁演示 LED 作业](/media/2018/FM3-blinky-demo-led-assignment.jpg)

 "blinky" 构建配置使用的 LED 分配

"blinky" 构建配置正确执行时：

* LED 定时器使用上图中标有“A”的 LED。按下
 用户按钮 SW2 时，该 LED 将打开，
 如果按下 SW2 未达 5 秒钟，该 LED 将关闭。
* 队列接收任务使用上图中标有“B”的 LED。
 该 LED 每次在队列中接收到项目时都会切换
 （因此每 200 毫秒切换一次）。

#### 直观的 full 演示功能

![SpansionFM3FreeRTOS完整演示 LED 作业](/media/2018/FM3-full-demo-LED-assignment.jpg)

 “full”构建配置使用的 LED 分配

由 full 演示创建的许多任务和定时器中只有少数具有
外部可观察的行为。“full”构建配置正确执行时：
将观察到以下行为：

* 上图中标记为 A 的 LED 由
 “数字计数器”定时器控制。这些 LED 将显示一个从 0 到 9 重复
 递增的数字。
* 上图中标有 B 的 LED 由“Check”软件定时器控制。
 如果没有报错，此 LED 将每 3 秒切换一次，
 如果标准演示任务报错，则每 500 毫秒切换一次。
 可通过移除回环连接器来测试该机制，
 这样做会故意在“comtest”测试任务中生成错误。
* 上图中标记为 C 的 LED 由
 标准演示“comtest”任务控制。每次传输字符时，都会切换一次状态，
 而每次接收到相同的字符时，也会切换一次状态，切换速率
 非常快，而且只有肉眼可见。
* LED 定时器使用上图中标有“D”的 LED。按下
 用户按钮 SW2 时，该 LED 将打开，
 如果按下 SW2 未达 5 秒钟，该 LED 将关闭。
* 上图中标记为 E 的 LED 由
 “flash”任务控制。每个 LED 将以固定频率切换，
 三个 LED 中都使用不同的频率。
* 标记为 F 的 LED 由队列接收任务控制。
 该 LED 每次在队列中接收到项目时都会切换
 （因此每 200 毫秒切换一次）。

---

### RTOS 配置和使用详情

#### Cortex-M3 FreeRTOS 移植特定配置

此演示特定的配置项位于 FreeRTOS/Demo/CORTEX_MB9B500_IAR_Keil/FreeRTOSConfig.h（或
FreeRTOS/Demo/CORTEX_MB9A310_IAR_Keil/FreeRTOSConfig.h）
[可以编辑此文件中定义的常量，以适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

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
FM3 微控制器上可以指定的最低优先级实际上为 15，这是由
FreeRTOSConfig.h中的常量 configLIBRARY_LOWEST_INTERRUPT_PRIORITY 定义。可指定的最高优先级
始终为零。

我们还建议确保将所有四个优先级位分配为
抢占式优先级位，不要将任何优先级位分配为子优先级位。

每个移植都将 "BaseType_t" 
\#定义为处理器最有效的数据类型。此移植将 BaseType_t 定义为长类型。

#### 中断服务程序

与大多数移植不同，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于在
中断服务程序内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

此演示项目提供了 FreeRTOS 中断服务程序示例，
即在 main-full.c 和 main-blinky.c 中定义的 INT0_7_Handler() 以及
在 serial.c 中定义的两个 UART 中断处理程序 MFS0RX_IRQHandler() 和 MFS0TX_IRQHandler()
。

只有以 "FromISR" 结尾的 FreeRTOS API 函数可以从
中断服务程序中调用 - 而且中断的优先级须
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY 配置常量设置的
优先级。

#### FreeRTOS 使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

#### 在抢占式和协同式 RTOS 内核之间切换

将 RTOSDemo/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式调度；
设置为 0 以使用协作式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

FM3 演示应用程序项目中内置 Source/Portable/MemMang/heap_2.c，以
提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。
