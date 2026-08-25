---
title: "FreeRTOS Spansion（前 Fujitsu）16FX 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/SK-16FX-EUROScope.jpg)  

此页面显示了适用于 Spansion MB96340 系列 RTOS 移植的 FreeRTOS 演示应用程序。

演示已预配置为可在 Spansion 的 SK-16FX-EUROScope 入门套件上运行。演示使用
Softune 编译器和 IDE
以及 EUROScope Lite 调试器，两者都包含在入门套件中。

---

### *重要！使用 Spansion（前 Fujitsu）16FX 演示的注意事项*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

16FX 演示的 Softune 工作区名为 96340_FreeRTOS_96348hs.wsp，位于 Demo/MB96340_Softune 目录。
下载的 FreeRTOS zip 文件包含所有移植文件和演示应用程序项目文件。因此其包含的文件
远多于此演示使用的文件。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，
了解下载文件的描述和有关创建新项目的信息。

---

### 演示应用程序

### 演示应用程序设置

演示应用程序包括中断驱动的 UART 测试，其中一个任务传输字符，然后由另一个任务接收。为使该功能正确运行，
必须将环回连接器连接到 SK-16FX-EUROScope 板的 X4 连接器上
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

您可以通过其 USB 端口为入门套件供电，并使用同一个 USB 端口作为虚拟 COM 端口。通过 USB 线首次连接入门套件时，
系统会提示您安装 USB 驱动程序。入门套件 CD 上提供了所需的驱动程序。

无需其他特定的硬件设置。

构建应用程序、编程闪存和调试都是通过单独的程序执行的——这些程序分别是 Softune 本身、Spansion Flash MCU 编程器
和 EUROScope lite。三个程序的安装可执行文件都提供在入门套件 CD 上。Softune 和 EUROScope 都需要您注册软件
并获取许可文件，不过此过程快速且免费。

### 构建演示应用程序

1. 在 Softune IDE 中打开 Demo/MB96340_Softune/96340_FreeRTOS_96348hs.wsp 工作区。
2. 在 IDE 的 Project 菜单中选择 "Build"，编译演示应用程序时不应含有错误或警告，不过链接阶段将输出警告，
 这是因为在 Softune 库中缺乏调试信息。链接器警告无法避免，但可被忽略。

### 对微控制器闪存进行编程

1. 使用 USB 线将入门套件连接到您的主机。
2. 启动 Spansion Flash MCU 编程实用程序。
3. 确保选择正确的 MCU 和晶体频率——下图中红色突出显示部分。

![](/media/2018/Fujitsu-flash-MCU-programming-utility.jpg)  
Spansion Flash MCU 编程实用程序
4. 使用 "Open" 按钮（上图蓝色突出显示部分）选择内置文件 Demo/MB96340_Softune/FreeRTOS_96348hs_SK16FX100PMC/STANDALONE/ABS/  
FreeRTOS_96348hs_SK16FX100PMC.mhx
5. 在 Flash 编程实用程序上，单击 "Set Environment"，并确保分配给 USB 连接的（虚拟）COM 端口被选中。Windows 设备管理器可用于
 检查分配给 USB 连接的端口：

	1. 在 Windows 控制面板中选择 "System"。"System Properties" 对话框将打开。
	2. 在该对话框中选择 "Hardware" 选项卡，然后单击 "Device Manager" 按钮（下图中红色突出显示部分）。Device Manager 窗口将打开。
	 ![](/media/2018/fujitsu-rtos-port-device-manager.jpg)  
	打开 Device Manager
	3. 展开 Device Manager 中的 "Ports (Com and LPT)" 节点，显示分配给 Spansion 连接的端口（下述情况下为 COM4）。


	![](/media/2018/fujitsu-virtual-com-port.jpg)  
	查看分配给 Spansion USB 连接的端口
6. 确保入门套件板上的开关 S1 处于编程位置（朝向 D 连接器），然后按蓝色按钮重置 MCU。
7. 最后，单击 Flash 编程实用程序中的 "Full Operation" 按钮（上图中黄色突出显示部分）。对闪存进行编程不应超过大约
 20 秒。
8. 要开始执行程序，请将 S1 移回到 "Run" 位置，然后再次按下入门套件上的蓝色按钮。确保
 环回连接器位于 X4 上（如上文“演示应用程序设置”中所述），然后重置主板。

### 启动调试会话

1. 按照说明对 MCU 闪存进行编程，将 RS232（或 USB 虚拟 COM 端口）线放置到位，并将开关 SW1 置于运行 ("run") 位置。
2. 确保 Flash 编程实用程序不再运行，因为它会阻止调试器访问 COM 端口。
3. 启动 EUROScope 调试软件。
4. 从 EUROScope 文件菜单中选择 "Open Application"，然后导航至 Demo/MB96340_Softune/FreeRTOS_96348hs_SK16FX100PMC/STANDALONE/ABS/  
FreeRTOS_96348hs_SK16FX100PMC.abs 并打开
 此文件。请注意，这次我们打开了.abs 文件，而在 Flash 编程实用程序中，我们打开了.mhx 文件。
5. 在 Euroscope 的 "Preferences" 菜单中选择 "Select Target Connection"，然后确保 “Fujitsu 16FXBootROM (RS232)” 被选中，如下所示。

![](/media/2018/Fujitsu-EUROScope-select-target-connection.jpg)  
确保选中 "Fujitsu 16FXBootROM (RS232)"
6. 在同一弹出窗口（如上所示）中，单击 "Configure"，打开 RS232 配置选项。[注意：该操作会锁定计算机一两分钟，无需惊慌，只需等待
 下一个对话框出现]。
7. 设置如下所示的通信选项——显然，要使用适合您的主计算机的 COM 端口，这可能不是如下所示的 COM1！

![](/media/2018/Configure-16FX-BootROM-connection.jpg)  
配置通信参数
8. 在 EUROScope 的 "Communications" 菜单中选择 "Open"。如果一切正常，您应该可看到源代码和汇编代码，准备进行调试。如果没看到，
 请单击 "Initialise target and run until main" 速度按钮。如果您仍然看不到源代码，请使用 EUROScope 的 "Preference" 菜单中的 “Source Paths” 选项，
 确保 EUROScope 正在尝试在正确的位置查找源文件。
9. 一旦建立了调试连接，就可按照预期那样使用 EUROScope 浏览代码、查看内存、设置断点等。

### 演示应用程序功能

演示应用程序创建了 8 个协程，31 个持久性任务，并定期动态创建和销毁另外 2 个任务。这些任务主要包含标准
演示应用程序任务（请参阅  （请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解各个任务的详细信息）。

除了标准演示任务外，还创建了以下任务和测试：

* 检查任务
 “检查”任务负责确保所有标准演示任务
 都按预期执行。检查任务通常每 3 秒执行一次，但
 其在系统内具有最高优先级，因此保证能够获得执行时间。检查任务发现的任何错误
 都会被锁定，直到处理器重置。在
 每个周期结束时，检查任务会切换 LED。如果所有任务执行时都不出错，LED 将每 3 秒钟切换一次；
 无论何时只要有任务报错，则切换速率会增加到 500 毫秒
 [可在执行演示时移除回环连接器来测试该机制，
 这样做是故意在
 "com test" 任务中生成一个错误]。
* 跟踪任务
 此任务仅当 INCLUDE_TraceListTasks 在 FreeRTOSConfig.h 内设置为 1 时才包含在构建中，并且仅可在独立执行（而不是通过调试器）时使用。

 跟踪任务是将执行跟踪和任务状态信息写入 UART 1 的用户交互式任务。 要查看菜单和提供的信息，请将 UART 1 连接到
 主机上的终端程序（例如超级终端）。使用的波特率为 9600。

SK-16FX-EUROScope 硬件包含一个 2 * 7 段的数值显示器，每个段都可以单独控制。除了这些段之外，显示器还包含两个 “.”
字符，也可以单独控制。这些段和 "." 字符为演示任务提供了便捷的输出，演示任务通常会使用常规的 LED。

如果演示应用程序正确执行，其表现如下：

* “检查”函数会每 3 秒钟切换 2 * 7 段显示器上的 “.” 字符。
* 如果构建中含有跟踪任务，则跟踪任务会通过 UART 1 向终端程序发送菜单选项。
* LED 闪烁任务会使用显示器上第一个字符的段——闪烁任务控制的段会
 以恒定速率切换，但各任务使用的频率不同。会创建 3 个闪烁任务。
* LED 闪烁协程会使用显示器的第二个字符。同样，每个协例程将以恒定速率切换段，
 但各协程使用的频率不同。会创建 8 个协程。

---

### RTOS 配置和使用详情

### 优化

请注意，如果优化级别设置为 0，移植将无法正常运行。这是因为 0 级优化会导致编译器
将
序言和尾声指令插入到 RTOS 内核使用的中断服务程序中以用于任务切换（即便是使用了 _nosavereg 函数限定符）。
如果需要 0 级优化，则
这些中断服务程序（包含在 RTOS 内核本身的可移植层中，并非应用程序代码中）将需要
用纯汇编代码重新编写。

### 寄存器库

16FX 移植不使用寄存器库。仅使用库 0。

### 内存模型

16FX 移植可使用小型、中型、紧凑型或大型内存模型。
Demo/MB96340_Softune/FreeRTOS_96348hs_SK16FX100PMC/Src/FreeRTOSConfig.h 中的 configMEMMODEL 定义必须设置为 portSMALL、
portMEDIUM、 portCOMPACT 或 portLARGE 以匹配项目设置。

![](/media/2018/fujitsu-softune-selecting-memory-model.jpg)  
在 Softune IDE 中选择内存模型，configMEMMODEL 设置必须
与所选项相匹配

### 看门狗 (Watchdog)

演示应用程序演示了为看门狗提供服务的三种方法：

1. 从 tick 中断内清除看门狗。
2. 从专用看门狗任务内清除看门狗。
3. 从闲置任务内清除看门狗。

可通过 Demo/MB96340_Softune/FreeRTOS_96348hs_SK16FX100PMC/SRC/watchdog/watchdog.h 的设置选择要使用的方法。

**注意：**这三种方法仅用于演示目的，因为这三种实现都过于简单，无法提供安全的看门狗机制。
如果需要安全的看门狗机制，则需要在看门狗定时器重置之前执行多种系统检查。

### RTOS 使用的资源

重新加载定时器 0 会生成 RTOS tick。
RTOS yield 函数会使用软件中断 122。

ISR 功能的 RTOS yield 会利用延迟中断。

### RTOS 移植特定配置

此演示的特定配置项位于 Demo/MB96340_Softune/FreeRTOS_96348hs_SK16FX100PMC/Src/FreeRTOSConfig.h 中。您可以编辑
本文件中定义的常量，以适配您的应用程序，特别是以下常量：

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS 滴答的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY**
 此常量设置了 RTOS 内核使用的中断优先级。
 RTOS 内核应使用低中断优先级（高数值），允许更高优先级的中断不受
 内核进入临界区的影响。临界区不是全局禁用中断，而是仅禁用
 低于 RTOS 内核中断优先级的中断。

 因此中断处理非常灵活：

	1. 在 RTOS 内核的优先级上，中断处理的“任务”
	 可以像系统中的任何其他任务一样被编写和优先处理。这些是被中断唤醒的任务。中断服务程序 (ISR) 本身应写得
	 尽可能短，因为它只是抓取数据，然后唤醒高优先级处理程序任务。接着，ISR 会直接返回到
	 唤醒的处理程序任务，因此中断处理在时间上是连续的，就像所有处理都是在 ISR 本身中完成的一样。这样的好处是
	 处理程序任务中的所有中断都保持启用状态。启用以太网的演示中的以太网驱动器使用处理程序任务演示该机制。
	2. 优先级高于 RTOS 内核优先级的 ISR 绝不会被 RTOS 内核本身屏蔽，因此其响应度不会受到 RTOS 内核功能的影响。
	 但是，此类 ISR 无法使用 FreeRTOS API 函数。快速定时器中断测试演示了这种行为。

每个移植会定义 (#define) 'BaseType_t' 为该处理器的最有效数据类型。本移植将
BaseType_t 定义为 short (16 位) 类型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档进行编写。
宏 portYIELD_FROM_ISR() 可用于从 ISR 内请求上下文切换。请参阅 Demo/MB96340_Softune/FreeRTOS_96348hs_SK16FX100PMC/Src/serial/serial.c，
查看示例。

### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/MB96340_Softune/FreeRTOS_96348hs_SK16FX100PMC/Src/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 ，可使用抢占式调度；设置为 0，
可使用协同式调度。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是基于提供的演示应用程序项目
搭建您的应用程序。

### 内存分配

Source/Portable/MemMang/heap_3.c 包含在演示应用程序项目中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。

### 串行驱动程序

请注意，提供的串行驱动器示例旨在演示 RTOS 内核的某些功能，并非表示最佳解决方案。

