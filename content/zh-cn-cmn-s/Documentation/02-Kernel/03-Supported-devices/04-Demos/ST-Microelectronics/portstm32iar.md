---
title: "STMicroelectronics STM32F103 ARM Cortex-M3 演示"
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
| <br />![](/media/2018/stm32.jpg)<br /> |

本页介绍的 FreeRTOS 演示应用程序适用于 [STMicroelectronics STM32 ARM Cortex-M3 微控制器](http://www.st.com/internet/mcu/subclass/1169.jsp)。本演示使用适用于 ARM 的 IAR Embedded Workbench 开发工具，
并且预配置为在 ST 的 STM32 评估板上运行（如需使用其他开发板，请参阅[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。
评估板配备有 STM32F103VB 微控制器，
该微控制器包含 128 KB 的板载闪存和 20 KB 的板载 RAM。STM32F103VB 还包括 USB 和 CANbus 外设。

**注意：**如果项目构建失败，很可能是使用的 IAR
Embedded Workbench 版本过低。如果是这种情况，
则项目文件也很可能（在无提示的情况下）已经损坏，
即使已更新 IAR 版本，也需要将项目文件恢复到初始状态，才能构建项目。

---

### *重要！使用 STM32 ARM Cortex-M3 演示的注意事项*

*使用此 RTOS 移植之前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示所需的多得多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
下载文件的描述和有关创建新项目的信息。

STM32F103 演示的 IAR 工作区文件名为 RTOSDemo.eww，位于 FreeRTOS/Demo/CORTEX_STM32F103_IAR 目录中。

---

### 演示应用程序

#### 演示应用程序硬件设置

演示应用程序包含受中断驱动的 UART 测试，其中一个任务传输字符，该字符随后由另一个任务接收。为确保该功能
的正常操作，必须将环回连接器安装到 STM32 评估板的 UART00 连接器
（引脚 2 和 3 必须在9 路连接器上连接在一起）。

此演示应用程序使用了在原型板上构建的 LED 显示屏，因此无需使用其他硬件设置。

使用 J-Link USB JTAG 接口将主机与目标连接。

#### 构建和运行演示应用程序

1. 在 Embedded Workbench IDE 中打开 FreeRTOS/Demo/CORTEX_STM32F103_IAR/RTOSDemo.eww 项目。
2. 在 IDE 的 "Project" 菜单中选择 "Rebuild All"。项目若构建成功，不会报错或出现警告。
3. 在 IDE 的'Project' 菜单中选择 'Debug'。将用新建二进制数组对微控制器闪存进行编程，而且调试器将
 在进入 main () 时中断。

该项目包括内置在二进制数组中的位图。这将导致二进制数组大小变大，并且在某些优化级别下，
导致构建大小超过 Embedded Workbench Kickstart 版本的 32K 限制。如果出现该问题，则可以通过
从构建中删除位图来减少代码大小（从 lcd_message.h 中删除 pcBitmap 数组，并在同一文件中注释对 LCD_DrawMonoPict() 的调用）。

#### 功能

此演示应用程序创建了 24 个持久任务，并定期动态创建和销毁另外 4 个任务。这些任务
主要包括标准演示应用程序任务（请参阅  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，
了解各个任务的详细信息）。

除了标准演示任务外，还创建了以下任务和测试：

* 高优先级中断测试
 使用一个由自由运行的定时器
 生成的高频周期性中断，来演示
 'configKERNEL_INTERRUPT_PRIORITY' 配置常数的使用。中断
 服务程序测量
 每个中断之间发生的处理器时钟的数量 - 从而测量中断计时的抖动。
 测得的最大抖动时间被锁定在 ulMaxJitter 变量中，
 并通过“检查”任务显示在 LCD 显示屏上，如下所述。在
 timertest.c 源文件中配置和处理快速中断。这
 演示了如何配置 RTOS 内核
 才能不对优先级更高的中断处理造成影响。

 当在处理较低优先级中断过程中出现较高优先级中断时，
 ARM Cortex-M3 核心可以加快进入中断服务程序的速度（从而减少延迟），
 最多 8 个周期。因此，测得的抖动时间应
 不超过 8 个时钟周期。
* LCD 任务
 LCD 任务是一项“网关守卫”任务。这是唯一一项
 被允许直接访问显示器的任务。其他任务要向
 LCD 写入消息，需将消息发送到一条队列中，然后再向 LCD 任务发送该队列，而不是
 直接访问 LCD。LCD 任务只在队列中阻塞，
 等待消息，在消息到达时唤醒并显示消息。
* 检查任务
 检查任务每 5 秒执行一次，但
 具有最高优先级，因而可以保证能够获得处理器时间。其主要功能是
 检查所有标准演示任务是否仍在运行。如果
 在演示任务中发现任何意外行为，检查任务将
 把错误写入 LCD （通过 LCD 任务） （可以通过删除 UART0 上的环回连接器，
 并故意生成错误来测试
 此机制）。如果所有演示任务
 都执行其预期行为，则检查任务会将 PASS
 和最大抖动时间一起写入 LCD（还是通过 LCD 任务） ，
 如上所述。

如果正确执行，该演示应用程序将实现以下效果：

* 标记为 LED1、LED2 和 LED3 的 LED 由 'flash' 任务控制。每个 LED 将以恒定频率闪烁，LED1 的频率最高，
 LED 3 的频率最低。
* LED4 由标准 ComTest Tx 任务控制。每当 ComTest Tx 任务通过
 RS232 移植传输字符时，LED4 将进行切换。
* “检查”任务将每 5 秒向显示器写入 'PASS' 和抖动时间（以纳秒为单位）。

---

### RTOS 配置和使用详情

#### RTOS 移植专用配置

这些演示的特定配置项位于 FreeRTOS/Demo/CORTEX_STM32F103_IAR/FreeRTOSConfig.h 中。可编辑
本文件中定义的常量，以适配您的应用程序。特别是以下常量：

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
并且提供了以不同方式指定优先级的库函数。例如，在 STM32 上，您可以在 ST 驱动程序库调用中指定的最低优先级
实际上是 15，可以指定的最高优先级是 0。这是由
FreeRTOSConfig.h 中的常量 configLIBRARY_KERNEL_INTERRUPT_PRIORITY 定义的。

每个移植都将 'BaseType_t' 定义为该处理器的最有效数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档进行编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。

请注意，portEND_SWITCHING_ISR() 将启用中断。

#### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_STM32F103_IAR/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1 以使用抢占式内核或
设置为 0，以使用协同式内核。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

#### 内存分配

Source/Portable/MemMang/heap_2.c 位于 ARM Cortex-M3 演示应用程序项目中，
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
