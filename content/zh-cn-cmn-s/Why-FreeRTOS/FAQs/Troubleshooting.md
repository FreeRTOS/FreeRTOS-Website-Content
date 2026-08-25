---
title: 在查看常见问题之前……
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 对基于 FreeRTOS 的应用程序进行故障诊断
---

有关[“我的应用程序无法运行，问题可能出在哪里？”](#freertos-常见问题我的应用程序无法运行问题可能出在哪里)这一常见问题，
请参阅下文。但是在查看此常见问题之前，不妨先查阅以下实用提示。


## ARM Cortex-M MCU 用户注意事项

大多数关于 ARM Cortex-M 微控制器的支持请求
都与中断优先级分配不正确导致的问题有关。自 FreeRTOS V7.5.0 起，系统内置了 configASSERT() 调用，以捕获
这种常见用户错误的来源。请确保已在开发过程中对 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) 进行定义。

此外，我们还提供了以下两项在线资源：

1. [专门](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)
   介绍 ARM Cortex-M 中断行为及其与中断嵌套相关 FreeRTOSConfig.h 设置关系的
   页面。

2. 介绍如何调试 ARM Cortex-M [硬故障异常](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Others/Debugging-Hard-Faults-On-Cortex-M-Microcontrollers)的页面。


## 关于 configASSERT() 的说明

[configASSERT() 宏](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)可用于捕获用户错误。请确保
已在 FreeRTOS 应用程序开发或调试过程中对 configASSERT() 进行定义。


## 其他帮助资源

如果阅读此常见问题页面后，您的问题依然没有得到解决，请使用其他支持资源，
包括[快速入门指南](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide)（其中会附有
FreeRTOS.org 网站上各种实用页面的链接）以及[官方支持系统](https://forums.freertos.org/)。


## FreeRTOS 常见问题：我的应用程序无法运行，问题可能出在哪里？

虽然我不了解您的应用程序的具体情况，但以下是一些常见解决方案：


### 创建的应用程序可以编译，但无法运行

所有官方 FreeRTOS 移植都会随附相应的官方演示，
该演示（至少在创建时）无需任何修改即可在开发所使用的硬件平台上编译和执行。
之所以提供演示项目，是为了确保新用户可以在最短时间内上手使用 FreeRTOS，
最大限度地降低学习和探索成本。强烈建议，在创建新的 FreeRTOS 项目时，
从提供的任一预配置演示入手， 然后对其进行适配。这种做法
可以确保新项目包含所有必要的源文件和头文件，并安装必要的
中断服务程序，从而节省项目创建者的精力。

如果创建的项目可以编译，并且至少执行到调度器已启动的状态，
但在调用
[vTaskStartScheduler()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/03-vTaskStartScheduler) 后，只有一项任务在执行，或者根本没有任务在执行，
很可能是因为中断向量表出现问题。

所有 FreeRTOS 移植都使用定时器中断，部分 FreeRTOS 移植使用多个中断。请参考
提供的演示项目。

**ARM Cortex-M 用户特别注意事项：**ARM Cortex-M3、ARM Cortex-M4 和 ARM Cortex-M4F 移植要求
在 SysTick、PendSV 和 SVCCall 中断向量上安装 FreeRTOS 处理程序。可以
将 FreeRTOS 定义的 xPortSysTickHandler()、xPortPendSVHandler()
和 vPortSVCHandler() 函数直接填入向量表的对应位置，或者如果中断向量表符合 CMSIS 标准，
可以在 FreeRTOSConfig.h 中添加以下三行代码，以将 FreeRTOS 函数名称映射到
其 CMSIS 等效函数名称：

```c
#define vPortSVCHandler SVC_Handler
#define xPortPendSVHandler PendSV_Handler
#define xPortSysTickHandler SysTick_Handler
```

这种方式仅在开发工具提供的默认处理程序
定义为[弱符号](http://en.wikipedia.org/wiki/Weak_symbol)时有效。如果默认处理程序
未被定义为弱符号， 则需要将其注释掉或删除。


### 任务堆栈

[另请参阅
[uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)
API 函数和
[堆栈溢出检测](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking)选项]。目前，请求支持最常见的原因就是
堆栈溢出。任务可用堆栈的大小是通过
xTaskCreate() 的 usStackDepth 参数
或者 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
API 函数来设置的。

对于导致问题的任务，不妨尝试增加为其分配的堆栈空间，
或减少任务使用的堆栈量。请勿编写需要大量堆栈的
中断服务程序。

能够调用任意字符串格式化函数的任务可能需要大量堆栈，
使用 GCC 编译器时更是如此。此类任务很容易发生堆栈溢出。

创建任务时，每个任务堆栈的字节都会设置为 0xa5，因此比较容易
发现是否发生堆栈溢出。此外，tasks.c 中的 usTaskCheckFreeStackSpace() 函数
演示了如何在运行时检查堆栈使用情况（不过此函数效率较低，
因此应仅用于调试）。


### main() 堆栈

FreeRTOS 调度器启动后，
只有 RTOS 任务和中断才有上下文，main() 的上下文将不复存在。出于此原因，为最大限度地提高 FreeRTOS 应用程序可以使用的 RAM，
在 C 标准允许的情况下，部分 FreeRTOS 移植
会重新使用分配给 main() 的堆栈，将其作为系统堆栈或中断堆栈。因此，
绝对不要在 main() 使用的堆栈上分配 FreeRTOS 应用程序需要或能够以任何方式访问的变量或缓冲区，
因为它们很可能会被覆盖。


### 中断不执行

首先，请确认问题是否与 FreeRTOS 有关，方法为
在不使用 FreeRTOS 的简单基础应用程序中尝试使用中断。

如果在调度器启动之前调用了 FreeRTOS API 函数，
则中断会故意保持禁用状态，直到第一项任务开始执行
才重新启用。这是为了保护系统，
因为中断会在系统初始化期间（在调度器启动之前以及调度器可能处于不一致状态时）尝试使用 FreeRTOS API 函数，
这可能导致崩溃，
从而对系统产生影响。

更改微控制器中断启用位或优先级标志时，
请勿使用除调用 taskENTER_CRITICAL() 和 taskEXIT_CRITICAL() 以外的任何方法。
这些宏会记录调用的嵌套深度，以确保中断
只有在所有的嵌套调用都结束（计数归零）时
才会重新启用。请注意，某些库函数可能会自行启用和禁用
中断。


### 我在演示中添加了一项简单任务，但现在演示崩溃了！

创建任务时，
需要从[内核堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)获取内存。
许多演示应用程序项目将堆的大小设置为刚好能够运行演示任务，
因此没有足够的空间来添加更多任务。
启动 RTOS 调度器时，会自动创建空闲任务。如果堆的大小不够用于创建空闲任务，
则 vTaskStartScheduler() 将返回，导致应用程序根本无法启动。

要解决此问题，可以[增加堆空间](/Documentation/02-Kernel/03-Supported-devices/02-Customization)，
或删除一些演示应用程序任务。


### 在中断中使用 API 函数

除非 API 函数的名称以 "...FromISR()" 结尾，
否则请勿在中断服务程序中使用。

**ARM Cortex-M3、ARM Cortex-M4 和 ARM Cortex-M7 用户：请注意，
95% 针对 ARM Cortex-M 设备的支持请求都与这一问题有关：**

（另有[单独页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)
专门介绍 ARM Cortex-M 中断优先级，并全面介绍如何设置 ARM Cortex-M 中断优先级，
以用于强大的 FreeRTOS 中断嵌套模型。）

如果中断的优先级高于通过 configMAX_SYSCALL_INTERRUPT_PRIORITY 设置的优先级，
则无法通过此中断调用 API 函数。设置中断优先级时，
请注意以下几点：

* configMAX_SYSCALL_INTERRUPT_PRIORITY 在 FreeRTOSConfig.h 中定义。在 ARM Cortex-M3 设备上，
  中断优先级数值越低，逻辑上优先级越高。请务必为中断分配优先级，
  否则将默认其优先级为 0。0 代表最高优先级，
  高于 configMAX_SYSCALL_INTERRUPT_PRIORITY。

* 指定优先级时务请小心，因为不同的 ARM Cortex-M3 实现
  使用不同数量的优先级位。

* ARM Cortex-M3 内部使用字节的 'n' 个最高有效位来表示中断优先级，
  其中 'n' 是由如上所述的实现定义的。ARM 和各种 ARM Cortex-M3 被许可方
  提供了允许分配中断优先级的库函数，
  有些库函数要求在调用前将优先级移到最高有效位，
  而其他库函数则在内部执行移位操作。

* 定义中断优先级的位通常分为两部分：代表抢占优先级的位
  和代表子优先级的位。为保证最大程度的简洁性和兼容性，请确保
  将所有优先级位都指定为“抢占式优先级”位。


### RTOS 调度器在尝试启动第一项任务时崩溃

如果您使用的是 ARM7 目标板，则处理器在启动 RTOS 调度器时
必须处于监督模式。


### 中断启用标志设置不正确

在启用或禁用中断时，
请勿使用除调用 portENTER_CRITICAL() 和 portEXIT_CRITICAL() 以外的任何方式。这些宏会记录调用的嵌套深度，
以确保中断只有在所有的嵌套调用都结束（计数归零）时才会重新启用。

如果在调度器启动之前调用了 FreeRTOS API 函数，则大部分 FreeRTOS 移植
会故意禁用中断，直到第一项任务开始执行才重新启用。这是
为了保护系统，因为中断会在系统初始化期间（调度器启动之前）尝试使用 FreeRTOS API 函数，
这可能导致崩溃，从而对系统产生影响。


### RTOS 调度器还未启动，应用程序就已崩溃

RTOS 调度器启动之前，无法进行上下文切换。因此，
任何可能导致上下文切换的中断服务程序
都不能在 RTOS 调度器启动之前执行。同样，任何试图向队列发送数据或从队列接收数据，或者操作信号量的中断服务程序
也不能在调度器启动之前执行。

许多 API 函数都不能在 RTOS 调度器启动之前调用。最好
将这些函数的使用限制在创建任务、队列和信号量上，这些资源在 RTOS 调度器开始运行后
即会被使用。


### 挂起 RTOS 调度器（调用 vTaskSuspendAll()）引发问题

在 RTOS 调度器挂起时，请勿调用 API 函数。有些函数可以使用，
但并非所有函数都能使用。挂起机制并非针对此目的而设计。


### 我创建的新应用程序无法编译

请基于所使用移植配套的演示项目文件来创建新的应用程序。这样
可确保包含正确的文件，并正确配置编译器。


### 我卡在了 for( pxIterator = ( ListItem_t * ) &( pxList->xListEnd ); 这一行

原因可能如下：

1. 堆栈溢出：请参阅 [/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking)。

2. 中断优先级分配不正确，特别是在 ARM Cortex-M3 部件上，数值越大，实际中断优先级越低，
   这一点可能有违直觉。请前往
   [/Documentation/02-Kernel/03-Supported-devices/02-Customization/#kernel_priority](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)，参阅有关 configMAX_SYSCALL_INTERRUPT_PRIORITY 的内容。

3. 在临界区内或 RTOS 调度器挂起时调用 API 函数。


## 我还能做什么？

1. 查看下载页面上的[已知问题列表](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)
   。
2. 在[受监控的支持论坛](https://forums.freertos.org/)上发帖，描述您遇到的问题。
