---
title: "适用于Luminary Micros Stellaris 微控制器的 Cortex-M3/CrossStudio 移植"
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
| <br />![lm3s102.gif](/media/2018/lm3s102.gif)<br /> |

目前有四种FreeRTOS移植适用于基于[Luminary Micro](http://www.luminarymicro.com/)Stellaris Cortex 的嵌入式微控制器。一是使用 [Sourcery G + + (GCC)工具](http://www.codesourcery.com/)是移植,
二是使用 [ARM Keil 工具](portcortexkeil)的移植，三是使用 [IAR工具](http://www.iar.com/)的移植，四是本页面上所示的使用
[Rowley CrossWorks](http://www.rowley.co.uk/)的移植。

此处为 CrossWorks 移植提供了三个演示应用程序，两个针对由 Luminary Micro 供应的 DK-LMS102 开发板，
另一个针对由 Rowley Associates 供应的低成本[CrossFire LM3S102 板](http://www.rowley.co.uk/crossfire/crossfire_lm3s102.htm)。CrossFire LM3S102
通过内置的 USB 连接器直接连接到主机，不需要使用独立的 JTAG 接口。

[! [](/media/2018/lm3s102_crossfire.gif)] (http://www.rowley.co.uk/crossfire/crossfire_lm3s102.htm)
CrossFire LM3S102 开发板

Stellaris 是一个新的微控制器系列，也是首款市售带有 Cortex-M3 内核的微控制器。LM3S102 是一款低成本、低引脚数的设备。它的
芯片上有 2K 字节的 RAM 和 8K 字节的 ROM。它是演示 FreeRTOS V4.0.0 中包含的新协程功能的理想设备。

CrossWorks Cortex-M3 演示依赖于需从 FreeRTOS单独授权的驱动程序库和 makefile。许可条款包含在库头文件顶部的注释中，
该头文件位于 Demo/CORTEX_LM3S102_ROWLEY/hw_include 目录下。该许可的完整副本在同一目录中。

**升级到 FreeRTOS V5.0.3 :** FreeRTOS V5.0.3 为 Cortex-M3 移植引入 configMAX_SYSCALL_INTERRUPT_PRIORITY 配置选项。请参阅
[RTOS内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档以获取有关此功能的完整信息。

**升级到 FreeRTOS V4.8.0：**  在 V4.8.0 之前，FreeRTOS 内核未使用 SVCall 中断，从 V4.8.0 开始才使用 SVCall 中断。
因此，要将旧项目升级到 V4.8.0 标准，需要稍微编辑一下启动代码。要执行此操作，只需
将 vPortSVCHandler () 安装到中断向量表（包含在启动源文件中）内的 SVCall 位置。包含在
FreeRTOS 下载中的演示项目已更新，可以作为示例。

---

### 重要提示！ARM Cortex-M3 CrossWorks 移植的使用说明

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和用法详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
以了解下载文件的描述和有关创建新项目的信息。

Luminary Micro移植的 CrossWorks 解决方案（工作区）位于 FreeRTOS/Demo/CORTEX_LM3S102_Rowley 目录。

---

### 演示应用程序

FreeRTOS 源代码下载包含针对此移植的三个演示应用程序。这些演示里面还包括完全抢占式任务和协程。演示 1 创建 3 个任务（包括空闲任务）
和 6 个协程。演示 2 创建 2 个任务和 7 个协程。这两个演示都配置为在 DK-LMS102 开发板上执行。
演示 3 创建了 4 个协程和空闲任务，并配置为在 CrossFire LM3S102 板上执行。

由于 ROM 和 RAM 限制，没有使用标准演示任务。

---

### 演示应用程序硬件设置，演示 1 和演示 2

LINK_RST 跳线必须布设在 DK-LMS102 目标板上的相应位置，所有其他跳线可以保持在默认位置。

此演示应用程序包括一个中断驱动的 UART 测试，其中一个协程传输字符，一个任务接收这些字符。为了使该功能正确运行，
必须将环回连接器安装到 DK-LMS102 原型板的 SER0 连接器上
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。

使用[CrossConnect JTAG 接口](http://www.rowley.co.uk/arm/CrossConnect.htm)连接主机 PC 与目标板。

### 功能，演示 1 和演示 2

如果演示 1 应用程序正确执行，其表现如下：
* 标记为 LED0 至 LED4 的 LED 由 "flash" 协程控制。每个 LED 将以恒定频率闪烁，LED0 的频率最高，
 速度最快，LED4 速度最慢。
* 串行端口上每传输一个字符， LED5 都会闪烁。
* 每当在串行端口上通过环回连接器接收和验证字符时，LED6 都会闪烁。
* LED7 用于指示检测到错误，因此应保持关闭状态。
* LCD 将滚动显示消息，指示正在执行的演示。

演示包含检查所有任务和协程是否按预期执行的功能。如果在任何任务或协程中发现错误
LED7 会点亮。可以在演示执行过程中移除环回连接器来测试此功能。

演示 2 应用程序具有类似的功能，但测试的是 RTOS 移植的其他功能。

---

### 演示应用程序硬件设置，演示 3

CrossFire LM3S102 板不需要任何特殊设置。它通过内置的 USB 连接直接连接到主机，不需要使用
外部 JTAG 接口。

### 功能，演示 3

演示 3 应用程序正确执行时，其将循环闪烁三个彩色 LED，闪烁速率由电位器设置。

---

### 构建和执行演示应用程序

CrossWorks 解决方案 FreeRTOS/Demo/CORTEX_LM3S102_Rowley/RTOSDemo.hzp 中包含三个演示项目和两项配置。必须为调试会话选择 "Flash Debug"
配置。必须选择 "Flash Release" 配置，以便单独运行此演示，而不用通过调试器运行。

![](/media/2018/selectconfig.gif)
选择构建配置

要构建应用程序：

1. 从 IDE 的下拉列表中选择您希望构建的项目![](/media/2018/selectproject.gif)
选择待构建项目
2. 在 "Build" 菜单中选择 "Rebuild Demox"。构建项目时不应报错或出现警告。

如需下载并执行此演示：
1. 如果使用 CrossFire LM3S102，可直接将主机连接到目标板；如果使用 Luminary Micro
 开发板，可以使用 CrossConnect JTAG 接口。
2. 从 "Target" 菜单中为您的设置选择适合的连接。![](/media/2018/connectjtag.gif)
选择目标
3. 从 "Debug" 菜单中选择 "Start Debugging"。LM3S10x 闪存需要进行编程，调试器将停在 main() 的开始处。

---

### 配置和用法详情

### RTOS 移植特定配置

这些演示的特定配置项目位于相应 FreeRTOS/Demo/CORTEX_LM3S102_ROWLEY/Demox/FreeRTOSConfig.h 文件中。根据
您的应用需求编辑此文件中定义的常量。特别是：
用于设置 RTOS tick 频率的 configTICK_RATE_HZ 定义。提供的数值 1000 Hz 可用于
测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。

另请注意 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY。

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。

注意：请记住 Cortex-M3 核心使用低数值数字表示高
优先级中断，这似乎有悖直觉，而且很容易忘记！如果希望为中断分配低优先级，请勿将中断的
优先级指定为 0（或其他较小数值），因为这可能会导致中断实际上在系统中具有最高优先级，因此，如果该优先级高于
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，可能会导致系统崩溃。

Cortex-M3 核心的最低优先级实际上是 255，然而不同的 Cortex-M3 供应商采用了不同数量的优先级位，
并提供优先级指定方式不同的库函数。请使用提供的示例作为参考。

每个移植 #defines 'BaseType_t' 等于该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

中断向量表包含在 FreeRTOS/Demo/CORTEX_LM3S102_Rowley/demox/vectors.s中，可以根据需要填充。在演示应用程序中
向量表保持在闪存中。

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档进行编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。main.c 中定义的 UART ISR 演示了这种机制
（请参阅 vUART_ISR() 函数）。请注意，portEND_SWITCHING_ISR() 将启用中断。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_LM3S102_ROWLEY/Demox/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式，
设置为 0，则可使用协同式。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_1.c 包含在 ARM Cortex-M3 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。
