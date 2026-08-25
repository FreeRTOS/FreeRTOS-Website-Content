---
title: "适用于IARARM开发工具的 ST Microelectronics STR71x 移植"
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
| <br />![](/media/2018/strboard.jpg)带 LED 和环回连接器的 KickStart 板<br /> |

ST ARM7 移植是在
[STR712-SK/IAR KickStart 开发套件(http://www.st.com/internet/evalboard/product/152464.jsp)]中的原型板上开发的
（如果您希望使用替代开发板，我们也提供了[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。

STR712F 是一款外设丰富（包括 CANBus）、低引脚计数、基于 ARM7TDMI 的闪存嵌入式微控制器。
评估套件配备一个适用于 ARM 的无时限评估版[IAR嵌入式工作台开发
工具](http://www.iar.com/ewarm)（仅限 32KB）、一个 J-Link USB JTAG 调试器接口和一条 USB 数据线。可通过 USB JTAG 连接器或
使用外部电源为开发板充电。

开发工具含有一整套由编译器、汇编器和链接器组成的工具链、IDE 以及有限
功能模拟器。

使用 ST 提供的处理器外设库来提升开发效率。

**注意：**如果项目构建失败，很可能是使用的IAR
嵌入式工作台版本过低。如果构建失败，
那么也可能是项目文件(在无提示的情况下)已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR 。

---

### *重要提示！关于使用 ST ARM7 RTOS 移植的注意事项*

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和用法详情)

另请参阅常见问题: [我的应用程序未运行，哪里出错了?](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载内容包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
有关下载文件的描述和创建新项目的信息。

STR71x IAR ARM7 移植包含 THUMB 模式示例项目。工作区 *rtosdemo.eww*位于
IARDemo/ARM7_STR71x_ 目录中，应从 Embedded Workbench IDE 中打开。

Demo/ARM7_STR71x_IAR/library 目录包含演示应用程序使用的 ST 外设库组件
。

Demo/ARM7_STR71x_IAR/serial 目录包含一个
中断驱动的 RS232 串行移植驱动器的样本。

---

### 演示应用程序

FreeRTOS 源代码下载文件包含适用于 STR71x RTOS 移植的完全抢占式多任务演示应用程序。

#### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在标记为 RS232_1 的串行端口连接器上
将引脚 2 和 3 连接在一起即可）。演示应用程序使用 UART 0。KickStart 开发板上的跳线应
保留在默认位置，以确保 UART 0 连接到 RS232_1 连接器上。

此演示应用程序使用原型板上的内置 LED。这一个 LED 足以检查
演示是否正常运行工作（请参阅下文“检查”任务叙述章节），但为获得最佳效果，还另需四个 LED
。这些 LED 应连接到标记为 T1_OCMPA、T1_OCMPB、T1_ICAPB 和 T1_ICAPA 的排针引脚上。
在执行应用程序时，这些引脚被设置为 GPIO 输出。

#### IAR 工作区

![](/media/2018/str7proj.gif)
演示应用程序工作区

IDE 工作区包含 4 个文件夹：

1. **演示源文件**

 包含演示应用程序的源文件。
2. **库源文件**

 包含 RTOS 内核和演示应用程序使用的 ST 外设库的组件。
3. **RTOS 源文件**

 包含 FreeRTOS 实时内核的源文件。
4. **系统文件**

 包含启动代码、链接器脚本和中断向量表定义。

#### 构建演示应用程序

目前提供两种项目配置。“Debug” 包含最小优化，可与 J-Link JTAG 调试接口
一起使用。"Release" 包含完整优化，不包含调试信息。

只需在IAR嵌入式工作台 IDE 中打开 rtosdemo 工作区文件，确保根据需要选择*调试*或 *释放*（上图红色标记部分），
然后在 IDE 的 “Project” 菜单中选择 “Rebuild All”。

#### 运行演示应用程序

1. 确保 J-Link JTAG 调试接口已连接，并且原型板已接通电源。
2. 在 IDE 的 "Project" 菜单中选择 "Debug"。
3. 微控制器闪存将自动使用演示应用程序进行编程，并且调试器
 会在 main () 中断（C 源调试仅在使用*调试* 配置时可用）。
 在 IDE 的 "Debug" 菜单中选择 "Go" 以开始执行应用程序。

一旦将演示编程到闪存中，则无需调试器，仅需移除 JTAG 接口
并接通电源即可执行。

#### 功能

此演示应用程序可创建 25 个任务，其中包括 23 个标准演示任务、一个“检查”任务和一个空闲任务。请参阅
 [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分，了解标准演示任务的详细信息。

如果演示应用程序执行正确，则会有如下表现：

* 连接到标记为 T1_ICAPA、T1_ICAPB 和 T1_OCMPB 排针引脚的 LED 由 “闪烁” 任务控制。
 每个 LED 都将以恒定频率闪烁， T1_ICAPA 引脚上的 LED 频率最高，T1_OCMPB
 引脚上的 LED 频率最低。请注意，这些引脚都被设置为 GPIO 输出。
* 标记为 T1_OCMPA 的 LED 排针引脚由标准 ComTest Rx 任务控制。每次 ComTest Tx 任务
 通过 RS232 端口接受并验证字符时，其状态都会切换。环回连接器就位后，
 LED 应会快速闪烁。移除环回连接器会导致 LED 永久打开或
 关闭。
* 并非所有任务都会更新 LED 状态，所以没有可见的指示来表明它们运行正常。
 因此，系统创建了一个“检查”任务，以确保在其他任务中没有检测到任何错误。

 KickStart 开发板上内置的红色 LED 由“检查”任务控制。“检查”任务每三秒钟就会
 将系统中的所有任务检查一次，
 以确保它们执行无误。检查完后，它会切换红色 LED。因此，如果红色 LED 每三秒切换一次
 则说明没有检测到错误。如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一个错误。可以通过将环回连接器从串行端口（如上述）移除来检查此机制，
 因为这样做是在故意制造一个错误。

---

### 配置和用法详情

#### RTOS 移植特定配置

此移植的特定配置项目位于 Demo/ARM7_STR71x_IAR/FreeRTOSConfig.h中。可以编辑此文件中定义的常量，
确保适配您的应用程序。特别是，configTICK_RATE_HZ 定义用于
设置 RTOS tick 的频率。所提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但该值
高于大多数应用程序要求的频率。降低该值将会提高效率。

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

        /* End the interrupt in the EIC. */
        portCLEAR_EIC();
    }

```

通常情况下，您需要中断服务程序来引起上下文切换。例如，正在被接收的串行端口字符
可能会唤醒在等待该字符时被阻塞的高优先级任务。如果 ISR 中断了一个优先级较低的任务，
则其应立即返回到已被唤醒的任务。由于 IAR 内联汇编器的限制，
中断服务程序必须包含汇编文件包装器。

#### 具备上下文切换功能的 ISR 示例

可按照下列模板，在任何源文件中用 C 语言编写 ISR 主体部分。这只是一个普通的
ARM 模式函数，其结尾处包括对 END_SWITCHING_ISR() 的调用。

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

        /* End the interrupt in the EIC. */
        portCLEAR_EIC();
    }

```

请参阅 Demo/ARM7_STR71x_ **/serial/serial.c 中定义的函数vSerialISR()** IAR以了解完整示例。

ISR 的入口点必须写入汇编文件中。这只是
在调用 portSAVE_CONTEXT() 和 portRESTORE_CONTEXT() 宏之间分别放置一个对 C 函数的调用，具体操作模板如下所示：

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

请参阅文件 Demo/ARM7_STR71x_IAR/serial/serialIAR.S79 以了解完整示例。

#### 使用 STR712F 以外的部件

STR71x 系列使用标准的 ARM7 核心，因此主要的实时内核组件
能在所有 ARM7 设备上移植 - 但需考虑外设设置和内存要求。
应考虑的事项：

* source/portable/IAR/STR71x/port.c 中的 prvSetupTimerInterrupt () 会对看门狗外围设备进行配置
 以生成 RTOS 滴答。
* 中断服务程序设置和管理假设存在中断控制器。
* 串行端口驱动器。
* 寄存器位置定义由库头文件提供。
* 启动代码和向量表设置包含在 Demo/ARM7_STR71x_IAR/SrcIAR/CStartup.s79 中。
* RAM 大小：参见下文内存分配部分。

#### 在抢占式和协同式 RTOS 内核之间切换

将 Demo/ARM7_STR71x_IAR/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，即可使用抢占式内核；
将其设置为 0，则可使用协作式内核。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是以
提供的演示应用程序项目文件为基础构建您的应用程序，如 [源组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization) 章节所示。

#### 执行上下文

RTOS 调度器以监管者模式执行，任务以系统模式执行。
注意：
 启动 RTOS 调度器时(调用 vTaskStartScheduler)，处理器必须处于监管者模式
 。FreeRTOS 下载内容中所包含的演示应用程序
 会在 main 函数调用前切换到监管器模式。如果您没有使用
 这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。

中断服务程序总是在 ARM 模式下运行。其他所有代码都在 THUMB 模式下执行。

*注意 *：每个必要操作模式的堆栈大小要使用文件
Demo/ARM7_STR71x_IAR/CStartup.s79 中定义的常量来配置。这里既**不**使用IAR链接器配置实用程序，
也 **不**将堆栈设置为适用于所有操作模式。

SWI 指令由实时内核使用，因此不能被应用程序代码使用。

#### 内存分配

Source/Portable/MemMang/heap_2.c 包含在 ARM7 演示应用程序项目中，
以提供实时内核所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

#### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
代表优化的解决方案。特别是，它们并不使用 FIFO。

#### 滴答中断

看门狗外设用于生成滴答中断。

#### IAR 编译器注意事项

构建 FreeRTOS 源代码必须使用大量不同的编译器。IAR 编译器拥有特别强大的
(pedantic) 源检查功能，在编译 FreeRTOS 源代码时会生成几个警告。

遗憾的是，仅仅修改源代码无法修复这些警告，因为这些警告主要与良性代码有关，
添加这些良性代码是为了修复其他编译器生成的警告（主要与类型转换有关）。
因此，项目文件中已经禁用部分警告。
