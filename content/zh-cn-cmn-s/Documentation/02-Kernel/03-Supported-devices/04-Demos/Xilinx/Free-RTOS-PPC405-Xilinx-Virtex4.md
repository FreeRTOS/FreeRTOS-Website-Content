---
title: "XilinxVirtex-4 FPGA 上的 PowerPC (PPC405) 移植"
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

PPC405 移植使用[PowerPC & MicroBlaze Virtex-4 嵌入式开发套件](http://www.xilinx.com/products/devkits/DO-ML403-EDK-ISE-USB-UNI-G.htm)开发。该套件功能非常全面，
它包含了：

* [ML403 开发板](http://www.xilinx.com/products/boards/ml403/docs.htm)（如果您想使用其他开发板，我们也提供了相关[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) )。
* 所有需要的硬件开发工具。
* 所有需要的软件开发工具（EDK 和 ISE）。
* JTAG 接口。
* 所有需要的电缆。

FreeRTOS V5.0.2 提供了两个 PowerPC 项目，原始项目和包括可选浮点单元 (FPU) 的替代项目。
此页面的[配置和使用详情](#配置和用法详情)部分提供了有关使用 FPU 的更多信息。

---

### 重要提示！使用 Virtex4 PowerPC RTOS 移植的注意事项

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题: [我的应用程序未运行，哪里出错了?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅 [源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization) 章节，了解
下载文件的描述和有关创建新项目的信息。

不含 FPU 的 PowerPC 的 Platform Studio/GCC 演示应用程序项目命名为 system.xmp，
可以在 FreeRTOS/Demo/PPC405_Xilinx_Virtex4_GCC 目录下找到。使用 FPU 的替代演示
位于 FreeRTOS/Demo/PPC405_FPU_Xilinx_Virtex4_GCC 目录中。

目录FreeRTOS/Demo/PPC405_Xilinx_Virtex4_GCC/RTOSDemo/Serial 包含一个基本 UART 外围设备的中断驱动的串口驱动器样本
。

---

### 演示应用程序

FreeRTOS 源代码下载包含 Virtex4 PPC405 RTOS 移植的完全抢占式多任务演示应用程序。

演示应用程序会创建 40 个静态实时任务，然后动态创建和删除另外两个任务。其中的大多数
任务并非是 PPC405/Virtex4 应用程序特有的。除了标准演示任务外，还创建了以下演示特定任务：

* 检查 (Check) 任务。

 此操作每 3 秒执行一次，但具有最高的优先级以确保其拥有处理器时间。此任务主要用于
 检查其他所有任务是否仍可使用。

 大多数任务都会保持一个唯一的计数，每次任务成功完成其函数时，这个计数都会增加。如果
 任务中出现错误，计数将永久停止。检查任务检查每个任务的计数，以确保
 自上次执行检查任务以来，计数已变更。如果所有计数变量都已变更，则所有任务都在正确执行，
 没有错误。然后检查任务会切换 LED DS15。如果没有检测到错误，则切换周期
 将为 3 秒。如果有任何任务报告了错误，切换周期将为 500 毫秒。
* “寄存器检查”任务。

 这些任务用已知值填充 CPU 寄存器，然后检查每个寄存器是否仍包含预期值。此函数的
 发现意外值表明 RTOS 上下文切换机制中存在错误。寄存器检查任务以低优先级运行，
 因此经常被抢占。
* 可选浮点任务。

 含有 FPU 的替代项目会创建寄存器检查任务，用于测试浮点寄存器上下文切换，
 还会创建一组 8 个任务，用于测试和演示浮点操作的使用。

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
* LED DS6、DS5 和 DS4 由 'flash' 任务控制。每个 LED 将以恒定频率闪烁，LED DS6 的频率最高，
 LED DS4 的频率最低。
* 每当在串行端口上接收和验证字符时，SW4 上方的 LED 都会闪烁。每当字符在串行端口上传输时，SW5 上方的 LED
 都会闪烁（切换速率很快，不太容易看到）。
* LED DS15 受检查任务的控制。如果 LED DS15 每三秒切换一次，则表示从未检测到错误
 。如果切换速度增加到 500 毫秒，则表示“检查”任务至少发现了一个错误。可以
 通过从串行端口中移除环回连接器（如上所述）来测试此机制，
 此方式会故意生成错误。

### 生成和下载位流

Xilinx Platform Studio 项目了解构建的每个组件之间的依赖关系。如果您尝试下载
位流，它会首先检查该位流的所有组件是否为最新版本，如果不是，则确保它们是按照正确的顺序
。因此，要执行完整构建，最简单的方法是从 Platform Studios 的 "Device Configuration" 菜单中
选择 "Download Bitstream"。
1. 使用 JTAG 适配器将 ML403 开发板连接到主机。如果使用并行端口版本，
 请确保将并行连接器和 PS/2 连接器连接到主机。
2. 为 ML403 上电。
3. 在 Platform Studio IDE 中打开 Demo/ PPC405_Xilinx_Virtex4_GCC/system.xmp 文件。
4. 从 Platform Studios 的 "Device Configuration" 中选择 "Download Bitstream"。初始构建将需要 10
 到 30 分钟，具体取决于主机，完成后应下载到 ML403。

该项目是从 RAM 执行的，因此如果断电，项目将丢失。

### 构建演示应用程序

要构建演示应用程序，请在 Platform Studio 的 "Application" 窗口中右键单击该项目，
然后从生成的弹出菜单中选择 "Build Project"。

![](/media/2018/building-PowerPC-project.jpg)
使用弹出菜单构建 PowerPC 演示应用程序。

**注意**：文件 system_incl.make 包含 “XILINX_EDK_DIR = C:/devtools/XilinxEDK” 行。在构建
RTOS 演示应用程序之前，可能需要更新此文件以正确安装 Xilinx 工具。

### 使用调试器

对 FPGA 编程完成后，可以使用 Insight 调试器来修改和执行软件构建：

1. 按照上述步骤构建应用程序并准备开发环境。
2. 点击 XMD 加速按钮 ![](/media/2018/xmdsb.gif)，或从 Platform Studio 的 "Debug" 菜单中选择 "Launch XMD" 来启动 XMD 接口。
 这对于主机调试器与开发板的通信是必要的。
3. 使用 "Software Debugger" 加速按钮 ![](/media/2018/debuggersb.gif)，或从 Platform Studio 的 "Debug" 菜单中选择 "Launch Software Debugger" 来启动 Insight 调试器。
4. 在 Insight IDE 中，从 "File" 菜单中选择 "Target Settings"，并确保配置
 与下图一致：![](/media/2018/xmdtarget.gif)
Insight 目标设置
5. 再次在 Insight IDE 中选择 "Run" 加速按钮![](/media/2018/runsb.gif)。
6. Insight 将连接到目标，下载可执行文件，然后执行到 main() 的开始处并中断。之后，
 Insight 就可用于常规的查看代码和检查系统资源。

---

### 配置和用法详情

### GCC 项目的注意事项

1. 可能需要手动更新 Demo/MicroBlaze/System_incl.make 中的定义 XILINX_EDK_DIR，以确保它包含
 xilinx/EDK 目录的正确路径。
2. 我发现，如果项目位于包含空格 (' ') 的目录路径中，则将无法构建工具。

### 初始化中断控制器

安装任何中断服务程序之前，必须先调用 vPortSetupInterruptController()
或 vTaskStartScheduler()。演示应用程序调用 vPortSetupInterruptController() 
作为main () 重点第一行。vPortSetupInterruptController() 的原型如下：

```c
void vPortSetupInterruptController( void );
```

根据演示应用程序，假设正在使用一个中断控制器。

### 安装中断处理程序

应使用 xPortInstallInterruptHandler() 安装中断处理程序。源文件 serial.c 包含一个此函数的用法示例。
xPortInstallInterruptHandler() 的原型如下：

```c

BaseType_t xPortInstallInterruptHandler( unsigned char ucInterruptID,
                                            XInterruptHandler pxHandler,
                                            void *pvCallBackRef );
```

其中：
* ucInterruptID 是分配给 Xilinx 生成的名为 "xparameters.h" 的头文件中外设的 ID。
 例如，在 RTOS 演示应用程序中，给 UART 分配的 ID 是 XPAR_OPB_INTC_0_RS232_UART_INTERRUPT_INTR。
* pxHandler 是一个指向 C 中断处理程序函数的指针。
* pvCallBackRef 是一个指向参数的指针，此参数将被传递到 C 中断处理程序函数中。
 中断处理程序函数必须接受单个 void * 参数，即使未使用此参数。
 serial.c 中的函数 vSerialISR() 可以用作示例。

### 数学库

提供给 GCC 的（仿真浮点）数学库不是可重入的，且未经采取适当的互斥预防措施，不得使用。
因此，最好使用如下所述的浮点运算单元。

### 使用 APU 浮点运算单元对项目设置的要求

FreeRTOS/Demo/PPC405_FPU_Xilinx_Virtex4_GCC 目录下的示例项目是专为
用于浮点运算配置的。以下是相关设置：

* 将 FreeRTOSConfig.h中的 configUSE_FPU 设置为 1。
* 将 FreeRTOSConfig.h中的 configUSE_APPLICATION_TASK_TAG 设置为 1。
* FreeRTOSConfig.h 包含一行 #include "FPU_Macros.h"。FPU_Macros.h 包含必须的 traceTASK_SWITCHED_IN() 和
 traceTASK_SWITCHED_OUT() 定义。包含文件排序至关重要——从 FreeRTOSConfig.h 中包含 FPU_Macros.h 可确保
 顺序正确。
* 将 APU FPU 并入 FPGA 设计时，会自动设置编译器选项，使其正确用于硬件
 而非仿真浮点运算，"-mfpu=sp_full" 是必选项。

### 指定任务使用浮点运算

要熟悉浮点运算要求，最好的方法是查看
FreeRTOSRTOS/Demo/PPC405_FPU_Xilinx_Virtex4_GCC/RTOSDemo/flop/flop.c and FreeRTOS/Demo/PPC405_FPU_Xilinx_Virtex4_GCC/RTOSDemo/flop/flop-reg-test.c.
本节对代码做了简要说明。

与每个任务相关联的是标签值。这不是 RTOS 内核本身使用的，因此可以被移植层
或应用程序用于它希望的任何目的。此页面所描述的移植使用标签值来表示任务
是否需要浮点上下文。定义 traceTASK_SWITCHED_OUT() 和 traceTASK_SWITCHED_IN() 宏分别执行
实际上下文的保存和还原。

标签值必须为 NULL 或指向一个足以容纳浮点上下文的缓冲区。任务创建时的默认值是 NULL，
表示任务不需要浮点上下文。

函数：

void vTaskSetApplicationTaskTag( TaskHandle_t xTask, TaskHookFunction_t pxTagValue );

用于将 pxTagValue 的一个标签值与一个句柄等于 xTask 的任务相关联。
常量 portNO_FLOP_REGISTERS_TO_SAVE 表示浮点上下文的 32 位寄存器构成数量。
作为示例，可使用以下方式分配一个足够大的缓冲区用于保存浮点上下文：

unsigned long ulFlopContext[ portNO\\_FLOP\\_REGISTERS\\_TO\\_SAVE ];

要将此缓冲区分配给任务的标签值，可以调用：

vTaskSetApplicationTaskTag( xTask, ( void * ) ulFlopContext );

请参阅所提供的示例。

### RTOS 移植特定配置

此移植的特定配置项位于 Demo/PPC405_Xilinx_Virtex4_GCC/RTOSDemo/FreeRTOSConfig.h中。可编辑
此文件中定义的常量，确保适配您的应用程序。特别是：
用于设置 RTOS tick 频率的 configTICK_RATE_HZ 定义。提供的数值 1000 Hz 可用于
测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值将有助于提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 请求在 ISR 内进行上下文切换

可以从 ISR 内调用宏 portYIELD_FROM_ISR() 来请求在 ISR 终止之前选择一个新任务来运行。
通常是在 ISR 导致任务接触阻塞时进行此操作，并且解除阻塞的任务的优先级当前执行任务
的优先级高。

### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/MicroBlaze/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式；
设置为 0，则可使用协同式。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

PowerPC 演示应用程序项目中内置 Source/Portable/MemMang/heap_2.c
以提供 RTOS 内核所需的内存分配。
这个方案非常简单，它从一个大型数组中分配内存块。数组大小由 FreeRTOSConfig.h 中的常量 configTOTAL_HEAP_SIZE 设置。
请参阅 API 文档的 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 章节，
以获取完整信息。

### 串口驱动程序

还应注意，编写串行端口驱动器是为了演示和测试某些实时内核功能，它并非一个优化的解决方案。
**注意：**一旦生成硬件映像，基本 UART 使用的波特率将被固定。传递给
串行端口初始化例程的波特率参数无影响。
