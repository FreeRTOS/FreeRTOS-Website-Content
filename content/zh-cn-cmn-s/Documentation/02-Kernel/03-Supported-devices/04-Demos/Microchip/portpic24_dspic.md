---
title: "PIC24 MCU 和 dsPIC ® DSC RTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2024/boardDebugger.jpg)

此页介绍了 FreeRTOS 移植和演示应用程序，
适用于 [Microchip' 的 dsPIC 微控制器](https://www.microchip.com/en-us/products/microcontrollers-and-microprocessors/dspic-dscs) 和
[Microchip' 的 PIC24 微控制器](https://www.microchip.com/en-us/products/microcontrollers-and-microprocessors/16-bit-mcus) 产品。

为不同系列的设备提供了多个演示应用程序。大多数演示都针对 Explorer16 开发板
（如果您希望使用替代开发板，我们也提供了说明）并使用 Microchip' 的 [XC16 或 XC-DSC](https://www.microchip.com/xc)。
有些演示使用其他开发板（Curiosity 平台开发板），有关开发板和编译器的详细信息，请参阅各个演示的自述文件。

---

#### 重要提示！PIC24 和 dsPIC33 移植使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示使用的文件多很多。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，
了解下载文件的描述和有关创建新项目的信息。

不同设备变体的演示代码可在  PIC24_DSPIC_MPLABX\Demo 目录中找到。

设备和项目专用文件放在每个单独的文件夹下，通用文件夹包含通用代码。

---

### 演示应用程序

本节内容与 PIC24 和 dsPIC33 演示应用程序有关。

#### 演示应用程序硬件设置

所有 Explorer 16 跳线都可以保留在默认位置，特别是，应配备 JP2 以确保 LED 能正确运作。

演示应用程序包含通过 UART 发送和接收字符的任务。一个任务发送的字符必须由另一个任务接收，
如果丢失了任何字符或接收顺序错误，则会标记错误情况。UART TX 和 RX 引脚需要短接，具体引脚编号请参阅各个项目的自述文件。

有关特定设备的硬件设置，请参阅每个项目目录下的自述文件。

### 功能

演示应用程序可创建 14 个任务（包括空闲任务）、5 个协程和一个高频中断测试。正确执行时，演示设置如下：
* 标记为 D3 至 D7 的 LED 由 "flash" 协程控制。各灯都将以恒定的频率闪烁，其中 LED D3 最快，LED D7 最慢。
 这个基本示例演示了如何将协程与任务混合。
* 串行端口上每传输一个字符， LED D9 都会切换。该频率使您无法区分字符之间的每一次切换，
 尽管您可以查看完整消息传输之间的间隔。
* 每当在串行端口上接收和验证字符时， LED D10 都会闪烁（通过环回连接器）。
 同样地，切换频率太高，会导致无法区分单次切换。
* 大多数任务不会更新 LED ，因此没有明确迹象表明它们运行正常。因此，创建了一个“检查”任务，
 用于确保任何其他任务或协程中没有检测到任何错误。检查任务每三秒钟监控一次系统运行，然后向 LCD 写入 PASS 或 FAIL 消息。
 任何故障都会被锁定，显示的消息指示检测到故障的任务（可以通过在演示执行时移除环回连接器来测试此功能）
 。如下一个要点所述，PASS 消息是一个时间度量，以纳秒为单位。
* 使用自由运行定时器产生高频周期性中断，以演示如何使用配置常量 configKERNEL_INTERRUPT_PRIORITY。
 中断服务程序测量在各中断之间发生的处理器时钟的数量，由此测量中断定时中的抖动。
 测得的最大抖动时间测锁定在 usMaxJitter 变量中，并通过如下所述的“检查”任务显示在 LCD 显示屏上。中断频率设置为 20KHz。
 此测试演示如何配置 RTOS 内核，使其不会影响中断服务程序的延迟。
* 该应用程序还演示了如何使用“网关守卫”任务，在这种情况下使用的是 LCD 网关守卫。LCD 任务是唯一有权直接访问 LCD 的任务。
 其他希望向 LCD 写入信息的任务会将队列中的信息发送给 LCD 任务，而不是自己访问 LCD。 
 LCD 任务只是阻塞在队列中等待消息，在消息到达时唤醒，并显示消息。

注意：在内存较小的设备上，任务数量会减少。

### 构建并执行演示应用程序

这些说明假设您的主机计算机上已正确安装了 MPLABX 和 XC16 或 XC-DSC 编译器。

要构建应用程序：

1. 在 MPLABX IDE 中打开演示应用程序工作区。
2. 右键单击项目，然后单击“清理并构建”，或者也可以转到“生产”，然后单击“清理并构建主项目”。

要在 MPLABX 模拟器中运行应用程序：

1. 右键单击并选择项目属性。在“连接硬件工具”下拉菜单中选择“模拟器”。
2. 在 main() 函数（包含在 main.c 内）中设置第一个指令的断点。
3. 从“调试”菜单中选择“调试主项目”（确保已将项目设置为主项目，右键单击项目，然后选择“设置为主项目”）。
 应用程序将开始执行，并在达到断点时停止。然后就可以使用标准调试器命令对应用程序进行操作了。

在模拟器内执行时，标准 ComTest 接收任务将不会接收任何字符（没有环回连接器），导致
 “检查”任务在通信测试任务中检测到一个错误。

要使用 [ICD 或 PICKit](https://www.microchip.com/en-us/tools-resources/debug/programmers-debuggers) 接口调试 Explorer 16 上的应用程序：

1. 将 ICD 或 PICKit 连接到 Explorer 16/32 开发板或任何其他适用的开发板上，如开发板手册所述。
2. 右键单击并选择项目属性。在“连接的硬件工具”下拉菜单中选择列出的 ICD 或 PICKit 设备。
3. 再次从“调试”菜单中选择“调试主项目”。
4. 在 main() 函数（包含在 main.c 内）中设置第一个指令的断点。
5. 从“调试”菜单中选择“继续”。应用程序将开始执行，并在达到断点时停止。
 然后就可以使用标准调试器命令对应用程序进行操作了。

在微控制器闪存中独立运行应用程序：

1. 将 ICD 或 PICKit 连接到 Explorer 16/32 开发板或任何其他适用的开发板上，如开发板手册所述。
2. 从 MPLABX IDE 的“生产”菜单中选择“制作和编程设备主项目”。
3. 断开电路板电源，然后拔下 ICD 或 PICKit 接口电缆。
4. 最后，再次通电以开始执行应用程序。

---

### 配置和用法详情

#### RTOS 移植特定配置

此移植的特定配置项目位于 PIC24_DSPIC_MPLABX/Demo/[dspic33c-client-freertos-demo | dspic33c-host-freertos-demo |
 dspic33e-freertos-demo \| dspic33f-freertos-demo \| pic24-freertos-demo]/FreeRTOSConfig.h。可以编辑此文件中定义的常量，以适配您的应用程序。
 尤其是以下常量：

* **configTICK_RATE_HZ**
  该常量可以用于设置 RTOS tick 的频率。演示项目提供的数值1000 Hz可用于测试 RTOS 内核功能，但速度高于大多数应用程序所需要的速度。
  降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY**
  此常量设置了 RTOS 内核使用的中断优先级。RTOS 内核应使用低中断优先级，以允许更高优先级的中断不受
  RTOS 内核进入临界区的影响。临界区不是全局禁用中断，而是仅禁用
  低于 RTOS 内核中断优先级的中断。

  因此中断处理非常灵活：

    1. 在 RTOS 内核的优先级上，可以根据系统中的任何其他任务编写中断处理“任务”并设置优先级。
     这些是被中断唤醒的任务。编写的中断服务程序 (ISR) 本身应尽可能短小，
     - 因为它只是抓取数据，然后唤醒高优先级处理程序任务。ISR 随后直接返回到唤醒的处理程序任务，因此中断处理在时间上是连续的，
     就像所有处理都在 ISR 中完成一样。这样的好处是，在处理程序任务执行期间，所有中断都保持启用状态。
    2. 运行在 RTOS 内核优先级以上的 ISR 不会被 RTOS 内核本身屏蔽，因此其响应性不会受到 RTOS 内核功能的影响。
     但是，此类 ISR 无法使用 FreeRTOS API 函数。本演示中的快速定时器中断测试演示了这种配置。

    遗憾的是，由于 GCC 内联汇编器的限制，修改该值需要对移植源代码中的中断屏蔽值
     （通过内联汇编器指令访问）进行小幅更新。移植源代码中包含一个 #error 指令，
     用于指示所需更新的位置，并提供所需更新的指令。 

每个移植都会使用 #define 将 "BaseType_t" 定义为该处理器的最有效数据类型。此移植将 BaseType_t 定义为短整型。

请注意，vPortEndScheduler() 尚未实现。

### 设备特定配置

xc.h 包含在 FreeRTOSConfig.h 的顶部，其中将包含相关的设备头文件。

#### 中断服务程序

不会引起上下文切换的中断服务程序没有特殊要求，可以按照编译器文档编写。

可以引起上下文切换的中断服务程序必须以优先级 portKERNEL_INTERRUPT_PRIORITY 执行，
并且只能在中断源被清除后，在服务程序的最末端调用 taskYIELD()。如需示例，请参阅演示应用程序中包含的文件 serial.c。

#### 临界区

退出临界区会始终将中断优先级掩码设置为 0（所有中断均已启用），无论在进入临界区时的
级别为何。FreeRTOS API 函数本身将使用临界区。

#### Shadow 寄存器

Shadow 寄存器不会被保存为任务上下文的一部分。

#### PSV 位处理

必须为每个任务设置同等的 CORCON 寄存器中的 PSV 位。如果需要更改默认位设置，必须在创建任何任务之前进行。

#### 抢占式内核和协同式 RTOS 内核之间的切换

在 PIC24_DSPIC_MPLABX/Demo/[dspic33c-client-freertos-demo | dspic33c-host-freertos-demo | dspic33e-freertos-demo | dspic33f-freertos-demo | pic24-freertos-demo]/FreeRTOSConfig.h 中将 configUSE_PREEMPTION 设置为 1 即可使用抢占式调度，设置为 0 即可使用协同式调度。如果 configIDLE_SHOULD_YIELD 设置为 1，则仅当 configUSE_PREEMPTION 设置为 0 时，演示应用程序才会正确执行 。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。保证这一点的最佳方法是将应用程序建立在提供的演示应用程序文件上。

#### 内存分配

PIC24 和 dsPIC33 演示应用程序项目中包含 Source/Portable/MemMang/heap_1.c，用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的内存管理章节，以了解全部信息。

#### 串口驱动程序

还应注意的是，编写串行驱动程序是为了测试某些实时内核功能，并不代表优化的解决方案。

