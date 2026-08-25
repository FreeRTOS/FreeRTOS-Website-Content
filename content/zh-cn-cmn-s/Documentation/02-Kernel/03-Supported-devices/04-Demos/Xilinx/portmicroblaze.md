---
title: "Xilinx Virtex-4 FPGA 上的 Microblaze 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![ml403.jpg](/media/2018/ml403.jpg)
经XilinxInc 许可复制的映像

本页面上介绍的移植和演示现已弃用。
最新演示的链接可在
[这里](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#XILINX)查找。

Microblaze 移植使用[PowerPC & MicroBlaze Virtex-4 FX12 版开发套件](http://www.xilinx.com/products/devkits/HW-V4-ML403-UNI-G.htm)开发。该套件功能非常全面，
它包含了：

* [ML403 开发板](http://www.xilinx.com/products/boards/ml403/docs.htm)（如果您想使用其他开发板，我们也提供了相关[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) )。
* 所有需要的硬件开发工具。
* 所有需要的软件开发工具（EDK 和 ISE）。
* JTAG 接口。
* 所有需要的线缆。

注意：请单独检查每个开发工具的许可条件，有些是开源工具，
有些仅用于评估，有些每年授予一次许可。

Microblaze 移植的初衷是让其尽可能通用以及得到广泛应用。因此，尽管
ML403 是一个全面的开发平台（涵盖以太网、USB、音频等），但 FreeRTOS 内核
还是要尽可能少地依赖核心 FPGA 组件之外的硬件。该移植随附的演示应用程序已配置为完全从
BRAM 执行，只使用基本的 UART 组件。

**注意：**Xilinx 一直同时服务于 Microblaze 核心和它们自己的工具链，因为本页所展示的移植最初就已经创建好了。Tyrel Newton 为此提供了大力支持，
它将该移植更新为采用Xilinx工具链 V14.4，并将[修改好的版本发布到了](http://interactive.freertos.org/entries/200807-up-to-date-gcc-microblaze-port)
本网站的 FreeRTOS 互动版块。非常感谢 Tyrel！

如下载所示，此演示应用程序未展示协程的使用情况。请参阅[协同程序文档](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/14-Standard-demo-examples)页面，
详细了解如何将协程功能快速添加到此演示。

---

### 重要提示！[Microblaze 软处理器核心](http://www.xilinx.com/products/design_resources/proc_central/microblaze.htm) RTOS移植使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
了解下载文件的描述和有关创建新项目的信息。

用于 Microblaze FreeRTOS 移植的 Platform Studio/GCC 演示应用程序项目命名为 system.xmp，
可位于 FreeRTOS/Demo/Microblaze 目录中。

FreeRTOS/Demo/Microblaze/Serial 目录中包含一个针对基本 UART 外围设备的中断驱动的串行端口驱动程序示例
。

---

### 演示应用程序

FreeRTOS 源代码下载文件包括 Microblaze GCC RTOS 移植的完全抢占式多任务演示应用程序。

演示应用程序创建了 23 个标准演示应用程序任务，一个“检查”任务，两个特定于 Microblaze
的测试任务和空闲任务，总共 27 个任务。
本网站的[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分提供了
关于标准演示任务功能的更多信息。

### 演示应用程序硬件设置

所有 ML403 跳线都可以保持在默认位置。

演示应用程序包括 ComTest 任务，其中一个任务会向另一个任务传输 RS232 字符。要正确执行此实时任务，
必须将环回连接器安装到 ML403 原型板的 RS232 端口
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。

### 功能

如果演示应用程序正确执行，其表现如下：
* LED 1、2 和 3 由 'flash' 任务控制。每盏灯将以恒定频率闪烁，LED 1
 速度最慢， LED 3 速度最快。
* 串行端口上每传输一个字符， SW4 上方的 LED 都会闪烁。
* 每当在串行端口上接收和验证字符时，SW5 上方的 LED 都会闪烁。
* 并非所有任务都会改变 LED，所以没有可见的指示来表明它们运行正常。
 因此，系统创建了一个检查任务，用于确保所有其他任务中没有检测到任何错误。

 LED 0 由“检查”任务控制。检查任务每 3 秒就会将系统中的所有任务检查一次，
 以确保任务执行无误。然后切换 LED 0。如果 LED 0 每三秒钟切换一次，
 那么就说明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一处错误。可以通过将环回连接器从串行端口（如上述）上移除来检查此机制，
 因为这样做是在故意制造一个错误。

### 构建和执行演示应用程序

由于 Microblaze 是软处理器内核，进行初始构建时会生成 FPGA 和软件映像。**这可能是
一个漫长的过程！**如果不改变硬件配置，那么初始构建之后的
编译和下载周期可以在几秒钟内完成。

Xilinx Platform Studio 项目了解构建的每个组件之间的依赖关系。如果您尝试下载
位流，它会首先检查该位流的所有组件是否为最新版本，如果不是，则确保它们是按照正确的顺序构建
。因此，执行完整构建的最简单的方法是点击
Platform Studio IDE 中的 "Download" 加速按钮：

1. 使用 JTAG 适配器将 ML403 开发板连接到主机。如果使用并行端口版本，
 请确保将并行连接器和 PS/2 连接器连接到主机。
2. 为 ML403 上电。
3. 在 Platform Studio IDE 中打开 Demo/Microblaze/system.xmp 文件。
4. 单击 "Download" 加速按钮![](/media/2018/downloadsb.gif)。
5. 如果这是初次构建，那么您可以走开去做一会儿别的事，因为构建需要一些时间。

构建和下载环节完成后，演示应用程序会自动开始执行。

该项目是从 BRAM 执行的，因此如果断电，项目会丢失。

### 使用调试器

对 FPGA 编程完成后，可以使用 Insight 调试器来修改和执行软件构建：

1. 按照上述步骤 1 至步骤 4 ，准备好开发环境。
2. 单击 "XMD" 加速按钮 ![](/media/2018/xmdsb.gif)，启动 XMD 接口。
 这一步对于主机调试器与开发板的通信是必要的。
3. 使用 "Build All User Applications" 加速按钮 ![](/media/2018/buildsb.gif)构建软件源文件。
4. 使用 "Software Debugger" 加速按钮 ![](/media/2018/debuggersb.gif)启动 Insight 调试器。
5. 在 Insight IDE 中，从 "File" 菜单中选择 "Target Settings"，并确保配置
 与下图一致：![](/media/2018/xmdtarget.gif)
Insight 目标设置
6. 再次在 Insight IDE 中选择 "Run" 加速按钮![](/media/2018/runsb.gif)。
7. Insight 将连接到目标，下载可执行文件，然后执行到 main() 的开始处并中断。之后，
 Insight 就可用于常规的查看代码和检查系统资源。

---

### 配置和用法详情

### 硬件组件

为了满足最低限度的要求，构建配置仅包括下述项：
* 基本 Microblaze 配置，没有缓存或浮点支持，没有外部内存接口。
* 调试模块。
* 演示应用程序所需的 LED 输出。
* 基本 UART（用于测试中断机制）。
* 单个中断控制器。
* 用于生成 RTOS 滴答的定时器。
* 必要的总线接口。

### GCC 项目的注意事项

1. 可能需要手动更新 Demo/MicroBlaze/System_incl.make 中的定义 XILINX_EDK_DIR，以确保它包含
 xilinx/EDK 目录的正确路径。
2. 我发现，如果项目位于包含空格 (' ') 的目录路径中，则将无法构建工具。

### RTOS 移植特定配置

此移植的特定配置项目位于Source/Demo/MicroBlaze/FreeRTOSConfig.h。可以编辑
此文件中定义的常量，确保适配您的应用程序。特别是：
用于设置 RTOS tick 频率的 configTICK_RATE_HZ 定义。提供的数值 1000 Hz 可用于
测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值将有助于提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

启动 RTOS 调度器时，FreeRTOS 内核会安装自己的中断处理程序。它使用与外设库相同的数据结构体
和间接机制，不需要做特殊考虑。

不会引起上下文切换的中断服务程序没有特殊要求，可以按正常函数
编写。

通常，上下文切换需要中断服务程序。例如，正在被接收的串行端口字符
可能会唤醒在等待该字符时被阻塞的高优先级任务。如果 ISR 中断了一个优先级较低的任务，
则其应立即返回到已被唤醒的任务。在中断函数的末尾调用宏 portYIELD_FROM_ISR() 可以确保，
可运行的最高优先级任务即为离开中断函数后
立即需要执行的任务。请参阅 Demo/MicroBlaze/serial/serial.c 中的 vSerialISR() 函数，
了解如何将 portYIELD_FROM_ISR() 与 xQueueSendFromISR() 和 xQueueReceiveFromISR() 结合使用。

### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/MicroBlaze/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式；
设置为 0，则可使用协同式。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 Microblaze 演示应用程序的 makefile 中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。
**注意：**一旦生成硬件映像，基本 UART 使用的波特率将被固定。传递给
串行端口初始化例程的波特率参数无影响。正如下载的一样，波特率设置为 9600。
