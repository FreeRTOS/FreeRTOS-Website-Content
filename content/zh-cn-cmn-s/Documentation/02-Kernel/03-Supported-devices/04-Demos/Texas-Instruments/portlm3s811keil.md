---
title: "Luminary Micro LM3S811 ARM Cortex-M3 移植，适用于 Keil RVDS IAR和 GCC 开发工具"
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
| <br />![lm3s811.jpg](/media/2018/lm3s811.jpg)<br /> |

目前有四种 FreeRTOS移植适用于基于 [Luminary Micro](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) Stellaris ARM Cortex-M3 的嵌入式微控制器，一种
使用 ARM Keil 工具，一种适用于[Rowley CrossWorks](http://www.rowley.co.uk/)，一种使用[IAR工具套件](http://www.iar.com/)，一种
[使用 Sourcery G + +](portcortexgcc)（来自 [CodeSourcery](http://www.codesourcery.com/)的GCC）。
本页介绍面向 Luminary MicroLM3S811 评估套件（EKK-LM3S811）的演示。提供了 Keil、 IAR 和 GCC 工具的使用说明。

LM3S811 评估套件包括一个小型低成本 PCB，
它依靠一条 USB 数据线供电、编程和调试。它具有适配 LM3S811 微控制器引脚的连接点、小型图形 LCD、用户按钮和用户 LED。

请参阅 LM3S102 演示应用程序，以获取同样展示如何使用协程的替代项目。

**升级到 FreeRTOS V5.0.3：**FreeRTOS V5.0.3 为 ARM Cortex-M3 移植引入了 configMAX_SYSCALL_interrupt_PRIORITY 配置选项。请参阅
[RTOS内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档以获取有关此功能的完整信息。

**升级到 FreeRTOS V4.8.0：**  在 V4.8.0 之前，FreeRTOS 内核未使用 SVCall 中断，从 V4.8.0 开始才使用 SVCall 中断。
因此，要将旧项目升级到 V4.8.0 标准，需要稍微编辑一下启动代码。要执行此操作，只需
将 vPortSVCHandler () 安装到中断向量表（包含在启动源文件中）内的 SVCall 位置。包含在
FreeRTOS 下载中的演示项目已更新，可以作为示例。

---

### 重要提示！使用 [Luminary Micro LM3S811](http://www.ti.com/product/lm3s811)移植的注意事项

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

Keil/RVDS 工具的 Stellaris LM3S811 演示项目文件名为 RTOSDemo.Uv2，应
位于 FreeRTOS/Demo/CORTEX_LM3S811_KEIL 目录中。

IAR 工具的 Stellaris LM3S811 演示项目文件名为 RTOSDemo.eww，应
位于 FreeRTOS/Demo/CORTEX_LM3S811_IAR 目录中。
**注意：**如果此项目未能使用 IAR 工具生成，则可能是 IAR
Embedded Workbench 版本过低造成的。如果是这种情况，
则项目文件也很可能（在无提示的情况下）已经损坏，
将其恢复至初始状态，然后使用新版本的 IAR 构建项目。

GCC 工具的 Stellaris LM3S811 演示生成文件可以在FreeRTOS/Demo/CORTEX_LM3S811_GCC 目录中找到。

---

### 演示应用程序

### 演示应用程序硬件设置

演示应用程序包括一个写入 UART 的任务。LM3S811 评估套件将充当 RS232 到 USB 的转换器，从而能够通过一条 USB 数据线
在哑终端上查看书面数据。
为了正确运行，必须安装 Luminary Micro 提供的 USB 驱动程序。当评估板首次插入并被 Windows 检测到时，将收到安装驱动程序的
提示。无需进一步硬件设置。

### 功能

main() 只需设置硬件，创建所有演示应用程序任务，
然后启动 RTOS 调度器。FreeRTOS 网站的[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节介绍了
有关标准演示任务的更多信息。

除了一个标准演示应用程序任务子集， main.c 还会
定义以下任务：

* **打印任务。**打印任务是唯一可以访问 LCD 的任务
 ——从而确保资源的相互排斥和访问一致性。
 其他任务不会直接访问 LCD，而是将要显示的文本
 发送到打印任务。打印任务大多数时候处于阻塞状态
 ——仅在消息排队显示时才唤醒。
* **“按钮处理程序”任务。**评估板包含一个
 配置为用于生成中断的用户按钮。中断处理程序使用
 信号量来唤醒按钮处理程序任务，演示如何用优先级机制
 将中断处理延迟到任务级别。按钮处理程序任务
 可以向 LCD（通过打印任务）和 UART
 （通过评估板上的 UART 到 USB 转换器）发送消息，
 该消息可以使用哑终端查看。注意：必须关闭哑终端
 以便重新闪烁微控制器。无需通过 FIFO 使用由中断驱动的
 非常基础的 UART 驱动程序。UART 被配置为 19200 波特。
* **“检查”任务。**检查任务每五秒钟才执行一次，但具有
 高优先级，保证能够获得处理器时间。其功能是
 检查其他所有任务是否仍在运行，并且在任何时候
 均没有检测到错误。如果从未检测到错误，则将 “PASS”
 写入显示屏（通过打印任务）；如果曾检测到错误，
 则消息将变成 “FAIL”。每次写入消息的位置
 均会变化。

当正确执行（没有检测到任何错误）时，演示应用程序将通过 UART 到 USB 转换器定期在 LCD 和哑终端上
显示 “PASS”。

### 驱动程序库

演示项目使用开发工具供应商或直接由 Luminary Micro 提供的驱动程序库。 Luminary Micro为了正确运行，驱动程序库版本
必须包含对 LM3S811 评估板的支持。驱动程序库直接包含在项目文件或 Makefile 中。在使用 Keil 工具的地方，
可能有必要调整库的路径，以匹配开发机器上的 Keil 安装路径。

![](/media/2018/driverlib.jpg)
驱动程序库包含在项目工作区或 Makefile 中。
可能需要调整
库
的路径以匹配您的开发工具安装路径。

### 构建和执行演示应用程序 - Keil

确保驱动程序库正确包含在项目工作区中：

1. 在 uVision IDE 中打开 FreeRTOS/Demo/CORTEX_LM3S811_KEIL/RTOSDemo.Uv2项目。
2. 在 "Project" 菜单中选择 "Rebuild all target files"。项目应该成功构建，不会报错或出现警告。
3. 将 LM3S811 开发板连接到主机 PC，并在出现提示时安装相关 USB 驱动程序。
4. 在 "Flash" 菜单中选择 "Download"。构建窗口应在几秒后指示设备已被擦除，随后对设备编程并最终进行验证。
5. 要调试应用程序，请在 "Debug" 菜单中选择 "Start/Stop Debug Session"，然后在同一菜单中点击 "Run"。

![](/media/2018/cortex_run.gif)
在调试器中运行应用程序

### 构建和执行演示应用程序 - IAR

1. 从 嵌入式工作台 IDE 中打开 FreeRTOS/Demo/CORTEX_LM3S811_IAR/RTOSDemo.eww 项目。
2. 在 "Project" 菜单中选择 "Rebuild all"。项目应该成功构建，不会报错或出现警告。
3. 将 LM3S811 开发板连接到主机 PC，并在出现提示时安装相关 USB 驱动程序。
4. 在 "Project" 菜单中选择 "Debug"。微控制器闪存将写入演示应用程序，并且调试器将启动。

### 构建和执行演示应用程序 - GCC

这些说明假设在 PATH 环境变量中已经安装、配置并包含了 Sourcery G++ 工具。

1. 打开命令提示符并导航到FreeRTOS/Demo/CORTEX_LM3S811_GCC 目录。
2. 键入 “Make”，项目应该成功构建，不会报错或出现警告，由此产生的二进制文件放置在名为  gcc 的目录中

示例输出：

```c

C:/E/Dev/FreeRTOS/Demo/CORTEX_LM3S811_GCC>make
  CC    init/startup.c
  CC    main.c
  CC    ../../Source/list.c
  CC    ../../Source/queue.c
  CC    ../../Source/tasks.c
  CC    ../../Source/portable/GCC/ARM_CM3/port.c
  CC    ../../Source/portable/MemMang/heap_1.c
  CC    ../Common/Minimal/BlockQ.c
  CC    ../Common/Minimal/PollQ.c
  CC    ../Common/Minimal/integer.c
  CC    ../Common/Minimal/semtest.c
  CC    hw_include/osram96x16.c
  LD    gcc/RTOSDemo.axf

C:/E/Dev/FreeRTOS/Demo/CORTEX_LM3S811_GCC>

```
3. 进入 GCC 目录。
4. 键入 “arm-stellaris-eabi-gdb RTOS Demo.axf” 以启动调试器。
5. 在出现 GDP 提示时 | 在出现 GDP 提示时键入 “target extended-remote \| arm-stellaris-eabi-sprite -r -s 2 -f lmi stdio” 以连接到主板。
6. 键入 “load” 以对微控制器闪烁进行编程。
7. 键入 “continue” 以开始执行程序。

示例输出：

```c

C:/E/Dev/FreeRTOS/Demo/CORTEX_LM3S811_GCC>cd gcc

C:/E/Dev/FreeRTOS/Demo/CORTEX_LM3S811_GCC/gcc>arm-stellaris-eabi-gdb RTOSDemo.axf
GNU gdb (Sourcery G++ 4.1-23) 6.5.50.20060822-cvs
Copyright (C) 2006 Free Software Foundation, Inc.
GDB is free software, covered by the GNU General Public License, and you are
welcome to change it and/or distribute copies of it under certain conditions.
Type "show copying" to see the conditions.
There is absolutely no warranty for GDB.  Type "show warranty" for details.
This GDB was configured as "--host=i686-mingw32 --target=arm-stellaris-eabi".
For bug reporting instructions, please see:
.
..
(no debugging symbols found)
(gdb) target extended-remote | arm-stellaris-eabi-sprite -r -s 2 -f lmi stdio
Remote debugging using | arm-stellaris-eabi-sprite -r -s 2 -f lmi stdio
0x000000c4 in ResetISR ()
(gdb) load
Loading section .text, size 0x241c lma 0x0
Loading section .data, size 0x4 lma 0x241c
Start address 0xc5, load size 9248
Transfer rate: 73984 bits/sec, 840 bytes/write.
(gdb) continue
Continuing.

```

---

### 配置和用法详情

### RTOS 移植特定配置

此移植的特定配置项目位于 FreeRTOS/Demo/CORTEX_LM3S811_[compiler]/FreeRTOSConfig.h，其中的 “[compiler]” 是 Keil、IAR 或 GCC。可编辑
在本文件中定义的常量，以适配您的应用程序。特别是-

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS tick 的频率。提供的数值 1000 Hz 可用于
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，获取有关这些配置常量的完整信息。

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

中断向量表包含在FreeRTOS/Demo/CORTEX_LM3S811_KEIL/startup_rvmdk.s, FreeRTOS/Demo/CORTEX_LM3S811_IAR/startup.c 或
FreeRTOS/DEMO/CORTEX_LM3S811_GCC/init/startup.c（分别用于Keil、 IAR 和 GCC 演示），并且可根据需要进行填充。在演示应用程序中
向量表保持在闪存中。

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档进行编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。有关 UART ISR 定义，请参阅
[Keil/ARM LM3S102](portcortexkeil)、 [GCC LM3S102](portcortexgcc)或[IAR LM3S316](portcortexiar)演示应用程序中的示例。

### 抢占式内核和协同式 RTOS 内核之间的切换

将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_2.c 位于 ARM Cortex-M3 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 部分，
以获取完整信息。

### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。
