---
title: "Xilinx Virtex5 FPGA 上的 PowerPC PPC440 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/ML505.jpg)

PPC440 移植使用[PowerPC & MicroBlaze Virtex-5 嵌入式开发套件](http://www.xilinx.com/products/devkits/DK-V5-EMBD-ML507-G.htm)开发。该套件功能非常全面，
它包含了：

* ML507开发板（如果您希望使用替代开发板，我们也提供了相关[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) )。
* 所有需要的硬件开发工具。
* 所有需要的软件开发工具（EDK 和 ISE）。
* USB JTAG 接口。
* 所有需要的线缆。

---

### 重要提示！使用 Virtex5 PowerPC RTOS 移植的注意事项

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
下载文件的描述和有关创建新项目的信息。

提供了三个 Platform Studio 项目配置，名称均为 system.xmp：

1. 一个不使用浮点运算单元的项目，位于FreeRTOS/Demo/PPC440_Xilinx_Virtex5_GCC 目录。
2. 一个使用单精度浮点运算单元的项目，位于 FreeRTOS/Demo/PPC440_SP_FPU_Xilinx_Virtex5_GCC
 目录。
3. 一个使用双精度浮点运算单元的项目，位于 FreeRTOS/Demo/PPC440_DP_FPU_Xilinx_Virtex5_GCC
 目录。

---

### 演示应用程序

每个演示应用程序创建至少 40 个静态实时任务，然后持续创建和删除另外两个。其中的大多数任务
都来自一组标准演示任务，并非只适用于 PPC440/Virtex5 应用程序。它们的存在纯粹是为了测试
移植，并提供每个 FreeRTOS API 函数使用方法的示例。
本网站的[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分提供了
有关标准演示任务的信息。

除了标准演示任务外，还创建了以下演示特定任务：

* 检查 (Check) 任务。

 此操作每 3 秒执行一次，但具有最高的优先级以确保其拥有处理器时间。此任务主要用于
 检查其他所有任务是否仍可使用。

 大多数任务都会保持一个唯一的计数，每次任务成功完成其函数时，这个计数都会增加。如果
 任务中出现错误，计数将永久停止。检查任务检查每个任务的计数，以确保
 自上次执行检查任务以来，计数已变更。如果所有计数变量都已变更，则所有任务都在正确执行，
 没有错误。检查任务然后切换 LED 3。如果未检测到错误， LED 将每 3 秒
 切换一次。如果任何任务停止响应或报错，则切换频率将增加到每 500 毫秒一次。
* 寄存器 (Register Check) 检查任务。

 这些任务对端口进行测试，通过用已知值填充 CPU 寄存器，然后检查每个寄存器
 是否仍包含预期的值。若在任何寄存器中发现了意外值，则表示 RTOS 上下文切换实现中出现了错误。
 这些任务的优先级非常低，以确保它们定期被其他任务抢占。
* 可选浮点任务。

 包含浮点运算单元的项目会创建任务，这些任务也会检查浮点寄存器是否正确
 保存和还原。此操作得以实现是因为包含了一组
 浮点“寄存器检查”任务和执行浮点运算操作的任务。

### 演示应用程序硬件设置

演示应用程序包括 ComTest 任务，其中一个任务会向另一个任务传输 RS232 字符。为使该任务正确运行，
必须将一个环回连接器连接到 ML507 上标记为 COM1 的连接器上
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

演示应用程序使用开发板上内置的 LED，因此不需要其他硬件设置。

### 功能

演示应用程序正确执行时有以下表现：
* LED 0、1 和 2 由 'flash' 任务控制。每个 LED 将以恒定频率闪烁，LED 2 的频率最高，
 LED 0 的频率最低。
* LED 3 由 'Check' 检查任务控制，正常情况下应每 3 秒切换一次。如果此 LED 的切换频率提高到每 500 毫秒一次，则表明至少
 一个错误被发现和锁存（可以通过移除 COM1 上的环回连接器来测试此机制，
 因为这样做是在故意制造一个错误）。

### 生成和下载位流

Xilinx Platform Studio 项目了解构建的每个组件之间的依赖关系。如果您尝试下载
位流，它会首先检查该位流的所有组件是否为最新版本，如果不是，则确保它们是按照正确的顺序
构建的。因此，要执行完整构建，最简单的方法是从 Platform Studio 的 "Device Configuration" 菜单中
选择 "Download Bitstream"。
1. 使用 USB JTAG 适配器将 ML507 开发板连接到主机。
2. 为 ML507 上电。
3. 从 Platform Studio IDE 中打开相关的 system.xmp 文件。
4. 从 Platform Studios 的 "Device Configuration" 菜单中选择 "Download Bitstream"。初始构建可能需要很长时间才能完成，耗时取决于
 主机 PC 和创建的配置。一旦初始构建完成，位流将被下载到 ML507。

该软件项目是从 RAM 执行的，因此如果断电，项目将丢失。

### 构建演示应用程序

要构建演示应用程序和所有依赖库，可以从 Platform Studio 的 "Software" 菜单中
选择 "Build All User Applications"。应用程序应能成功构建，不出现任何错误或警告。

### 使用调试器

对 FPGA 编程完成后，可以使用 Insight 调试器来修改和执行软件构建：

1. 要打开 XMD 界面，从 Platform Studio 的 "Debug" 菜单中选择 "Launch XMD"。
 这一步对于主机调试器与开发板的通信是必要的。
2. 在 XMD 控制台窗口中
 键入“dow RTOSDemo/executable.elf”以下载 ELF 文件，然后键入“con”（表示“继续”），开始执行应用程序。
3. 要打开 Insight 调试器，从 Platform Studio 的 "Debug" 菜单中选择 "Launch Software Debugger"。
4. 在 Insight IDE 中，从 "Run" 菜单中选择 "Connect to Target"。首次尝试连接时将显示一个对话框，
 - 确保对话框中显示的配置
 与下图一致：![](/media/2018/xmdtarget.gif)
Insight 目标板设置
5. Insight 将连接到目标板。之后，
 Insight 就可用于常规的查看代码和检查系统资源。

---

### 配置和使用详情

### 初始化中断控制器

安装任何中断服务程序之前，必须先调用 vPortSetupInterruptController()
或 vTaskStartScheduler()。演示应用程序调用 vPortSetupInterruptController() 
作为main () 重点第一行。vPortSetupInterruptController() 的原型如下：

```c
void vPortSetupInterruptController( void );
```

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

以下是相关设置：

* 将 FreeRTOSConfig.h中的 configUSE_FPU 设置为 1。如果使用双精度浮点元算单元，则还必须对 USE_DP_FPU 进行定义
 （下载中所包含的双精度示例使用命令行选项进行此操作）。
* 将 FreeRTOSConfig.h中的 configUSE_APPLICATION_TASK_TAG 设置为 1。
* FreeRTOSConfig.h 包含一行 #include "FPU_Macros.h"。FPU_Macros.h 包含必须的 traceTASK_SWITCHED_IN() 和
 traceTASK_SWITCHED_OUT() 定义。包含文件排序至关重要——从 FreeRTOSConfig.h中包含 FPU_Macros.h 可确保
 顺序正确。
* 将 APU FPU 并入 FPGA 设计时，会自动设置编译器选项，使其正确用于硬件
 而非仿真浮点运算，"-mfpu=sp_full" 是必选项。

### 指定任务使用浮点运算

要熟悉浮点运算要求，最好的方法是查看
位于FreeRTOSRTOS/Demo/PPC440_DP_FPU_Xilinx_Virtex5_GCC/RTOSDemo/flop/flop.c和 FreeRTOS/Demo/PPC440_DP_FPU_Xilinx_Virtex5_GCC/RTOSDemo/flop/flop-reg-test.c 中的示例
（以及它们的对应的单精度示例）。
本节对代码做了简要说明。

与每个任务相关联的是标签值。这不是 RTOS 内核本身使用的，因此可以被移植层
或应用程序用于它希望的任何目的。此页面所描述的移植使用标签值来表示任务
是否需要浮点上下文。定义 traceTASK_SWITCHED_OUT() 和 traceTASK_SWITCHED_IN() 宏分别执行
实际浮点上下文的保存和还原。

标签值必须为 NULL 或指向一个足以容纳浮点上下文的缓冲区。任务创建时的默认值是 NULL，
表示任务不需要浮点上下文。

函数：

void vTaskSetApplicationTaskTag( TaskHandle_t xTask, TaskHookFunction_t pxTagValue );

用于将 pxTagValue 的一个标签值与一个句柄等于 xTask 的任务相关联。
常量 portNO_FLOP_REGISTERS_TO_SAVE 表示浮点上下文的 32 位寄存器构成数量。
作为示例，可使用以下方式分配一个足够大的缓冲区用于保存单精度浮点上下文：

float fFlopContext[ portNO\\_FLOP\\_REGISTERS\\_TO\\_SAVE ];

将浮点改为双精度后将分配足够的空间来保存双精度浮点上下文。
要将此缓冲区分配给任务的标签值，可以调用：

vTaskSetApplicationTaskTag( xTask, ( void * ) ulFlopContext );

请参阅所提供的示例。

### RTOS 移植特定配置

此移植的特定配置项目位于 FreeRTOSConfig.h。提供的三个 PPC440 演示都有自己的 FreeRTOSConfig.h 文件，
位于各自的项目目录中。可以根据您的应用程序的需求，
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
