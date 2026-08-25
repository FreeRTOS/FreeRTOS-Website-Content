---
title: "ST STM32 Primer ARM Cortex-M3 演示"
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
| <br /><br />![](/media/2018/STM32_Primer.jpg)<br /> |

本页介绍的 FreeRTOS 演示应用程序适用于 [STM32 Primer](http://www.stm32circle.com/)，
这是一款针对 [STMicroelectronics STM32 ARM Cortex-M3 微控制器](http://www.st.com/internet/mcu/subclass/1169.jsp)的新型评估平台。 
演示使用配备 [Raisonance Ride V7](http://www.raisonance.com/) IDE 的GCC 编译器。

演示使用来自 CircleOS 的驱动程序和其他源文件（与 FreeRTOS.org 不同，CircleOS 不是实时内核）。这些文件
是与 FreeRTOS.org 分开授权的。用户必须熟悉 [CircleOS](http://www.stm32circle.com/circleos_doc/index.html) 许可。请注意，
FreeRTOS 演示本身不是 CircleOS 应用程序，因而会在 STM32 Primer 上覆写 CircleOS。位于 
Raisonance Ride 发行版 [Program Files]RaisonanceRideLibARMCircleOS 目录下的批处理文件，可用于将 CircleOS 恢复到 STM32 Primer 硬件。

**使用 RIDE 第 7 版：**FreeRTOS V5.1.1 不能使用最新版 RIDE 库构建。位于 FreeRTOS SVN
存储库中的最新版本已修复-必要的更改将包含在下一个版本中。

**升级到 FreeRTOS V5.0.3：**FreeRTOS V5.0.3 为 ARM Cortex-M3 移植引入了 configMAX_SYSCALL_interrupt_PRIORITY 配置选项。请参阅
[RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，获取关于此功能的完整信息。

**升级到 FreeRTOS V4.8.0：**  在 V4.8.0 之前，FreeRTOS 内核未使用 SVCall 中断，从 V4.8.0 开始才使用 SVCall 中断。 
因此，要将旧项目升级到 V4.8.0 标准，需要稍微编辑一下启动代码。要执行此操作，只需
将 vPortSVCHandler () 安装到中断向量表（包含在启动源文件中）内的 SVCall 位置。包含在 
FreeRTOS 下载中的演示项目已更新，可以作为示例。

---

### *重要！关于使用 STM32 Primer ARM Cortex-M3 演示的注意事项*

*在使用此 RTOS 移植之前，请阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 下载包含所有 FreeRTOS 移植的源代码，因此包含的文件比此演示所需的多得多。
请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，了解
下载的文件和关于创建新项目的信息。

STM32F103 Primer Ride 演示的 Ride 工作区文件名为 RTOSDemo.rprj，位于 FreeRTOS/Demo/CORTEX_STM32F103_Primer_GCC 
目录中。

---

### 演示应用程序

### 演示应用程序硬件设置

演示应用程序使用内置在评估板上的 LED 和显示器，因此不需要特定的硬件设置。 

USB 接口用于直接连接 STM32 Primer 和主机。

### 构建和运行演示应用程序

将 STM32 Primer上标有“调试”的 USB 端口与主机相连。

1. 在 Ride IDE 中打开 FreeRTOS/Demo/CORTEX_STM32F103_Primer_GCC/RTOSDemo.rprj 项目。
2. 在 IDE 'Project' 菜单中选择 'Make Project'。项目应该成功构建，没有错误或警告。
3. 在IDE 'Debug' 菜单中选择 'Start'。将用新建二进制数组对微控制器闪存进行编程，而且调试器将
 在进入 main () 时中断。

该项目包括内置在二进制数组中的位图。这将导致二进制数组大小变大，并且在某些优化级别下，将使所得的二进制数组
对于微控制器闪存而言过大。如果出现该问题，则可以通过 
将 mainINCLUDE_BITMAP within main.c 定义设置为 0，轻松地将位图从构建中排除，从而减少代码大小。

### 功能

演示应用程序会创建 22 个实时任务。这些任务主要包括 
标准演示应用程序任务（请参阅  [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节， 
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
 直接访问 LCD。LCD 任务只阻塞等待
 消息的队列 - 当消息到达时唤醒。

 LCD 任务接收两种类型的消息。第一种包含用于
 在 LCD 上显示的字符串。第二种包含一条
 根据[如下](#演示应用程序硬件设置)所述的当前 MEMS 输入（MEMS 功能来自 CircleOS 演示）来更新 LCD 的指令。
* 检查任务
 检查任务每 5 秒执行一次，但
 具有最高优先级，因而可以保证能够获得处理器时间。其主要功能是
 检查所有标准演示任务是否仍在运行。如果
 在演示任务中发现任何意外行为，检查任务将
 向 LCD 写入错误（通过 LCD 任务）。如果所有演示任务
 都执行其预期行为，则检查任务会将 PASS
 和最大抖动时间一起写入 LCD（还是通过 LCD 任务） ，
 如上所述。
* Tick hook
 这是一个基本的 Tick Hook，定期向 LCD 任务发送消息，请求更新 MEMS 输入。
* 闪烁任务
 这是一项非常基本的任务，每秒钟唤醒一次，然后使 LED 闪烁。它仅用于定时验证。

如果正确执行，该演示应用程序将实现以下效果：

* 绿色 LED 由“闪烁”任务控制，每秒钟都会切换。
* MEMS 输入用于控制 LCD 上显示小球的位置。通过倾斜 STM32 Primer，小球可以围绕 LCD 移动。
 将 45% 设置为中性位置。此功能来自 CircleOS 演示，但在此情况下，它在其自主任务中执行。
* “检查”任务将每 5 秒向显示器写入 'PASS' 和抖动时间（以纳秒为单位）。

---

### RTOS 配置和使用详情

### RTOS 移植特定配置

这些演示的特定配置项位于 FreeRTOS/Demo/CORTEX_STM32F103_Primer_GCC/FreeRTOSConfig.h 中。可以编辑 
在本文件中定义的常量，以适配您的应用程序。特别是- 

* **configTICK_RATE_HZ**
 可通过该常量设置 RTOS tick 的频率。提供的数值 1000 Hz 可用于 
 测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。

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

### 中断服务程序

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档进行编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。STM32/IAR 演示中的中断驱动 UART 演示可以
用作示例。请参阅文件 FreeRTOS/Demo/CORTEX_STM32F103_IAR/serial/serial.c 获取完整示例，但请注意，
此示例仅用于演示所需机制，不应作为优化 UART 驱动程序的示例。

请注意，portEND_SWITCHING_ISR () 将启用中断。

### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTEX_STM32F103_Primer_GCC/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1 以使用抢占式内核或 0 
以使用协同式内核。请注意，当使用协同 RTOS 调度器执行时，测量其自身定时特征的演示任务可能报告错误。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_2.c 位于 ARM Cortex-M3 演示应用程序项目中， 
用于提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分， 
获取完整信息。
