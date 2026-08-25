---
title: FreeRTOS FAQ - 内存使用、启动时间与上下文切换时间
created: 2018-09-20 00:00:00.0 UTC
description: FreeRTOS 内存使用、启动时间与上下文切换时间相关的信息
---

## FreeRTOS 占用多少 RAM？

这取决于您的应用程序。以下指南基于：

- IAR STR71x ARM7 移植。
- 全面优化。
- 最低配置。
- 四种优先级。

| **项目**                       | **使用的字节**                                                            |
| ------------------------------ | ------------------------------------------------------------------------- |
| 调度器自身               | 236 字节（很容易通过使用较小的数据类型降低）。            |
| 每创建一个队列，会增加 | 76 字节和队列存储区域（请参阅常见问题：为什么队列占用这么多 RAM？）  |
| 每创建一个任务，会增加  | 64 字节（包括任务名称使用的 4 个字符）和任务堆栈大小。 |


## FreeRTOS 使用了多少 ROM/Flash？

这取决于您的编译器、系统架构和 RTOS 内核配置。

RTOS 内核本身在下列情况下使用大约 5 - 10 KB 的 ROM 空间：
使用与常见问题“FreeRTOS 占用多少 RAM？”中相同的配置时。


## FreeRTOS 启动需要多久？

FreeRTOS、OPENRTOS 和 SAFERTOS（大部分情况下）作为源代码提供，用于静态链接到用户应用程序
。因此构建流程会生成单个可执行的二进制映像。通常，
这样的映像会包括 C 启动例程，以在调用 main() 来执行用户应用程序之前，设置 C 运行时间环境
。中断向量表也将静态配置，
包含于相同二进制内预先确定的位置。

下表说明了启动此类系统所需的处理引导顺序，
以及与完成此处理所需时间相关的一些指导。请注意，提供的任何数字
真实但仅供参考。可实现的实际时间将取决于所使用的架构、
配置的时钟频率以及内存接口的配置。

1. 根据要求的性能级别配置 CPU 时钟。

   通常需要几次寄存器写入操作，随后短暂延迟以便时钟锁定。这将需要
   大约几微秒，取决于所使用的架构。该步骤是可选的。
   它可以稍后从 C 代码执行，但如果它在初始化内存之前执行，则会增加启动时间
   。

2. 初始化仅包含 0 值 (bss) 的静态变量和全局变量。

   在应用中包含 FreeRTOS 通常只会额外添加数百个写入访问，
   这些访问操作在非常紧密的汇编循环中执行。与不包括
   RTOS 内核的情况相比，这将增加几微秒的时间。

3. 初始化包含非零值的变量。

   在应用程序中包含 FreeRTOS 通常不会为此步骤增加任何额外的时间。

4. 执行其他所需的硬件设置。

   通常需要在启动 RTOS 调度器之前配置外围设备。这需要多长时间
   取决于所使用外设的复杂程度，但在
   FreeRTOS 所针对的微控制器类别上，总时间通常只需要几毫秒。

5. 创建应用程序队列、信号量和互斥锁。

   通常，大多数队列、信号量和互斥锁会在 RTOS 调度器启动之前创建
   。举例来说，在 ARM Cortex-M3 设备上，使用 ARM RVDS 编译器，并将优化
   设置为 1（低），则创建队列、信号量或互斥锁需要大约 500 个 CPU 周期。

6. 创建应用程序任务。

   通常大多数任务会在 RTOS 调度器启动之前创建。例如，
   在 ARM Cortex-M3 设备上，使用 ARM RVDS 编译器，并将优化设置为 1（低），
   则创建每个任务大约需要 1100 个 CPU 周期。

7. 启动 RTOS 调度器。

   通过调用 vTaskStartScheduler() 启动 RTOS 调度器。启动过程包括配置
   tick 中断、创建空闲任务，然后恢复要运行的第一个任务的上下文。例如，
   在 ARM Cortex-M3 设备上，使用 ARM RVDS 编译器，并将优化设置为 1（低），
   则启动 RTOS 调度器需要大约 1200 个 CPU 周期。


## 上下文切换时间是多少？

上下文切换时间取决于移植、编译器和配置。在下列测试条件下，
获得的是 84 个 CPU 周期的上下文切换时间：

- 支持 Keil 编译器的 FreeRTOS ARM Cortex-M3 移植
- 堆栈溢出检查已关闭
- 跟踪功能已关闭
- 运行时统计功能已关闭
- 编译器已设置为优化速度
- [configUSE_PORT_OPTIMISED_TASK_SELECTION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_port_optimised_task_selection) 在
  FreeRTOSConfig.h 中设置为 1

注意：

- 在这些测试条件下，上下文切换时间不取决于是
  选中不同的任务用于运行，还是选中相同的任务继续运行。

- ARM Cortex-M 移植在 PendSV 中断中执行所有任务上下文切换。引用的时间
  不包括进入中断的时间。

- 引用的时间包括一小段 C 代码。已经确定以程序集代码提供整个实现
  本可以节省 12 个 CPU 周期。人们认为
  维护一小段通用 c 代码（为了跟踪等功能的维护、支持、稳健性、
  自动纳入等原因）的好处大于从上下文切换时间中扣除 12 个 CPU 周期的好处
  。

- 进入中断时未自动保存的 Cortex-M CPU 寄存器可以通过
  单一程序集指令保存，然后使用另一个单一程序集指令再次恢复。这
  两个指令各消耗 12 个 CPU 周期。


## 为什么我的编译器告诉我 FreeRTOS 正在使用所有可用的 RAM？

[内存分配方案示例](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)中有三种方案
（由 FreeRTOS 提供）从静态分配的数组分配内存。
该数组的大小由 FreeRTOSConfig.h 中的 [configTOTAL_HEAP_SIZE](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtotal_heap_size) 常量决定。这些只是
正常静态分配的数组，因此出现在许多工具链提供的 RAM 使用数据中
。工具链实际上将堆显示为已消耗 RAM，但此时堆
完全空闲，因为实际上并没有为它分配内存。

C 应用程序需要一些 RAM 用于静态变量、缓冲区等，但它们很少使用
微控制器上可用的所有 RAM 。许多 FreeRTOS 演示应用程序将堆的大小设置为
可以用完剩余的所有 RAM，使得看起来似乎应用程序正在占用所有的可用 RAM。


## 为什么队列占用这么多 RAM？

队列内置了事件管理功能。这意味着队列数据结构体包含
其他 RTOS 系统有时会单独分配的所有 RAM。在
FreeRTOS 内部没有事件控制块的概念。


## 如何减少 RAM 占用量？

- [FreeRTOS-Plus-Trace](/Documentation/03-Libraries/02-FreeRTOS-plus/05-FreeRTOS_plus_Trace/00-FreeRTOS_Plus_Trace) 可以跟踪内存
  分配和内存空闲事件，因此在分析并优化内存使用方面很有用。

- 大多数情况下，[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)可用于取代二进制信号量
  。二进制信号量是需要创建的通用对象，
  而直达任务通知直接发送到任务，不使用任何 RAM。

- [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)中的每个标志（位）可用作
  [二进制信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)，因此将多个二进制信号量替换为单一事件组
  。

- 使用 [uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)   函数查看哪些任务可以分配到较小的堆栈。

- 使用 xPortGetFreeHeapSize() 和（适用时）xPortGetMinimumEverFreeHeapSize() API 函数
  来查看多少 FreeRTOS 堆已分配但从未使用，并
  相应地调整[。](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtotal_heap_size)

- 如果正在使用 [heap_1.c、heap_2.c、heap_4.c 或 heap_5.c](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)，
  而且应用程序的任何内容都没有直接调用 malloc()（而非 pvPortMalloc()），
  则确保 C 链接器未分配到堆，因为此堆将永远不会使用。

- 将 configMAX_PRIORITIES 和 configMINIMAL_STACK_SIZE（位于 portmacro.h 中）设置为应用程序可接受的最小值
  。

- 恢复 main() 使用的堆栈。一旦启动 RTOS 调度器，则不需要程序进入时使用的堆栈
  （除非应用程序调用 vTaskEndScheduler() 函数。此函数仅在
  PC 和 Flashlite 移植中发布时得到直接支持，或者与 ARM Cortex-M 和 RX 移植一样，将堆栈作为中断堆栈使用）
  。每个任务自己的堆栈都已分配，因此
  分配给 main() 的堆栈在 RTOS 调度器启动后可复用。

- 尽可能减少 main() 使用的堆栈。创建第一个应用程序任务时将自动创建空闲任务
  。因此，程序进入时（在 RTOS 调度器启动之前）使用的堆栈必须足够大，
  以便嵌套调用
  xTaskCreate()（或 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)）。
  手动创建空闲任务可以减少一半的堆栈要求。手动创建空闲任务：

  1. 在 Sourcetasks.c 中找到 prvInitialiseTaskLists() 函数。
  2. 该函数在底部调用 xTaskCreate() 创建空闲任务。从
     Sourcetasks.c 剪切此行，并将其粘贴到 main() 函数中。

- 合理安排任务数量。在下列情况下不需要空闲任务：

  1. 应用程序有一个从不阻塞的任务，并且
  2. 应用程序没有调用 vTaskDelete()。

- 减少定义 BaseType_t 使用的数据大小（这可能会增加执行时间）。

- 还可以进行其他小调整（例如，任务优先级队列不需要事件管理），
  但如果您达到这个级别，您需要更多 RAM！


## 为什么我的编译器告诉我 FreeRTOS 使用的 ROM 远多于声称需要的 ROM？

此前引用的 ROM/Flash 占用数据是真实的。如果您编写了一个小型 FreeRTOS 测试程序，而且此程序
似乎消耗了比预期更多的 ROM，那么这可能是因为您的构建中的库，
而不是因为 FreeRTOS。特别是 GCC 字符串处理和任何浮点库
将增加您的代码量。

FreeRTOS 在名为 printf-stdarg.c 文件中包含许多字符串处理函数的精简开源实现
。将此文件纳入项目可以大大减少构建使用的 ROM，
以及需要分配给调用字符串处理库的任何任务（例如sprintf()）的堆栈大小
。注意，printf-stdarg.c 为开源，但不涵盖于 FreeRTOS
许可证中。在使用之前，请确保您可以接受文件本身所规定的许可条件。

此外，多数链接器会默认删除未使用的代码，但 GNU 链接器仅会在您明确告知的情况下删除未使用的代码
。

查看输出的 .map 文件，找到 ROM/Flash 准确的用途。


## 如何向任务分配 RAM？

如果使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) API 函数创建任务，
那么任务所需的 RAM 由应用程序编写者提供，
并且不会分配内存。

如果使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/) API 函数创建任务，
那么任务所需的 RAM 会在 xTaskCreate() API 函数中从
[FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)分配。

main() 使用的堆栈不被任务使用，但（取决于移植）可能由中断使用。


## 如何向队列分配 RAM？

如果使用 [xQueueCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic) API 函数创建队列，
那么队列所需的 RAM 由应用程序编写者提供，
并且不会分配内存。

如果使用 [xQueueCreate()](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate) API 函数创建队列，
那么队列所需的 RAM 会在 xQueueCreate() API 函数中从
[FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)分配。


## 任务堆栈应该多大？

任务可通过使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/)
或 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
API 函数创建。函数的 usStackDepth 参数指定了将为正在创建的任务分配的堆栈大小
（单位为词，而非字节！）。人们通常会询问如何确定
usStackDepth 值，但除了下文所述的一种方法以外，
确定使用 RTOS 时需要多少堆栈与确定编写裸机应用程序（不使用操作系统的应用程序）时需要多少堆栈并无多大区别
。

与编写裸机应用程序时完全相同，所需的堆栈大小取决于
以下应用程序特定的参数：

- 函数调用嵌套深度
- 函数作用域变量声明的数量和大小
- 函数参数的数量
- 处理器架构
- 编译器
- 编译器优化级别
- 中断服务程序的堆栈要求——对于许多 RTOS 移植来说是零，因为 RTOS
  在进入中断服务程序时会切换为使用专用中断堆栈。

每当调度器暂停运行当前任务，以运行不同的任务时，
处理器上下文都会保存到当前任务的堆栈上。下次该任务运行时，保存的处理器上下文会从该任务的堆栈中弹出
。保存处理器上下文所需的堆栈空间
是 RTOS 自身对任务堆栈要求以外的唯一额外堆栈要求。

尽管难以确定要为任务分配多少堆栈，但 RTOS 会提供功能，
以便采用务实的试错方法来调整任务的堆栈大小；
[uxTaskGetStackHighWaterMark()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)
API 函数可以用于查看实际的堆栈使用量，允许在分配的堆栈超出必要大小时减少堆栈大小，
而[堆栈溢出检测](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking)
功能可以用于确定堆栈是否太小。此外，所有 RTOS 任务使用的堆栈
可以通过
[uxTaskGetSystemState()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/01-uxTaskGetSystemState)
API 函数，或者众多 FreeRTOS 感知 IDE 插件的其中一个同时查看。

FreeRTOS 下载文件包含每种移植的演示应用程序，而每个演示应用程序提供的 FreeRTOSConfig.h 文件
定义一个名为 [configMINIMAL_STACK_SIZE](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configminimal_stack_size) 的常量。
强烈建议分配给任务的堆栈不要小于
在移植演示应用程序中使用的 configMINIMAL_STACK_SIZE 设置。

另请参阅 [Erich Styger 关于使用 GNU 堆栈分析工具的博客文章](http://mcuoneclipse.com/2015/08/21/gnu-static-stack-usage-analysis/)。
