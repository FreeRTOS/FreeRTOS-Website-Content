---
title: "Cortex-M3/GCC 移植，适用于Luminary Micros Stellaris 微控制器"
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

 目前有四种 FreeRTOS移植适用于基于[Luminary Micro](http://www.luminarymicro.com/)Stellaris Cortex 的嵌入式微控制器，一种使用
 [Sourcery G + + (GCC) 工具](http://www.codesourcery.com/)，一个适用于[Rowley CrossWorks](http://www.rowley.co.uk/)，
 另一种适用于[IAR工具](http://www.iar.com/)，还有一种使用
 [ARM Keil 工具](portcortexkeil)。
 本页内容仅与基于 GCC 的移植相关。它非常类似于与 ARM Keil 移植相关的页面，直至有关生成说明的
 章节。

 LM3S102 是一款低成本、低引脚数的设备。它的
 芯片上有 2K 字节的 RAM 和 8K 字节的 ROM。自 FreeRTOS V4.0.0 包含协程功能以来，它是演示该功能的理想设备。

Cortex GCC 演示依赖于需从 FreeRTOS单独授权的驱动程序库和 makefile。许可条款包含在库头文件顶部的注释中，
该头文件位于 Demo/CORTEX_LM3S102_GCC/hw_include 目录下。

根据 Keil 移植，GCC 移植是使用 DK-LMS102 开发板开发的。

**升级到 FreeRTOS V5.0.3：**FreeRTOS V5.0.3 为 ARM Cortex-M3 移植引入了 configMAX_SYSCALL_interrupt_PRIORITY 配置选项。请参阅
[RTOS内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档以获取有关此功能的完整信息。

**升级到 FreeRTOS V4.8.0：**  在 V4.8.0 之前，FreeRTOS 内核未使用 SVCall 中断，从 V4.8.0 开始才使用 SVCall 中断。
因此，要将旧项目升级到 V4.8.0 标准，需要稍微编辑一下启动代码。要执行此操作，只需
将 vPortSVCHandler () 安装到中断向量表（包含在启动源文件中）内的 SVCall 位置。包含在
FreeRTOS 下载中的演示项目已更新，可以作为示例。

|  |  |
| --- | --- |
|  |  |

---

### 重要提示！使用 ARM Cortex-M3 GCC 移植的注意事项

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，
下载文件的描述和有关创建新项目的信息。

Luminary Micro移植的 GCC makefile 可以在FreeRTOS/Demo/CORTEX_LM3S102_GCC 目录中找到。

---

### 演示应用程序

FreeRTOS 源代码下载文件包含两个此移植的演示，其中包括完全抢占式任务和协程。演示 1 创建 3 个任务（包括空闲任务）
和 6 个协程。演示 2 创建 2 个任务和 7 个协程。由于 ROM 和 RAM 限制，没有使用标准演示任务。

### 演示应用程序硬件设置

DK-LMS102 的所有跳线都可以保持在默认位置。

此演示应用程序包括一个中断驱动的 UART 测试，其中一个协程传输字符，一个任务接收这些字符。对于此功能的正确操作，
必须将环回连接器安装到 DK-LMS102 原型板的 SER0 连接器上
（9 路连接器上的引脚 2 和 3 必须连接在一起）。

必须连接 USB 启用跳线才能使用直接 USB 调试设施。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。

### 功能

如果演示 1 应用程序正确执行，其表现如下：
* 标记为 LED0 至 LED4 的 LED 由 "flash" 协程控制。每个 LED 将以恒定频率闪烁，LED0 的频率最高，
 速度最快，LED4 速度最慢。
* 串行端口上每传输一个字符， LED5 都会闪烁。
* 每当在串行端口上通过环回连接器接收和验证字符时，LED6 都会闪烁。
* LED7 用于指示检测到错误，因此应保持关闭状态。
* LCD 将滚动显示消息，指示正在执行的演示。

演示包含检查所有任务和协程是否按预期执行的功能。如果在任何任务或协程中发现错误
LED7 会点亮。可以在演示执行过程中移除环回连接器来测试此功能。

演示 2 应用程序具有类似的功能，但测试的是 RTOS 移植的其他功能。要切换到演示 2，只需拷贝
FreeRTOS/DEMO/CORTEX_LM3S102_GCC/Demo2 中的文件到FreeRTOS/DEMO/CORTEX_LM3S102_GCC 目录。

### 构建和执行演示应用程序

这些说明假设已安装了 GCC 编译器和相关工具（make.exe 等），并且它们的位置已包含在环境变量
路径中。

要构建应用程序：

1. 使用命令提示符，导航到FreeRTOS/Demo/CORTEX_LM3S102_GCC 目录。
2. 键入“make” 以使用现有的 makefile 和 linker 脚本构建应用程序。该应用程序
 应该成功构建，不会报错或出现警告，如下所示：

```c

$ make
  CC    init/startup.c
  CC    main.c
  CC    hw_include/pdc.c
  CC    ../../Source/list.c
  CC    ../../Source/queue.c
  CC    ../../Source/tasks.c
  CC    ../../Source/portable/GCC/ARM_CM3/port.c
  CC    ../../Source/portable/MemMang/heap_1.c
  CC    ParTest/ParTest.c
  CC    ../Common/Minimal/crflash.c
  CC    ../../Source/croutine.c
  LD    gcc/RTOSDemo.axf
```
构建文件被放置到名为 GCC 的子目录中。

DK-LMS102 评估板包含一个 USB 接口，允许将应用程序直接下载到目标闪存。更多详细信息请参阅 Sourcery G++ 手册
。要调试应用程序：
1. 通过命令提示符导航到FreeRTOS/Demo/CORTEX_LM3S102_GCC/GCC 目录。
2. 通过键入“arm-stellaris-eabi-gdb RTOSDemo.axf”启动调试器
3. 通过键入"(gdb) target extended-remote armswd -s 2 -f lmi.dll stdio"  | (其中" (gdb) "是命令提示符）连接到目标板。
4. 只需键入“(gdb) load”即可下载 RTOSDemo.axf 文件。应看到与下方所示类似的输出。
```c

Loading section .text, size 0x1fd4 lma 0x0
Loading section .data, size 0x10 lma 0x1fd4
Start address 0x61, load size 8164
Transfer rate: xxxxx bits/sec, xxx bytes/write.
```
5. 下载映像后，键入 “run” 以启动应用程序。GDB 询问您是否
要从头开始，请输入 “y” 以继续。然后，您将停留在
ResetISR，即应用程序的入口点。
```c

The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program:c:FreeRTOS/Demo/CORTEX_LM3S102_GCC/gcc/RTOSDemo.axf
Reloaded SP/PC from 0, reset xPSR and LR
Stopped at entry.
Program received SIGTRAP, Trace/breakpoint trap.
0x00000060 in ResetISR()
```
6. 现在可以通过键入 “continue” 来执行演示。

有关使用 GDB 的更多信息，请参阅 [GDB 用户手册](http://www.gnu.org/software/gdb/documentation/)。

---

### 配置和用法详情

### RTOS 移植特定配置

此移植的特定配置项目位于 FreeRTOS/Demo/CORTEX_LM3S102_GCC/FreeRTOSConfig.h。可编辑
此文件中定义的常量，确保适配您的应用程序。特别是：
用于设置 RTOS tick 频率的 configTICK_RATE_HZ 定义。提供的数值 1000 Hz 可用于
测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。

另请注意 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY。

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。

注意：请记住 ARM Cortex-M3 核心使用的数值越低，表示
中断优先级越高，这似乎有悖直觉，而且很容易忘记！如果希望为中断分配低优先级，请勿将中断的
优先级指定为 0（或其他较小数值），因为这可能会导致中断实际上在系统中具有最高优先级，因此，如果该优先级高于
configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能会导致系统崩溃。

ARM Cortex-M3 核心的最低优先级实际上是 255，然而，不同的 ARM Cortex-M3 供应商采用了不同数量的优先位，
并提供了优先级指定方式不同的库函数。请使用提供的示例作为参考。

每个移植 #defines 'BaseType_t' 等于该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

中断向量表包含在 FreeRTOS/Demo/CORTEX_LM3S102_GCC/init/startup.c 中，可以根据需要填充。在演示应用程序中，
向量表保持在闪存中。

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档进行编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。main.c 中定义的 UART ISR 演示了这种机制
（请参阅 vUART_ISR() 函数）。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_LM3S102_GCC/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式，
将其设置为 0，则可使用协作式内核。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

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
