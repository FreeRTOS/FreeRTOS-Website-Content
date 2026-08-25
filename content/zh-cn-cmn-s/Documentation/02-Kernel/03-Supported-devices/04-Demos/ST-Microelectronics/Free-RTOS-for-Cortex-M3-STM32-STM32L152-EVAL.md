---
title: "FreeRTOSSTM32L152 ARM Cortex-M3 微控制器的演示"
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
| <br />![](/media/2018/FreeRTOS-running-on-an-STM32L154-EVAL-evaluation-board.jpg)<br /> |

### 引言

 [[另请参见演示项目：使用 FreeRTOS 无滴答模式
 来最大限度地减少在 
 STM32L](STM32L-discovery-low-power-tickless-RTOS-demo) 上运行的应用程序的功耗]

本页记录了低功耗 FreeRTOS STM32L152 微控制器 [](http://www.st.com/internet/mcu/product/248824.jsp的) 演示应用程序。
控制器来自 [STMicroelectronics](http://www.st.com/)。演示使用 [IAR Embedded Workbench for ARM V6.10](http://www.iar.com/ewarm) - 
来自 IAR Systems，并针对官方的 [STM32L152-EVAL](http://www.st.com/internet/com/TECHNICAL_RESOURCES/TECHNICAL_LITERATURE/USER_MANUAL/CD00288880.pdf) 评估板，
来自 STMicroelectronics（我们提供了[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)，
如果您希望使用替代开发板）。

** 注意：**如果项目生成失败，可能是因为您使用的 IAR
嵌入式工作台版本过低。如果是这种情况，
那么也可能是项目文件(在无提示的情况下)已经损坏，因此需要
还原到原始状态，然后使用新版本的 IAR 生成项目。

6.10 版本预先安装了 FreeRTOS 状态查看器插件，
无需手动安装。

#### 此页面上展示的项目演示的FreeRTOS 功能

该项目演示了以下 FreeRTOS 功能和技术：
* 'gatekeeper' 任务设计模式

 演示 LCD 任务是唯一有权访问 LCD 的任务。
 其他任务和中断想要向 LCD 写入消息时，不会直接这么做，
 而是通过向 LCD 任务发送信息。
* 'controller' 任务设计模式

 演示 LCD 任务还演示了 'controller' 任务概念。
 发送到 LCD 的消息包含一个消息类型和
 一个消息值参数。LCD 任务知道如何处理消息
 值（可以是整数、字符指针或其他任何东西），
 因为它可以解释消息类型。
* 受控（非自由运行）的输入轮询

 一个演示按键轮询的任务使用 FreeRTOS的时间延迟功能
 来控制读取按键输入状态的速度。因此
 不需要复杂的按键消抖，同时避免任务
 占用了所有可用的 CPU 时间。
* （有效和间接地）从中断服务程序写入 LCD

 通常无法从中断服务程序中高效使用
 LCD 等慢输出装置。在本演示中，操纵杆选择按键
 用于生成外部中断，中断服务程序
 通过将字符串发送到一个消息队列中的 LCD 任务
 来将字符串间接发送到 LCD。
* 收集和显示运行时间统计

 运行时间统计提供每个任务处于运行状态
 的时间。时间是以绝对值和
 占总运行时间的百分比呈现。
* 中断嵌套

 USART3 Rx 和 Tx 中断设置的优先级比
 系统中使用的任何其他中断的优先级都要高（包括
 RTOS 内核自身使用的中断）。因此，USART3 中断将
 中断（嵌套）任何其他中断。
* 空闲任务钩子函数

 空闲任务钩子用于将处理器置于低能耗
 状态。请注意，演示的实现使用标准
 任务实现来实现，因此
 未针对低功耗操作进行优化。将轮询任务转换为事件驱动任务，
 降低滴答中断频率等，
 可以实现更低的功耗。
* 滴答中断钩子函数

 滴答中断钩子用于实现 'watchdog' 类型的功能。
 它会监控系统中的其他所有任务，查找任何异常
 行为，然后发送 PASS 或错误代码状态消息
 到 LCD/Controller 演示任务。LCD/Controller 演示任务使用
 其接收消息的消息类型成员来将消息
 解释为状态消息，然后使用其接收消息的消息值成员
 来决定写入 LCD 的状态字符串。
* malloc() failed 钩子函数

 malloc() failed 钩子会捕获对 pvPortMalloc() 的
 失败调用，这是用于完成分配的 FreeRTOS 堆内存
 不够而导致的。
 可以从应用程序任务中调用 pvPortMalloc()，也可以
 从创建任务、队列和信号量的 FreeRTOS API 函数中调用。
* 查询待分配的 FreeRTOS 堆内存数量

 从一个任务中调用 xPortGetFreeHeapSize()（RTOS 调度器启动后），
 将待分配的 FreeRTOS 堆内存
 （因此这部分内存可用）输出到终端 IO 窗口
 （位于 IAR Embedded Workbench IDE 中）。

---

### *重要提示！使用 STM32 ARM Cortex-M3 演示的注意事项*

*使用此 RTOS 移植之前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法
运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码，因此
包含的文件比此演示所需更多的文件。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，
了解关于已下载文件的说明
的信息。

STM32L152 演示的 IAR 工作区文件名称是 RTOSDemo.eww，
位于 FreeRTOS/Demo/CORTEX_STM32L152_IAR 目录。

---

### 演示应用程序

#### 演示应用程序硬件设置

演示应用程序包含中断驱动的 UART 测试。这会产生两个
任务，包括一个发送任务和一个接收任务。传输任务将字符传输到
USART3 上，接收任务接收 USART3 上的字符。接收任务
应该接收传输任务传输的字符，因此为了实现正确操作，
必须将一个回环连接器连接到
STM32L152-EVAL 评估板上的 USART3/CN5 连接器上（引脚 2 和 3 必须
在 CN5 9Way 连接器上连在一起）。并且 USART3 相关的跳线 JP5、JP7 和 JP8
必须设置为将引脚 2 和 3 短路（而不是设置为
将引脚 1 和 2 短路）。

演示应用程序还使用内置在 STM32L152-EVAL 上的
所有四个 LED。跳线 JP18 and JP19 必须被闭合（短路），LED3 和 LED4 才能
运行。

该端口的开发和测试使用
连接到目标硬件上的 CN8 的 J-LInk USB JTAG 接口。评估硬件还提供
一个内置的 ST-Link 调试接口，可使用
标记为 ST-Link/CN11 的 USB 连接器访问。

#### 构建和运行演示应用程序

1. 从 Embedded Workbench IDE 中打开 FreeRTOS/Demo/CORTEX_STM32L152_IAR/RTOSDemo.eww 项目。
2. 从 IDE 的 'Project' 菜单中选择 'Rebuild All'。项目若构建成功，不会报错或出现警告。
3. 在 IDE 的'Project' 菜单中选择 'Debug'。将用新建二进制数组对微控制器闪存进行编程，而且调试器将
 在进入 main() 时中断。

#### 功能

此文档页面顶部列出了 FreeRTOS 功能
在 STM32L152 演示项目中的演示。main.c 源文件中的注释
提供了有关如何实现和实现此功能的
实现和实施的。

演示正常执行时，将观察到以下行为：

* LED1、LED2 和 LED3 受标准 'flash' 任务
 控制。每个 LED 将以不同的固定频率切换。LED1
 将以最高频率切换，LED3 将以最低频率
 切换。
* 每当 COM 测试传输任务传输
 一个字符时，LED4 都会切换。
* 每 5 秒钟将向 LCD 写入状态消息。如果
 演示正在执行，没有错误，则状态将被
 报告为 PASS。在所有其他情况下，状态消息将指示
 哪个任务或测试报告了错误。可以对此功能进行测试。
 移除 USART3/CN5 连接器上的回环连接器，
 这样做会故意在 COM 测试任务中生成错误。
* 按下或释放操纵杆的 'up' 按键
 显示一条信息，指示按键状态
 （0 表示按下，1表示释放）。
* 按下操纵杆的 select 按键
 （直接向下朝向其底部的 PCB 按下），
 会在 LCD 上显示一条消息，指示已生成
 按键中断。它还将导致运行时间统计
 （自演示启动之后，每个任务在运行状态下花费的时间）
 被输出到 Embedded Workbench IDE 的
 中断 IO 窗口中（请参见下方屏幕截图）。

下方图片是在调试会话期间的屏幕截图。FreeRTOS状态查看器的
“任务和队列”窗口可以在
屏幕截图底部。终端 IO 窗口中可以看到运行时间
统计信息。

![FreeRTOS STM32L152 调试会话屏幕截图](/media/2018/FreeRTOS-STM32L152-Debug-Session-Screen-Shot.jpg)

** FreeRTOS 调试会话期间的屏幕截图。
FreeRTOS
 状态查看器插件窗口可以在屏幕截图底部看到。

 运行时间统计信息可以在终端 IO 窗口中看到。**

---

### RTOS 配置和使用详情

#### RTOS 移植特定配置

这些演示的特定配置项目包含在 FreeRTOS/Demo/CORTEX_STM32L154_IAR/FreeRTOSConfig.h 中。可以编辑
此文件中定义的常量，以适配您的应用程序。特别是以下常量：

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

#### 中断服务程序

与大多数移植不同，导致上下文切换的中断服务程序
没有特殊要求，可根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 中请求上下文切换。

请注意，portEND_SWITCHING_ISR() 会使中断保持启用。

此演示项目提供了 FreeRTOS 中断服务程序示例，
即在 main.c 中定义的 TIM6_IRQHandler() defined 和
在 serial.c 中定义的 USART3_IRQHandler()。请注意，实现 USART3_IRQHandler() 是为了强调端口和
演示终端使用的队列，此演示的制作并不是为了
演示高效的中断服务程序！

#### 在抢占式和协同式 RTOS 内核之间切换

在 FreeRTOS/Demo/CORTEX_STM32L154_IAR/FreeRTOSConfig.h 中将 定义 configUSE_PREEMPTION 设置为 1 以使用抢占式，
或设置为 0 以使用协同式。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

Source/Portable/MemMang/heap_2.c 位于 ARM Cortex-M3 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
