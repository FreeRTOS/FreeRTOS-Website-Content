---
title: "FreeRTOS 空闲任务"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: 任务优先级
    link: /Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities
---

[[有关任务的更多信息……](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview)]

[FreeRTOS 教程书](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book)
提供了关于任务及其行为的额外详细信息。


### 空闲任务

RTOS 调度器启动时，自动创建空闲任务，以确保始终
存在一个能够运行的任务。它以最低[优先级](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities)创建， 
以确保如果有更高的优先级应用程序任务处于准备就绪[状态](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/02-Task-states)，则不使用任何 CPU 时间。

空闲任务负责释放 [RTOS](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 分配给 
已删除任务的内存。因此，在 
使用 [vTaskDelete()](/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete) 函数来确保闲置任务不会匮乏处理时间的应用程序中， 
这很重要。
空闲任务没有其他激活函数，因此可以在所有其他条件下合理地缺乏微控制器时间 
。

应用程序任务可以共享空闲任务优先级 (tskIDLE_PRIORITY)。
请参阅 configIDLE_SHOULD_YIELD [配置参数](/Documentation/02-Kernel/03-Supported-devices/02-Customization)，
了解如何配置该行为。


---

### 空闲任务钩子

空闲任务钩子是在空闲任务的每个周期中调用的函数。如果希望应用程序 
函数以空闲优先级运行，则有两个选择：

1. 在空闲任务钩子中实现此函数。

   必须始终有至少一个任务已准备好运行。因此，必须确保钩子 
   函数不调用任何可能导致空闲任务阻塞的 API 函数（例如，vTaskDelay()，或
   具有阻塞时间的[队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues)或[信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores)函数）。协程 
   可以在钩子函数内阻塞。

2. 创建空闲优先级任务以实现该函数。

   这是一种更灵活的解决方案，但具有更高的 RAM 使用开销。

有关使用空闲钩子的更多信息，请参阅[嵌入式软件应用程序设计](/Why-FreeRTOS/Features-and-demos/RAM_constrained_design_tutorial/Real-time-application-design)部分
。


要创建一个空闲钩子：

1. 在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization)中将 configUSE_IDLE_HOOK 设置为 1。
2. 定义具有以下名称和原型的函数：`void vApplicationIdleHook( void );`

通常使用空闲钩子函数将微控制器 CPU 设为节能模式。
