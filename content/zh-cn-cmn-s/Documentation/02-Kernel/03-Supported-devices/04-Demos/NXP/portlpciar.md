---
title: "Philips（现为 NXP）LPC2129 (ARM7) RTOS 移植 适用于 IAR 开发工具"
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
| <br />![mcb2100.gif](/media/2018/mcb2100.gif)<br /> |

目前，基于 Philips LPC2000 ARM7 的嵌入式微控制器包含四个 FreeRTOS 移植。
此页面仅涉及 [IAR 开发工具](http://www.iar.com/ewarm)移植。

该移植在 [MCB2100 开发板/原型板](http://www.keil.com/mcb2100)上
使用 J-LINK USB JTAG 接口开发（如果希望使用其他开发板，可以参考此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。

MCB2100 是一款功能齐全的原型板，可轻松访问 LPC2129 外设，
包括 8 个由 FreeRTOS 演示应用程序使用的内置 LED。

**注意：**如果项目构建失败，可能是使用的 IAR
Embedded Workbench 版本过低。如果是这种情况
则项目文件也很可能（在无提示的情况下）已经损坏，
即使已更新 IAR版本，也需要将项目文件恢复到初始状态，才能构建项目。

---

### *重要！使用 IAR LPC2000 RTOS 移植的注意事项*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件多于此演示使用的文件。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

此演示的 IAR Embedded Workbench 项目文件位于 Demo/ARM7_LPC2129_IAR 目录，
该目录还包含 main.c，即包含 main() 函数的源文件。

Demo/ARM7_LPC2129_IAR/SrcIAR 和 Demo/ARM7_LPC2129_IAR/resource 目录
包含 IAR Philips 构建环境的支持文件。

---

### 演示应用程序

FreeRTOS 源代码下载包含用于 IAR LPC2129 RTOS 移植的完全抢占式多任务演示应用程序。

#### 功能

可使用 IAR 开发工具 KickStart 版本构建演示应用程序，该版本文件大小限制
为 32K 字节。

项目文件中提供了两个配置："Flash Debug"（无优化）和
"Flash Bin"（完全优化）（不包括静态群集选项）。

此演示应用程序可创建 25 个标准演示任务、一个空闲任务和一个“check”任务。
请参阅  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解各个任务的详细信息。
如果该演示应用程序正确执行，将实现以下效果：

* LED P1.16、P1.17 和 P1.18 由 "flash" 任务控制。每个 LED 将以恒定频率闪烁，LED P1.16 的频率最高，
 LED P1.18 的频率最低。
* 串行端口上每传输一个字符， LED P1.19 都会闪烁。
* 串行端口上每传输一个字符， LED P1.20 都会闪烁。
* 并非所有任务都会改变 LED，所以没有可见的指示来表明它们运行正常。
 因此，系统创建了一个检查任务，用于确保所有其他任务中没有检测到任何错误。

 LED P1.23 由检查任务控制。检查任务每 3 秒就会将系统中的所有任务检查一次，
 以确保任务执行无误。然后切换 LED P1.23。如果 LED P1.23 每 3 秒切换一次，
 则表明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一个错误。可以通过将环回连接器从串行端口（如上述）上移除来检查此机制，
 这样做是在故意制造一个错误。

#### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在 COM 0 的 P2 串行端口连接器上
将引脚 2 和 3 连接在一起）。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。

#### 构建演示应用程序

只需在 IAR IDE 中打开 RTOSDemo.ewp 项目工作区文件，选择所需的配置，
然后在 IDE "Project" 菜单中
选择 "Make"。应用程序在构建过程中不应出现任何错误或警告。

![](/media/2018/ewprojselect.jpg)
选择 "Flash Debug" 配置

#### 运行演示应用程序

IAR 移植无法通过  IAR 模拟器执行，因此必须在目标硬件上执行：
1. 确保 J-Link JTAG 调试接口已连接，并且原型板已接通电源。
2. 在 IDE 的 "Project" 菜单中选择 "Debug"。
3. 微控制器闪存将自动使用演示应用程序进行编程，
 并且调试器
 会在 main() 函数处中断。在 IDE 的 "Debug" 菜单中选择 "Go" 以开始执行应用程序。

可选择使用“项目选项”对话框
中的“调试器”类别替代 JTAG 接口。

---

### 配置和用法详情

#### RTOS 移植特定配置

此移植的特定配置项位于 Demo/ARM7_LPC2129_IAR/FreeRTOSConfig.h 中。可以编辑此文件中定义的常量
确保适配您的应用程序。特别是，可以将定义 configTICK_RATE_HZ 用于设置
RTOS 滴答的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但
此速度超过了大部分应用程序的要求。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

不会引起上下文切换的中断服务程序没有特殊要求，可以按照
正常的 IAR 语法写入。
例如：

```c

    static __arm __irq void vAnISR( void )
    {
        /* ISR C code goes here. */

        /* End the interrupt in the VIC. */
        VICVectAddr = 0;
    }

```

通常情况下，您需要中断服务程序来引起上下文切换。例如，正在被接收的串行端口字符
可能会唤醒在等待该字符时被阻塞的高优先级任务。如果 ISR 中断了一个优先级较低的任务，
则其应立即返回到已被唤醒的任务。由于 IAR 内联汇编器的限制，
中断服务程序必须包含汇编文件包装器。

#### 具备上下文切换功能的 ISR 示例

可按照下列模板，在任何源文件中用 C 语言编写 ISR 主体部分。这只是一个普通的
ARM 模式函数，其结尾处包括对 portEND_SWITCHING_ISR() 的调用。

```c

    /* For simplicity the C function should operate in ARM mode.
       Note that the __irq modifier is NOT used. */

    __arm void vASwitchingISR( void )
    {
        char cContextSwitchRequired;

        /* Write the ISR body here as per normal.

        A boolean is used to say whether a context switch is required.
        In this example assume we posted onto a queue and this caused a
        task to be woken. */

        cContextSwitchRequired = pdTRUE;

        /* Immediately before the end of the ISR call the
        portEND_SWITCHING_ISR() macro. */

        portEND_SWITCHING_ISR( ( cContextSwitchRequired ) );

        /* End the interrupt in the VIC. */
        VICVectAddr = 0;
    }

```

有关完整示例，请参阅在 Demo/ARM7_LPC2129_IAR/serial/serial.c 中定义的函数 vSerialISR()。

ISR 的入口点必须写入汇编文件中。这只是
在调用 portSAVE_CONTEXT() 和 portRESTORE_CONTEXT() 宏之间分别放置一个 C 函数，具体操作模板如下所示：

```c

        EXTERN vASwitchingISR
        PUBLIC vASwitchingISREntry

    /* This header defines the save/restore macros. */
    #include "ISR_Support.h"

    vASwitchingISREntry:

        portSAVE_CONTEXT      ; Call portSAVE_CONTEXT macro first
        bl  vASwitchingISR    ; Then call the function written in the C file.
        portRESTORE_CONTEXT   ; Call portRESTORE_CONTEXT last.

        END

```

有关完整示例，请参阅 Demo/ARM7_LPC2129_IAR/serial/serialIAR.S79 文件。

#### 使用 LPC2129 以外的部件

LPC2129 使用带有特定于处理器的外围设备的标准 ARM7 内核。核心实时内核组件应该
可以在所有 ARM7 设备上移植，但是需要考虑到外设设置和内存需求。
注意事项：
* Source/portable/IAR/LPC2000/port.c 中的 prvSetupTimerInterrupt() 可用于配置 LPC2129 定时器 0 以生成 RTOS 滴答。
* 端口、内存访问和系统时钟配置由 Demo/ARM7_LPC2129_IAR/main.c 中的 prvSetupHardware() 配置。
* 中断服务例程设置和管理假设存在矢量中断控制器。
* 串口驱动程序。
* 文件 iolpc2129.h 提供了寄存器位置定义，该文件位于 Demo/ARM7_LPC2129_IAR/FreeRTOSConfig.h 的顶部。
* 启动代码位于 Demo/ARM7_LPC2129_IAR/SrcIAR/cstartup.s79. main() 中。调用 main() 时，
 处理器处于监管者模式。
* RAM 大小：参见下文“内存分配”部分。

#### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/ARM7_LPC2129_IAR/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式内核；
设置为 0，可使用协同式内核。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
以提供的演示应用程序项目文件为基础构建您的应用程序，如[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分所述。

#### 执行上下文

RTOS 调度器以监管者模式执行，任务以系统模式执行。

注意：
 启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。

中断服务程序总是在 ARM 模式下运行。其他所有代码将运行在 ARM 或 THUMB 模式，这取决于构建。
应该注意的是，portmacro.h 中定义的一些宏只能从 ARM 模式代码调用，而且如果从 THUMB 代码
调用会导致编译时错误。Embedded Workbench 项目配置为 THUMB 模式，请参阅 LPC2006 GCC 移植，
了解仅使用 ARM 模式所需的配置示例。

Demo/ARM7_LPC2129_IAR/Startup.s 仅为系统/用户、IRQ 和 SWI 模式配置堆栈。

SWI 指令由实时内核使用，不能被应用程序代码使用。

#### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ARM7 演示应用程序的 makefile 中，以提供实时内核所需的
内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
以获取完整信息。

#### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
用于表示优化过的解决方案。
