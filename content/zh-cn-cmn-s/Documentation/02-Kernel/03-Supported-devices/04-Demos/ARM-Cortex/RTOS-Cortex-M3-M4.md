---
title: "在 ARM Cortex-M Core 上运行 RTOS"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [另请参阅[调试 Cortex 硬故障异常](Debugging-Hard-Faults-On-Cortex-M-Microcontrollers.md)]。

**注意：**此页面上有关中断嵌套的信息适用于 
使用 Cortex-M3、Cortex-M4、Cortex-M4F、Cortex-M7、Cortex-M33 和 Cortex-M23 时。不适用 
于不包含 BASEPRI 寄存器的 Cortex-M0 或 Cortex-M0+ 核心。

### 简介

数以千计的应用程序在 ARM Cortex-M 核心上运行 FreeRTOS。但很少有用户
针对 RTOS 和 ARM Cortex CPU 核心这一组合请求技术支持。大多数出现的问题
都是中断优先级设置不正确
导致的。这可能是意料之中的，
因为尽管 ARM Cortex-M 核心使用的中断模型非常强大，
但对于那些习惯了常规中断优先级方案的工程师来说，这种模型有些笨拙和
有悖直觉。本页旨在描述 ARM Cortex-M 的中断优先级机制，以及如何
与 RTOS 内核一起使用。

请记住，虽然 ARM Cortex-M3 核心强加的优先级方案似乎比较复杂，
但是每个官方 FreeRTOS 移植都配有一个正确配置的演示应用程序，
可作为参考。此外，FreeRTOS V7.5.0 还引入了 
额外的 configASSERT() 调用，专门用于捕获配置错误的 ARM Cortex-M 中断控制器 (NVIC)。
***请确保在开发过程中定义了 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
。***

### 可用的优先级

### 
 Cortex-M 硬件详情

首先要知道的是，可用优先级的总数是
由实现定义的，换言之，是由使用 ARM Cortex-M 核心的微控制器制造商
所定义的。因此，
并非所有 ARM Cortex-M 微控制器都提供相同数量的唯一
中断优先级。

ARM Cortex-M 架构自身允许最多 256 个不同的优先级（最多有 8 个
优先级位，因此从 0 到 0xff 的优先级都是可能的），但绝大多数使用 ARM Cortex-M 核心的微控制器
仅允许使用其中一部分。例如， TI Stellaris
Cortex-M3 和 ARM Cortex-M4 微控制器实现 3 个优先级位，提供
了 8 个唯一的优先级值。另一个例子是，NXP LPC17xx ARM Cortex-M3 微控制器
实现 5 个优先位，提供了 32 个唯一的优先级值。

如果您的项目包含 CMSIS 库头文件，请检查 __NVIC_PRIO_BITS 定义
来查看可用的优先级位数。

### 
 使用 RTOS时的相关性

RTOS 的中断嵌套方案将可用的中断优先级分为
两组：一组将被 RTOS 临界区屏蔽，另一组
永远不会被 RTOS 临界区屏蔽，因此始终处于启用状态。两个组之间的边界由
[FreeRTOSConfig.h 中的 configMAX_SYSCALL_INTERRUPT_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) 设置
定义。此设置的最佳值将取决于
微控制器中实现的优先级位数量。

### 抢占优先级和子优先级

### 
 Cortex-M 硬件详情

8 位优先级寄存器分为两个部分：抢占优先级和
子优先级。分配给每个部分的位数是可配置的。抢占优先级
定义了一个中断是否可以抢占另一个正在执行的
中断。当两个抢占优先级相同的中断同时发生时，
子优先级决定首先执行哪个中断。

### 
 使用 RTOS时的相关性

建议将所有优先级位都指定为抢占优先级位，
不保留任何优先级位作为子优先级位。任何其他配置都会
使 configMAX_SYSCALL_interrupt_PRIORITY 设置与
分配给各个外设中断之间的直接关系复杂化。

大多数系统的默认配置都是所需要的，
STM32 驱动器库除外。**如果使用的是带有 STM32 驱动程序库的 STM32
，则在启动 
RTOS 之前，通过
调用 NVIC_PriorityGroupConfig( NVIC_PriorityGroup_4 )，确保将所有优先级位分配为抢占式优先级位。**

### 数值优先级值与逻辑优先级设置之间的反转关系

### 
 Cortex-M 硬件详情

还要知道，在 ARM Cortex-M 核心中，优先级的数值越小，
则中断的逻辑优先级越高。例如，一个
数值优先级被分配为 2 的中断的逻辑优先级高于一个
数值优先级被分配为 5 的中断。换句话说，优先级为 2 的中断的优先级高于
优先级为 5 的中断，虽然数字 2 比数字 5 要小。
为了更清楚地说明这点：一个数值优先级为 2 的中断可以中断（嵌套）
一个数值优先级为 5 的中断；但数值优先级为 5 的中断不能
中断数值优先级为 2 的中断。

这是 ARM Cortex-M 中断优先级机制中最有悖直觉之处，
因为这与大多数未使用 ARM Cortex-M3 的微控制器架构相反。

### 
 使用 RTOS 时的相关性

以 "FromISR" 结尾的 FreeRTOS 函数是中断安全的，但前提是
调用这些函数的中断的逻辑优先级不高于
configMAX_SYSCALL_INTERRUPT_PRIORITY 定义的优先级（[configMAX_SYSCALL_INTERRUPT_PRIORITY
 在 FreeRTOSConfig.h 头文件中定义](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)）。
因此，对于任何使用一个 RTOS API 函数的中断服务程序，
必须为其手动设置为一个数值优先级，
这个值必须等于或**大于** configMAX_SYSCALL_INTERRUPT_PRIORITY 设定
的值。这确保了中断的逻辑优先级等于或小于 configMAX_SYSCALL_INTRUPT_PRIORITY
设置。

Cortex-M 中断的默认数值优先级为 0。0 是最高的
优先级。因此，**切勿将使用中断安全 RTOS API
 的中断的优先级设置为默认值**。

### Cortex-M 内部优先级表示

### 
 Cortex-M 硬件详情

ARM Cortex-M 核心将中断优先级值存储在
其 8 位中断优先级寄存器的最高有效位中。例如，如果
一个 ARM Cortex-M 微控制器仅实现 3 个优先位，
那么这 3 个位分别向上移位为位 5、6 和 7。位 0 到
位 4 可以取任何值，但为了将来的验证和最大兼容性，应将它们
设置为 1。

ARM Cortex-M 内部表示如下图所示。

![Cortex-M 中断优先级寄存器显示实现的位](/media/2018/cortex-m-priority-register.png)

 Cortex-M 优先级寄存器的空间最多可容纳 8 个优先级位。
 例如，如果微控制器仅实现 3 个位，则
 使用的是 3 个最高有效位。

![将值 5 存储在实现 3 个优先级位的 ARM Cortex-M 核心中](/media/2018/used-cortex-m-priority-register.png)

 上图展示了值 5（二进制 101）是如何存储在
 实现 3 个优先位的微控制器的优先级寄存器中的。
 该图演示了为什么当 3 个位移到所需位置而其余位设置为 1 时，
 值 5 （二进制 0000 0101）也可以被认为
 是 191 （二进制 1011 1111）。

![将值 5 存储在实现 4 个优先级位的 ARM Cortex-M 核心中](/media/2018/cortex-m-priority-register-4-bits.png)

 上图展示了值 5（二进制 101）是如何存储在
 实现 4 个优先位的微控制器的优先级寄存器中的。
 该图演示了为什么当 4 个位移到所需位置而其余位设置为 1 时，
 值 5 （二进制 0000 0101）也可以被认为
 是 95 （二进制 0101 1111）。

### 
 使用 RTOS时的相关性

如上所述，
使用 RTOS API 中断服务程序的逻辑优先级需要等于或低于
configMAX_SYSCALL_INTRUPT_PRIORITY 的设置（逻辑优先级越低，则优先级数值
越大）。

CMSIS 和各微控制器制造商提供库函数，可用于
设置中断的优先级。一些库函数要求
在 8 位字节的最低有效位中指定中断优先级，
也有另一些库函数要求要指定的中断优先级已经
移到了 8 位字节的最高有效位中。查看被调用函数的文档来确定
您需要的是哪一个。如果这里出了错，会导致
意料之外的行为。

configMAX_SYSCALL_INTERRUPT_PRIORITY 和 configKERNEL_INTERRUPT_PRIORITY 位于
FreeRTOSConfig.h 中，需要按照 ARM Cortex-M 核心的要求
为它们指定优先级值，即将优先级位移到
最高有效位。这就是
为什么
在每个官方 FreeRTOS 演示配套的 FreeRTOSConfig.h 头文件中，应该具有最低的中断优先级的 configKERNEL_interrupt_PRIORITY 被设置为 255（二进制 1111 1111）。
采用上述方式来指定这些值有许多原因：RTOS 内核直接访问 ARM Cortex-M3 硬件
（无需通过任何第三方库函数），RTOS 内核的实现
早于大多数库函数的实现，
并且最早的 ARM Cortex-M3 库面世时也使用了此方案。

### 临界区

### 
 Cortex-M 硬件详情

RTOS 内核使用 ARM Cortex-M 核心的 BASEPRI 寄存器
来实现临界区。因此，RTOS 内核能够仅屏蔽一部分中断，
从而提供灵活的中断嵌套模型。

BASEPRI 是一个位掩码。为 BASEPRI 设置为一个值后，它可以屏蔽所有逻辑优先级等于
或低于该值的中断。因此，无法使用 BASEPRI 来
屏蔽优先级为 0 的中断。

题外话：可以从中断中安全调用的 FreeRTOS API 函数
使用 BASEPRI 来实现中断安全临界区。进入临界区时，
BASEPRI 的值设置为 configMAX_SYSCALL_interrupt_PRIORITY，
退出临界区时，设置为 0。我们收到许多故障报告
认为 BASEPRI 应在退出临界区时返回到原始值，而不仅仅是设置为 0，
但是 Cortex-M NVIC 绝不会接受一个优先级低于当前正在执行的中断的优先级的中断，
不管 BASEPRI 设置为多少。一个总是
将 BASEPRI 设置为 0 的实现执行代码的速度比一个
存储然后恢复 BASEPRI 值的实现更快
（编译器的优化器打开的情况下）。

### 
 使用 RTOS 内核时的相关性

RTOS 内核通过将 configMAX_SYSCALL_INTRUPT_PRIORITY 的值
写入 ARM Cortex-M BASEPRI 寄存器来创建临界区。因为 BASEPRI 无法屏蔽
优先级为 0 的中断（最高的优先级），
所以不得将 configMAX_SYSCALL_INTERRUPT_PRIORITY 设置为 0。

