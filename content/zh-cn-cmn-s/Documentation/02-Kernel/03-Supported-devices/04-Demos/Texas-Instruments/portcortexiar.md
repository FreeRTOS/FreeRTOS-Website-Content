---
title: "适用于 Luminary Micro Stellaris 微控制器的 Cortex-M3/IAR 移植"
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
| <br />![lm3s316.gif](/media/2018/lm3s316.gif)<br /> |

该移植使用 [DK-LM3S316](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) 开发套件开发。

[LM3S316](https://www.ti.com/lit/ml/spmu145/spmu145.pdf?ts=1719575549427)
是一款低成本、低引脚数的设备。它的
芯片上有 4K 字节的 RAM 和 16K 字节的 ROM。我们故意限制了演示
应用程序的代码大小，以确保使用 IAR 工具中代码大小受限的 KickStart 版本构建此演示应用。

IAR ARM Cortex-M3 演示依赖于一份需从 FreeRTOS.org 单独授权的驱动程序库文件。适用于此库的许可的完整副本
包含在 EULA.txt 文件中，该文件位于 FreeRTOS 下载中的 Demo/CORTEX_LM3S316_IAR/hw_include 目录下。

目前有四种 FreeRTOS 移植适用于基于 [Luminary Micro](http://www.luminarymicro.com/) Stellaris ARM Cortex-M3 的微控制器。
 一是使用 [Sourcery G++ (GCC) 工具](http://www.codesourcery.com/)的移植，二是使用
 [ARM Keil 工具](portcortexkeil)的移植，三是针对 [Rowley CrossWorks](http://www.rowley.co.uk/) 的移植，
 四是本页面上展示的使用 [IAR Embedded Workbench](http://www.iar.com/) 工具链的移植。

**注意：**如果此项目未能使用 IAR 工具生成，则可能是 IAR
Embedded Workbench 版本过低造成的。如果构建失败，
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。

---

### 重要提示！使用 ARM Cortex-M3 移植的注意事项IAR

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和用法详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
下载文件的描述和有关创建新项目的信息。

Luminary Micro 移植的 IAR 工作区位于 FreeRTOS/Demo/CORTEX_LM3S316_IAR 目录中，称为 RTOSDemo.eww。

---

### 演示应用程序

FreeRTOS 源代码下载包含针对 IAR 移植的预配置演示应用程序。该应用演示了完全抢占式任务和协程——创建了 8
个协程和 5 个任务（包括空闲任务）。

### 演示应用程序硬件设置

大多数 DK-LM3S316 跳线可以保持在默认位置。为保证 ADC 能够正确读取光传感器，请确保跳线 0
也处于 ADC 连接器 JP2 上的相应位置。

此演示应用程序包括一个中断驱动的 UART 测试，其中一个协程传输字符，一个任务接收这些字符。为了使该功能正确运行，
必须将环回连接器安装到 DK-LM3S316 目标板的 SER0 连接器上
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。

使用 J-Link JTAG 接口连接主机 PC 与目标端。

### 功能

有关演示功能的详细说明，请参阅 Demo/CORTEX_LM3S316_IAR/main.c 顶部的注释。

如果演示应用程序正确执行，其表现如下：

* LCD 的顶行将滚动显示 'LCD 消息' 演示任务发来的消息。
* LCD 的底行将显示 ADC 0 值，该值可传输到上文“硬件设置”部分所述的 DK-LM3S316 光传感器。这
 源于 'ADC' 演示协程。
* 标记为 LED0 至 LED4 的 LED 由 "flash" 协程控制。每个 LED 将以恒定频率闪烁，LED0 的频率最高，
 速度最快，LED4 速度最慢。
* 串行端口上每传输一个字符， LED5 都会闪烁。
* 每当在串行端口上通过环回连接器接收和验证字符时，LED6 都会闪烁。
* LED7 用于指示检测到错误，因此应保持关闭状态。

演示包含检查所有任务和协程是否正常执行的功能。如果在任何协程或任务中发现错误，
则点亮 LED7。可以在演示执行过程中移除环回连接器来测试此功能，并为此专门生成
一个错误。

### 构建和执行演示应用程序

要构建应用程序，只需在 Embedded Workbench IDE 中打开 RTOSDemo.eww，然后从 "Project" 菜单中选择 "Rebuild all"。

如需下载并执行此演示，请进行以下步骤：

1. 使用 J-Link J-TAG 接口将主机连接到目标板。
2. 单击 "Debug" 速度按钮，或只需按下 CTRL D。
3. LM3S31x 闪存需要进行编程，调试器将停在 main() 的开始处。

---

### 配置和用法详情

### RTOS 移植特定配置

这些演示的特定配置项目位于 FreeRTOS/Demo/CORTEX_LM3S316_IAR/FreeRTOSConfig.h。可以编辑
在本文件中定义的常量，以适配您的应用程序。特别是-

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS tick 的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。

注意：请记住 ARM Cortex-M3 核心使用低数值数字表示高
优先级中断，这似乎有悖直觉，而且很容易忘记！如果您希望将中断分配为低优先级，请不要将中断的
优先级指定为 0（或其他较小数值），因为这可能会导致中断实际上在系统中具有最高优先级 - 因此，如果该优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能会导致系统崩溃。

ARM Cortex-M3 核心的最低优先级实际上是 255，然而，不同的 ARM Cortex-M3 供应商采用了不同数量的优先位，
并提供了优先级指定方式不同的库函数。请使用提供的示例作为参考。

每个移植 #defines 'BaseType_t' 等于该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

包含在 FreeRTOS/Demo/CORTEX_LM3S316_IAR/hw_include/startup.c 中，可以根据需要填充。
在演示应用程序中，向量表保存在闪存。

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。commtest.c 中定义的被称为 vUART_ISR() 的 UART ISR
演示了这种机制。

请注意，portEND_SWITCHING_ISR() 将启用中断。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_LM3S316_IAR/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式调度；
设置为 0，可使用协同式调度。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

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

