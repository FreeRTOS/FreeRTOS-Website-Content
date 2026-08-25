---
title: 定制
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: 内存管理
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management/
  - title: 堆栈溢出检测
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking/

---

FreeRTOS 可通过名为 FreeRTOSConfig.h 的配置文件进行定制。所有
FreeRTOS 应用程序都必须在其预处理器的 include 路径中包含 FreeRTOSConfig.h 头文件。
FreeRTOSConfig.h 可根据正在构建的应用程序定制 RTOS
内核，因此该配置文件特定于应用程序，而不是 RTOS，并且
应位于应用程序目录中，而不是 RTOS 内核源代码
目录中。

RTOS 源代码下载内容中包含的每个演示应用程序都有自己的
FreeRTOSConfig.h 文件。一些演示相当老旧，并未包含所有
可用的配置选项。其中忽略的配置选项
会在 RTOS 源文件中设置为默认值。

以下是一个典型的 FreeRTOSConfig.h 定义，接着是
对每个参数的解释：


```c
#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/* Here is a good place to include header files that are required across
   your application. */
#include "something.h"

#define [configUSE_PREEMPTION](#configuse_preemption)                                        1
#define [configUSE_PORT_OPTIMISED_TASK_SELECTION](#configuse_port_optimised_task_selection)                     0
#define [configUSE_TICKLESS_IDLE](#configuse_tickless_idle)                                     0
#define [configCPU_CLOCK_HZ](#configcpu_clock_hz)                                          60000000
#define [configSYSTICK_CLOCK_HZ](#configsystick_clock_hz)                                      1000000
#define [configTICK_RATE_HZ](#configtick_rate_hz)                                          250
#define [configMAX_PRIORITIES](#configmax_priorities)                                        5
#define [configMINIMAL_STACK_SIZE](#configminimal_stack_size)                                    128
#define [configMAX_TASK_NAME_LEN](#configmax_task_name_len)                                     16
#define [configUSE_16_BIT_TICKS](#configuse_16_bit_ticks)                                      0
#define [configIDLE_SHOULD_YIELD](#configidle_should_yield)                                     1
#define [configUSE_TASK_NOTIFICATIONS](#configuse_task_notifications)                                1
#define [configTASK_NOTIFICATION_ARRAY_ENTRIES](#configtask_notification_array_entries)                       3
#define [configUSE_MUTEXES](#configuse_mutexes)                                           0
#define [configUSE_RECURSIVE_MUTEXES](#configuse_recursive_mutexes)                                 0
#define [configUSE_COUNTING_SEMAPHORES](#configuse_counting_semaphores)                               0
#define [configUSE_ALTERNATIVE_API](#configuse_alternative_api)                                   0 /* Deprecated! */
#define [configQUEUE_REGISTRY_SIZE](#configqueue_registry_size)                                   10
#define [configUSE_QUEUE_SETS](#configuse_queue_sets)                                        0
#define [configUSE_TIME_SLICING](#configuse_time_slicing)                                      0
#define [configUSE_NEWLIB_REENTRANT](#configuse_newlib_reentrant)                                  0
#define [configENABLE_BACKWARD_COMPATIBILITY](#configenable_backward_compatibility)                         0
#define [configNUM_THREAD_LOCAL_STORAGE_POINTERS](#confignum_thread_local_storage_pointers)                     5
#define [configUSE_MINI_LIST_ITEM](#configuse_mini_list_item)                                    1
#define [configSTACK_DEPTH_TYPE](#configstack_depth_type)                                      uint16_t
#define [configMESSAGE_BUFFER_LENGTH_TYPE](#configmessage_buffer_length_type)                            size_t
#define [configHEAP_CLEAR_MEMORY_ON_FREE](#configheap_clear_memory_on_free)                             1

/* Memory allocation related definitions. */
#define [configSUPPORT_STATIC_ALLOCATION](#configsupport_static_allocation)                             1
#define [configSUPPORT_DYNAMIC_ALLOCATION](#configsupport_dynamic_allocation)                            1
#define [configTOTAL_HEAP_SIZE](#configtotal_heap_size)                                       10240
#define [configAPPLICATION_ALLOCATED_HEAP](#configapplication_allocated_heap)                            1
#define [configSTACK_ALLOCATION_FROM_SEPARATE_HEAP](#configstack_allocation_from_separate_heap)                   1

/* Hook function related definitions. */
#define [configUSE_IDLE_HOOK](#configuse_idle_hook)                                 0
#define [configUSE_TICK_HOOK](#configuse_tick_hook)                                 0
#define [configCHECK_FOR_STACK_OVERFLOW](#configcheck_for_stack_overflow)                      0
#define [configUSE_MALLOC_FAILED_HOOK](#configuse_malloc_failed_hook)                        0
#define [configUSE_DAEMON_TASK_STARTUP_HOOK](#configuse_daemon_task_startup_hook)                  0
#define [configUSE_SB_COMPLETED_CALLBACK](#configuse_sb_completed_callback)                     0

/* Run time and task stats gathering related definitions. */
#define [configGENERATE_RUN_TIME_STATS](#configgenerate_run_time_stats)                       0
#define [configUSE_TRACE_FACILITY](#configuse_trace_facility)                            0
#define [configUSE_STATS_FORMATTING_FUNCTIONS](#configuse_stats_formatting_functions)                0

/* Co-routine related definitions. */
#define [configUSE_CO_ROUTINES](#configuse_co_routines)                               0
#define [configMAX_CO_ROUTINE_PRIORITIES](#configmax_co_routine_priorities)                     1

/* Software timer related definitions. */
#define [configUSE_TIMERS](#configuse_timers)                                    1
#define [configTIMER_TASK_PRIORITY](#configtimer_task_priority)                           3
#define [configTIMER_QUEUE_LENGTH](#configtimer_queue_length)                            10
#define [configTIMER_TASK_STACK_DEPTH](#configtimer_task_stack_depth)                        configMINIMAL_STACK_SIZE

/* Interrupt nesting behaviour configuration. */
#define [configKERNEL_INTERRUPT_PRIORITY](#configkernel_interrupt_priorityconfigmax_syscall_interrupt_priority-和-configmax_api_call_interrupt_priority)         [dependent of processor]
#define [configMAX_SYSCALL_INTERRUPT_PRIORITY](#configkernel_interrupt_priorityconfigmax_syscall_interrupt_priority-和-configmax_api_call_interrupt_priority)    [dependent on processor and application]
#define [configMAX_API_CALL_INTERRUPT_PRIORITY](#configkernel_interrupt_priorityconfigmax_syscall_interrupt_priority-和-configmax_api_call_interrupt_priority)   [dependent on processor and application]

/* Define to trap errors during development. */
#define [configASSERT](#configassert)( ( x ) ) if( ( x ) == 0 ) vAssertCalled( __FILE__, __LINE__ )

/* FreeRTOS MPU specific definitions. */
#define [configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS](#configinclude_application_defined_privileged_functions) 0
#define [configTOTAL_MPU_REGIONS](#configtotal_mpu_regions)                                8 /* Default value */
#define [configTEX_S_C_B_FLASH](#configtex_s_c_b_flash)                                  0x07UL /* Default value */
#define [configTEX_S_C_B_SRAM](#configtex_s_c_b_sram)                                   0x07UL /* Default value */
#define [configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY](#configenforce_system_calls_from_kernel_only)            1
#define [configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS](#configallow_unprivileged_critical_sections)             1
#define [configENABLE_ERRATA_837070_WORKAROUND](#configenable_errata_837070_workaround)                  1

/* ARMv8-M secure side port related definitions. */
#define [secureconfigMAX_SECURE_CONTEXTS](#secureconfigmax_secure_contexts)         5

/* Optional functions - most linkers will remove unused functions anyway. */
#define [INCLUDE_vTaskPrioritySet](#include-参数)                1
#define [INCLUDE_uxTaskPriorityGet](#include-参数)               1
#define [INCLUDE_vTaskDelete](#include-参数)                     1
#define [INCLUDE_vTaskSuspend](#include-参数)                    1
#define [INCLUDE_vTaskDelayUntil](#include-参数)                 1
#define [INCLUDE_vTaskDelay](#include-参数)                      1
#define [INCLUDE_xTaskGetSchedulerState](#include-参数)          1
#define [INCLUDE_xTaskGetCurrentTaskHandle](#include-参数)       1
#define [INCLUDE_uxTaskGetStackHighWaterMark](#include-参数)     0
#define [INCLUDE_uxTaskGetStackHighWaterMark2](#include-参数)    0
#define [INCLUDE_xTaskGetIdleTaskHandle](#include-参数)          0
#define [INCLUDE_eTaskGetState](#include-参数)                   0
#define [INCLUDE_xTimerPendFunctionCall](#include-参数)          0
#define [INCLUDE_xTaskAbortDelay](#include-参数)                 0
#define [INCLUDE_xTaskGetHandle](#include-参数)                  0
#define [INCLUDE_xTaskResumeFromISR](#include-参数)              1

/* A header file that defines trace macro can be included here. */

#endif /* FREERTOS_CONFIG_H */

```

## 'config' 参数

### configUSE_PREEMPTION

如果希望使用抢占式 RTOS 调度器，请将其设置为 1；如果希望使用协同式 RTOS 调度器，请将其设置为 0。

  
### configUSE_PORT_OPTIMISED_TASK_SELECTION

一些 FreeRTOS 移植可通过两种方法选择下一项要执行的任务：
一种是通用方法，另一种是移植特定方法。

通用方法：

* 在 `configUSE_PORT_OPTIMISED_TASK_SELECTION` 设置为 0 时或 
  未实现移植特定方法时使用。
* 可用于所有 FreeRTOS 移植。
* 完全以 C 语言编写，效率低于移植特定方法。
* 对可用优先级的最大数量没有限制。

移植特定方法：

* 部分移植不可用。
* `configUSE_PORT_OPTIMISED_TASK_SELECTION` 设置为 1 时使用。
* 依赖一种或多种架构特定的汇编指令（通常是前导零计数 [CLZ] 指令或等效指令）， 
  因此仅适用于专为其编写该指令的架构。
* 比通用方法更高效。
* 对可用优先级的最大数量有限制，通常为 32 。


### configUSE_TICKLESS_IDLE

如果希望使用[低功耗无滴答模式](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)，请将 `configUSE_TICKLESS_IDLE` 设置为 1；
如果希望保持滴答中断始终运行，请将其设置为 0。并未针对 
所有 FreeRTOS 移植提供低功耗无滴答实现。


### configUSE_IDLE_HOOK

如果希望使用[空闲钩子](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task)，请将其设置为 1；如果希望忽略空闲钩子，请将其设置为 0。

  
### configUSE_MALLOC_FAILED_HOOK

每次创建任务、队列或信号量时，内核都会调用 `pvPortMalloc()` 从堆中分配内存
。官方 FreeRTOS 下载内容中
包括 4 种用于此目的的示例内存分配方案。这些方案
分别在 heap_1.c、heap_2.c、heap_3.c、heap_4.c 和 heap_5.c 源文件中实现。
`configUSE_MALLOC_FAILED_HOOK` 仅在使用这些示例方案时才有意义
。

`malloc()` 失败钩子函数是一个钩子（或回调）函数，
如果已定义并配置，则在 `pvPortMalloc()` 返回 NULL 时会被调用。
仅当剩余的 FreeRTOS 堆内存不足以成功完成请求的分配时，才会返回 NULL
。

如果 `configUSE_MALLOC_FAILED_HOOK` 设置为 1，则应用程序必须定义 `malloc()` 
失败钩子函数。如果 `configUSE_MALLOC_FAILED_HOOK` 设置为 0，
即使定义了 `malloc()` 失败钩子函数，也不会调用该函数。 `malloc()` 
失败钩子函数必须具有如下所示的名称和原型。

```c
void vApplicationMallocFailedHook( void );
```


### configUSE_DAEMON_TASK_STARTUP_HOOK

如果 `configUSE_TIMERS` 和 `configUSE_DAEMON_TASK_STARTUP_HOOK` 都设置为 1，
则应用程序必须定义一个与如下函数具有完全相同名称和原型的
钩子函数。当
RTOS 守护进程任务（也称为[定时器服务任务](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)） 
首次执行时，将只调用一次钩子函数。任何
需要 RTOS 运行的应用程序初始化代码均可放在钩子函数中。

```c
void void vApplicationDaemonTaskStartupHook( void );
```


### configUSE_SB_COMPLETED_CALLBACK

设置 `configUSE_SB_COMPLETED_CALLBACK()` 会将 `xStreamBufferCreateWithCallback()` 
和 `xStreamBufferCreateStaticWithCallback()`（及其消息缓冲区的等效函数）包含在构建中。使用 
这些函数创建的流缓冲区和消息缓冲区可以拥有自己独特的发送完成和接收完成回调， 
而使用 `xStreamBufferCreate()` 
和 `xStreamBufferCreateStatic()`（及其消息缓冲区的等效函数）创建的流缓冲区和消息缓冲区则共享 
由 `sbSEND_COMPLETED()` 和 `sbRECEVE_COMPLETED()` 宏定义的回调。为实现向后兼容，`configUSE_SB_COMPLETED_CALLBACK` 
默认为 0。


### configUSE_TICK_HOOK

如果希望使用[滴答钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions/#tick-hook-function)，请将其设置为 1；如果希望忽略滴答钩子，请将其设置为 0。


### configCPU_CLOCK_HZ

输入*内部*时钟的执行频率（单位为 Hz），该时钟可驱动
用于生成滴答中断的外围设备。
通常情况下，此频率与驱动内部 CPU 时钟的频率相同。此值是
正确配置定时器外围设备所必需的。


### configSYSTICK_CLOCK_HZ

仅适用于 ARM Cortex-M 移植的可选参数。

默认情况下，ARM Cortex-M 移植使用 Cortex-M SysTick 定时器生成 RTOS 滴答中断。大多数 
Cortex-M MCU 以与其本身相同的频率运行 SysTick 定时器。在这种情况下， 
无需 `configSYSTICK_CLOCK_HZ`，应让其保持未定义状态。如果 SysTick 
定时器的时钟频率与 MCU 核心的频率不同，则应将 `configCPU_CLOCK_HZ` 设置为 MCU 
时钟频率（正常情况下），并将 `configSYSTICK_CLOCK_HZ` 设置为 SysTick 时钟频率。


### configTICK_RATE_HZ

RTOS 滴答中断的频率。

滴答中断用于测量时间。因此，滴答频率越高，测量的时间越精确
。但是，滴答频率高也意味着 RTOS 内核将占用更多的 CPU 时间，因此
效率会降低。RTOS 演示应用程序使用的滴答频率均为 1000Hz。这是为了测试 RTOS 内核，
比通常所需的频率要高。

多项任务可以具有相同的优先级。RTOS 调度器
可在每个 RTOS 滴答期间在具有相同优先级的任务之间切换，以共享处理器时间。因此，滴答频率高也会
减少分配给每项任务的“时间切片”。


### configMAX_PRIORITIES

应用程序任务可用的[优先级](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities)数量。多项任务（数量不限） 
可以具有相同的优先级。协程的优先级是独立设置的，请参阅 `configMAX_CO_ROUTINE_PRIORITIES`。

每个可用优先级都会占用 RTOS 内核中的一些 RAM，因此不应将此值设置得高于应用程序
实际需要的数量。

如果 
[configUSE_PORT_OPTIMISED_TASK_SELECTION](#configuse_port_optimised_task_selection) 设置为 1，则最大允许值将受到限制。


### configMINIMAL_STACK_SIZE

空闲任务使用的堆栈大小。通常，此值不应小于 FreeRTOSConfig.h 文件中设置的值，
该文件随所用移植的演示应用程序一起提供。

与 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 和 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 函数的堆栈大小参数一样， 
此堆栈大小以字为单位，而不是字节。如果堆栈上的每个元素都是 32 位，
则堆栈大小为 100 意味着 400 字节（每个 32 位堆栈元素占用 4 个字节）。


### configMAX_TASK_NAME_LEN

创建任务时，赋予该任务的描述性名称的最大允许长度。
长度以字符数指定，*包括* NULL 终止字节。


### configUSE_TRACE_FACILITY

如果希望包含其他结构体成员和函数以协助执行可视化和跟踪，请将其设置为 1。


### configUSE_STATS_FORMATTING_FUNCTIONS

将 `configUSE_TRACE_FACILITY` 和 `configUSE_STATS_FORMATTING_FUNCTIONS` 设置为 1，
即可在构建中包含 [vTaskList()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtasklist) 和 [vTaskGetRunTimeStats()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#vtaskgetruntimestats)
函数。如果将上述其中任意一个函数设置为 0，则可从构建中忽略 `vTaskList()` 和 `vTaskGetRunTimeStates()`。


### configUSE_16_BIT_TICKS

所测量时间的单位为“滴答”，此值是指自 RTOS 内核启动以来滴答中断执行的次数。
滴答计数保存在类型为 `TickType_t` 的变量中。

将 `configUSE_16_BIT_TICKS` 定义为 1 会将 `TickType_t` 定义 (typedef) 为无符号的 16 位类型。
将 `configUSE_16_BIT_TICKS` 定义为 0 会将 `TickType_t` 定义 (typedef) 为无符号的 32 位类型。

在 8 位和 16 位架构上使用 16 位类型可显著提高性能，但会将最大可指定的
时间周期限制为 65535 个“滴答”。因此，假设滴答频率
为 250Hz，使用 16 位计数器时，任务可以延迟或阻塞的最长时间为 262 秒，
而使用 32 位计数器时为 17179869 秒。


### configIDLE_SHOULD_YIELD

此参数用于控制处于空闲优先级的任务的行为，仅在以下情况下有效：

1. 使用抢占式调度器。
2. 应用程序创建的任务以空闲优先级运行。

如果 `configUSE_TIME_SLICING` 设置为 1（或未定义），则具有相同优先级的任务
将共用时间切片。如果没有任务被抢占，则可以假设具有给定优先级的各项任务
都会分配到相同的处理时间，如果该优先级高于空闲优先级，
情况确实如此。

如果任务均为空闲优先级，行为可能会略有不同。如果 `configIDLE_SHOULD_YIELD` 设置为 1，
则在其他具有空闲优先级的任务准备运行时，空闲任务将立即让出 CPU。这可确保
在有应用程序任务可供调度时，空闲任务所占用的时间最少。但是，此行为可能
会产生不良影响（取决于应用程序的需求），如下所示：

![](/media/2018/idleyield.gif)

上图显示了四项以空闲优先级运行的任务的
执行模式。任务 A、B 和 C 是应用程序任务。任务 I 
是空闲任务。在 T0、T1、……、T6 时间点会定期进行上下文切换。空闲任务让出 CPU 时，
任务 A 开始执行，但空闲任务已占用
部分当前时间切片。这会导致任务 I 和任务 A 实际上共用同一时间
切片。因此，应用程序任务 B 和 C 获得的处理时间
要多于应用程序任务 A。

可以通过以下方式避免这种情况：

* 如有必要，使用[空闲钩子](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task)代替处于空闲优先级的单独任务。
* 确保创建的所有应用程序任务的优先级高于空闲优先级。
* 将 `configIDLE_SHOULD_YIELD` 设置为 0。

将 `configIDLE_SHOULD_YIELD` 设置为 0 可防止空闲任务
在其时间切片结束前让出处理时间。这可确保所有处于空闲优先级的任务
（如果没有任务被抢占）都分配到相同的处理时间，
但代价是空闲任务
会占用更多的总处理时间。


### configUSE_TASK_NOTIFICATIONS

将 `configUSE_TASK_NOTIFICATIONS` 设置为 1（或将 `configUSE_TASK_NOTIFICATIONS` 保留为未定义状态） 
将在构建中包含[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)功能 
及其相关 API。

将 `configUSE_TASK_NOTIFICATIONS` 设置为 0 将从构建中排除直达任务通知功能 
及其相关 API。

如果在构建中包含直达任务通知，每项任务会额外消耗 8 字节的 RAM。


### configTASK_NOTIFICATION_ARRAY_ENTRIES

每项 RTOS 任务都有一个[任务通知数组](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。 `configTASK_NOTIFICATION_ARRAY_ENTRIES` 
可用于设置数组中的索引数。 

在 FreeRTOS V10.4.0 之前，任务只有一个通知值，没有通知值数组， 
因此，出于向后兼容考虑，如果 `configTASK_NOTIFICATION_ARRAY_ENTRIES` 未定义，则默认为 1。


### configUSE_MUTEXES

如果希望在构建中包含互斥锁功能，请将其设置为 1；如果希望从构建中忽略互斥锁功能，请将其设置为 0。 
读者应该熟悉 
与 FreeRTOS 功能相关的互斥锁和二进制信号量之间的区别。

  
### configUSE_RECURSIVE_MUTEXES

如果希望在构建中包含递归互斥锁功能，请将其设置为 1；如果希望从构建中忽略递归互斥锁功能， 
请将其设置为 0。
  

### configUSE_COUNTING_SEMAPHORES

如果希望在构建中包含计数信号量功能，请将其设置为 1；如果希望从构建中忽略计数信号量功能， 
请将其设置为 0。
  

### configUSE_ALTERNATIVE_API

如果希望在构建中包含“替代”队列函数，请将其设置为 1；如果希望从构建中忽略“替代”队列函数， 
请将其设置为 0。有关替代 API，请参阅 queue.h 头文件。
**替代 API 已弃用，不应在新设计中使用**。


### configCHECK_FOR_STACK_OVERFLOW

[堆栈溢出检测](Stacks-and-stack-overflow-checking.md)页面描述了
此参数的用法。


### configQUEUE_REGISTRY_SIZE

队列注册表有两项用途，都与 RTOS 内核感知调试相关：

1. 可将文本名称和队列关联，以在调试 GUI 中轻松识别队列。
2. 包含调试器定位每个已注册队列和信号量所需的信息。

队列注册表仅在使用 RTOS 内核感知调试器时才有作用。

`configQUEUE_REGISTRY_SIZE` 定义可以注册的队列和信号量的最大数量。
仅需注册那些希望通过 RTOS 内核感知调试器查看的队列和信号量。
有关更多信息，请参阅 [vQueueAddToRegistry()](/Documentation/02-Kernel/04-API-references/06-Queues/15-vQueueAddToRegistry)
和 [vQueueUnregisterQueue()](/Documentation/02-Kernel/04-API-references/06-Queues/16-vQueueUnregisterQueue) 的 API 参考文档。


### configUSE_QUEUE_SETS

如果希望包含[队列集](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)功能（即
在多个队列和信号量上阻塞或挂起的能力），请将其设置为 1；如果希望忽略队列集功能，请将其设置为 0。


### configUSE_TIME_SLICING

默认情况下（如果未定义 `configUSE_TIME_SLICING`，或者 `configUSE_TIME_SLICING`
定义为 1），FreeRTOS 使用带时间切片的抢占式优先级调度。
这意味着 RTOS 调度器将始终运行优先级最高且处于就绪状态的任务，
并在每个 RTOS 滴答中断时在优先级相同的任务之间
切换。如果 `configUSE_TIME_SLICING` 设置为 0，则 RTOS 调度器
仍会运行优先级最高且处于就绪状态的任务，但不会
因为发生滴答中断而在优先级相同的任务之间切换。

  
### configUSE_NEWLIB_REENTRANT

如果 `configUSE_NEWLIB_REENTRANT` 设置为 1，则创建的所有任务都会分配到一个 [newlib](http://sourceware.org/newlib/) 
重入结构体。

请注意，我们已应大众需求增加了 Newlib 支持，
但 FreeRTOS 维护者自己并未使用。FreeRTOS
对由此产生的 newlib 操作概不负责。用户必须熟悉
newlib，并提供必要存根的系统级
实现。请注意，（在撰写本文时）当前的 newlib 设计
实现了系统级 `malloc()`，必须为该函数提供锁。


### configENABLE_BACKWARD_COMPATIBILITY

FreeRTOS.h 头文件包含一组 #define 宏，用于
将 FreeRTOS 8.0.0 之前版本中使用的数据类型名称映射到
FreeRTOS 8.0.0 版本中使用的名称。借助这些宏，无需修改应用程序代码，
即可将 FreeRTOS 8.0.0 之前的版本更新为
8.0.0 之后版本。将 `configENABLE_BACKWARD_COMPATIBILITY`
设置为 0（在 FreeRTOSConfig.h 中）可从构建中排除这些宏，
从而确保没有使用 8.0.0 版本之前的名称。

  
### configNUM_THREAD_LOCAL_STORAGE_POINTERS

设置每项任务的[线程本地存储数组](thread-local-storage-pointers.md)中的索引数。

  
### configUSE_MINI_LIST_ITEM

`MiniListItem_t` 用于 FreeRTOS 列表中的开始和结束标记节点，而 `ListItem_t` 则用于 
FreeRTOS 列表中的所有其他节点。`configUSE_MINI_LIST_ITEM` 设置为 0 时，`MiniListItem_t` 
和 `ListItem_t` 保持一致。`configUSE_MINI_LIST_ITEM` 设置为 1 时，`MiniListItem_t` 包含的字段 
比 `ListItem_t` 少 3 个，这样可以节省一些 RAM，但代价是可能违反某些编译器用于优化时所依赖的 
严格别名规则。如果未定义，`configUSE_MINI_LIST_ITEM` 默认为 1， 
以实现向后兼容。


### configSTACK_DEPTH_TYPE

设置在调用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 时用于指定堆栈深度的类型，
以及在许多其他使用堆栈大小的地方（例如，返回 
[堆栈高水位线](/Documentation/02-Kernel/04-API-references/03-Task-utilities/04-uxTaskGetStackHighWaterMark)时）使用的类型。

旧版 FreeRTOS 使用类型为 `UBaseType_t` 的变量指定堆栈大小， 
但这对 8 位微控制器的限制过于严格。 `configSTACK_DEPTH_TYPE`
可让应用程序开发者指定使用的类型，进而解除了这一限制
。


### configMESSAGE_BUFFER_LENGTH_TYPE

[FreeRTOS 消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)使用
类型为 `configMESSAGE_BUFFER_LENGTH_TYPE` 的变量存储
每条消息的长度。如果未定义，`configMESSAGE_BUFFER_LENGTH_TYPE`
默认为 `size_t`。如果存储在消息缓冲区中的消息
从未超过 255 字节，则在 32 位微控制器上将 `configMESSAGE_BUFFER_LENGTH_TYPE` 定义为 `uint8_t`
可为每条消息节省 3 个字节。同样，如果
存储在消息缓冲区中的消息从未超过 65535 字节，
则在 32 位微控制器上将 `configMESSAGE_BUFFER_LENGTH_TYPE` 定义为 `uint16_t`
可为每条消息节省 2 个字节。


### configSUPPORT_STATIC_ALLOCATION

如果 `configSUPPORT_STATIC_ALLOCATION` 设置为 1，则 RTOS 对象可以
通过应用程序编写者提供的 RAM 创建。

如果 `configSUPPORT_STATIC_ALLOCATION` 设置为 0，则 RTOS 对象
只能通过从 FreeRTOS 堆中分配的 RAM 创建。

如果 `configSUPPORT_STATIC_ALLOCATION` 未定义，则默认为 0。

如果 `configSUPPORT_STATIC_ALLOCATION` 设置为 1，则应用程序编写者还必须提供两个回调 
函数：

`vApplicationGetIdleTaskMemory()`，为 RTOS 空闲任务提供内存；（如果 `configUSE_TIMERS` 
设置为 1）`vApplicationGetTimerTaskMemory()`，为 RTOS 守护进程/定时器服务任务提供内存。 
示例如下。

```c
/* configSUPPORT_STATIC_ALLOCATION is set to 1, so the application must provide an  
   implementation of vApplicationGetIdleTaskMemory() to provide the memory that is  
   used by the Idle task. */  
void vApplicationGetIdleTaskMemory( StaticTask_t **ppxIdleTaskTCBBuffer,  
                                    StackType_t **ppxIdleTaskStackBuffer,  
                                    uint32_t *pulIdleTaskStackSize )  
{  
    /* If the buffers to be provided to the Idle task are declared inside this  
       function then they must be declared static - otherwise they will be allocated on  
       the stack and so not exists after this function exits. */  
    static StaticTask_t xIdleTaskTCB;  
    static StackType_t uxIdleTaskStack[ configMINIMAL_STACK_SIZE ];  

    /* Pass out a pointer to the StaticTask_t structure in which the Idle task's  
       state will be stored. */  
    *ppxIdleTaskTCBBuffer = &xIdleTaskTCB;  

    /* Pass out the array that will be used as the Idle task's stack. */  
    *ppxIdleTaskStackBuffer = uxIdleTaskStack;  

    /* Pass out the size of the array pointed to by *ppxIdleTaskStackBuffer.  
       Note that, as the array is necessarily of type StackType_t,  
       configMINIMAL_STACK_SIZE is specified in words, not bytes. */  
    *pulIdleTaskStackSize = configMINIMAL_STACK_SIZE;  
}  

/*-----------------------------------------------------------*/  

/* configSUPPORT_STATIC_ALLOCATION and configUSE_TIMERS are both set to 1, so the  
   application must provide an implementation of vApplicationGetTimerTaskMemory()  
   to provide the memory that is used by the Timer service task. */  
void vApplicationGetTimerTaskMemory( StaticTask_t **ppxTimerTaskTCBBuffer,  
                                     StackType_t **ppxTimerTaskStackBuffer,  
                                     uint32_t *pulTimerTaskStackSize )  
{  
    /* If the buffers to be provided to the Timer task are declared inside this  
       function then they must be declared static - otherwise they will be allocated on  
       the stack and so not exists after this function exits. */  
    static StaticTask_t xTimerTaskTCB;  
    static StackType_t uxTimerTaskStack[ configTIMER_TASK_STACK_DEPTH ];  

    /* Pass out a pointer to the StaticTask_t structure in which the Timer  
       task's state will be stored. */  
    *ppxTimerTaskTCBBuffer = &xTimerTaskTCB;  

    /* Pass out the array that will be used as the Timer task's stack. */  
    *ppxTimerTaskStackBuffer = uxTimerTaskStack;  

    /* Pass out the size of the array pointed to by *ppxTimerTaskStackBuffer.  
       Note that, as the array is necessarily of type StackType_t,  
      configTIMER_TASK_STACK_DEPTH is specified in words, not bytes. */  
    *pulTimerTaskStackSize = configTIMER_TASK_STACK_DEPTH;  
}  
```

应用程序必须提供回调函数示例，用于为空闲任务和定时器服务任务提供 RAM 
（如果 `configSUPPORT_STATIC_ALLOCATION` 设置为 1）。  

有关更多信息，请参阅[静态与动态内存分配](Static_Vs_Dynamic_Memory_Allocation.md)页面。


### configSUPPORT_DYNAMIC_ALLOCATION

如果 `configSUPPORT_DYNAMIC_ALLOCATION` 设置为 1，则 RTOS 对象可通过 RAM 
（从 FreeRTOS 堆中自动分配）创建。

如果 `configSUPPORT_DYNAMIC_ALLOCATION` 设置为 0，则 RTOS 对象只能通过应用程序编写者提供的 RAM 创建 
。

如果 `configSUPPORT_DYNAMIC_ALLOCATION` 未定义，则默认为 1。

有关更多信息，请参阅[静态与动态内存分配](Static_Vs_Dynamic_Memory_Allocation.md)页面。


### configTOTAL_HEAP_SIZE

FreeRTOS 堆中可用的 RAM 总量。

仅当 [configSUPPORT_DYNAMIC_ALLOCATION](#configsupport_dynamic_allocation) 设置为 1，
并且应用程序使用
FreeRTOS 源代码下载内容中提供的一种示例内存分配方案时，才会使用此值。
请参阅[内存配置](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，了解更多详情。


### configAPPLICATION_ALLOCATED_HEAP

默认情况下，[FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)由 FreeRTOS 声明，
并由链接器放置在内存中。如果将 `configAPPLICATION_ALLOCATED_HEAP` 设置为 1，
应用程序编写者可声明堆，
这意味着应用程序编写者可以将堆放置在内存中的任意位置。

如果使用 heap_1.c、heap_2.c 或 heap_4.c，并且 `configAPPLICATION_ALLOCATED_HEAP`
设置为 1，则应用程序编写者必须提供一个 `uint8_t`数组，
其名称和维度必须与下面所示完全一致。该数组将用作 FreeRTOS 堆。
如何将数组放置在特定内存位置取决于所使用的编译器，
请参阅编译器文档。

```c
uint8_t ucHeap[ configTOTAL_HEAP_SIZE ];
```


### configSTACK_ALLOCATION_FROM_SEPARATE_HEAP

如果 `configSTACK_ALLOCATION_FROM_SEPARATE_HEAP` 设置为 1， 
则使用 [xTaskCreate](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 或 [xTaskCreateRestricted](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted) API 创建的任务堆栈
将分别通过 `pvPortMallocStack` 和 `vPortFreeStack` 函数进行分配和释放。用户需要
提供 `pvPortMallocStack` 和 `vPortFreeStack` 函数的线程安全实现。
如此一来，用户便可以从内存的另一个区域
（可能是与 FreeRTOS 堆不同的另一个堆）为任务分配堆栈。

如果 `configSTACK_ALLOCATION_FROM_SEPARATE_HEAP` 未定义，则默认为 0。

`pvPortMallocStack` 和 `vPortFreeStack` 函数的示例实现如下：

```c
void * pvPortMallocStack( size_t xWantedSize  )  
{  
    /* Allocate a memory block of size xWantedSize. The function used for  
     * allocating memory must be thread safe. */  
    return MyThreadSafeMalloc( xWantedSize );  
}  

void vPortFreeStack( void * pv )  
{  
    /* Free the memory previously allocated using pvPortMallocStack. The  
     * function used for freeing the memory must be thread safe. */  
    MyThreadSafeFree( pv );  
}  
```

`pvPortMallocStack` 和 `vPortFreeStack` 函数的示例实现
  

### configGENERATE_RUN_TIME_STATS

[运行时统计](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/10-Run-time-statistics)页面描述了此参数的用法。
  

### configUSE_CO_ROUTINES

如果希望在构建中包含协程功能，请将其设置为 1；如果希望从构建中忽略协程功能， 
请将其设置为 0。要包含协程功能，项目中必须包含 croutine.c。

  
### configMAX_CO_ROUTINE_PRIORITIES

应用程序协程可用的[优先级](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/09-Co-routine-priorities)数量。多个协程（数量不限） 
可以具有相同的优先级。任务的优先级是独立设置的，请参阅 `configMAX_PRIORITIES`。


### configUSE_TIMERS

如果希望包含软件定时器功能，请将其设置为 1；如果希望忽略软件定时器功能，请将其设置为 0。
请参阅 [FreeRTOS 软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)页面，查看完整描述。


### configTIMER_TASK_PRIORITY

设置软件定时器服务/守护进程任务的优先级。
请参阅 [FreeRTOS 软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)页面，查看完整描述。


### configTIMER_QUEUE_LENGTH

设置软件定时器命令队列的长度。
请参阅 [FreeRTOS 软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)页面，查看完整描述。


### configTIMER_TASK_STACK_DEPTH

设置分配给软件定时器服务/守护进程任务的堆栈深度。
请参阅 [FreeRTOS 软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)页面，查看完整描述。


### configKERNEL_INTERRUPT_PRIORITY、configMAX_SYSCALL_INTERRUPT_PRIORITY 和 configMAX_API_CALL_INTERRUPT_PRIORITY

包含 `configKERNEL_INTERRUPT_PRIORITY` 设置的移植包括 ARM Cortex-M3、PIC24、dsPIC、PIC32、 
SuperH 和 RX600。包含 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 设置的移植包括 PIC32、RX600、 
ARM Cortex-A 和 ARM Cortex-M。

ARM Cortex-M3 和 ARM Cortex-M4 用户请注意本节末尾的特别注意事项！

`configMAX_API_CALL_INTERRUPT_PRIORITY` 是 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 的新名称， 
仅用于新版移植。两者功能相同。

`configKERNEL_INTERRUPT_PRIORITY` 应设置为最低优先级。

请注意，在以下讨论中，只有以 "FromISR" 结尾的 API 函数 
才能从中断服务程序中调用。

对于仅实现 `configKERNEL_INTERRUPT_PRIORITY` 的移植

`configKERNEL_INTERRUPT_PRIORITY` 设置 RTOS 内核自身使用的中断优先级。调用 API 函数的中断 
也必须在此优先级下执行。不调用 API 函数的中断可以 
在更高的优先级下执行，因此其执行不会因 RTOS 内核活动而延迟 
（在硬件本身的限制范围内）。

对于同时实现 `configKERNEL_INTERRUPT_PRIORITY` 和 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 的移植：  

`configKERNEL_INTERRUPT_PRIORITY` 设置 RTOS 内核自身使用的中断优先级。 
`configMAX_SYSCALL_INTERRUPT_PRIORITY` 设置 
可以调用中断安全 FreeRTOS API 函数的最高中断优先级。

要实现完全中断嵌套模型，可将 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 
设置为高于 `configKERNEL_INTERRUPT_PRIORITY`（即优先级更高）。 
**这意味着即使在临界区内部，FreeRTOS 内核也不会完全禁用中断。** 
此外，这是在未引入分段内核架构缺点的情况下实现的。但是，请注意， 
某些微控制器架构会在接受新中断时（在硬件中）禁用中断， 
这意味着在硬件接受中断
和 FreeRTOS 代码重启中断之间的短暂时间内，中断不可避免地会被禁用。

不调用 API 函数的中断可以在优先级高于 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 的情况下执行， 
因此不会因 RTOS 内核执行而延迟。

例如，假设一个微控制器具有 8 个中断优先级：0 为最低优先级， 
7 为最高优先级（请参阅本节末尾针对 ARM Cortex-M3 用户的特别注意事项）。如果 
将两个配置常量设置为 4 和 0，下图描述了在各个优先级上 
可以执行以及不能执行的操作：

![](/media/2018/Interrupt-priorities-interrupt-nesting.jpg)  
中断优先级配置示例

这些配置参数可以实现非常灵活的中断处理：

* 可以像系统中的其他任务一样编写中断处理“任务”并设置优先级。这些 
  任务由中断唤醒。编写的中断服务程序 (ISR) 本身应尽可能简短， 
  只需获取数据，然后唤醒高优先级处理程序任务。 
  ISR 随后直接返回到唤醒的处理程序任务，因此中断处理在时间上是连续的， 
  就像所有处理都在 ISR 中完成一样。这样做的优势在于， 
  在处理程序任务执行期间，所有中断都保持启用状态。
  
* 实现 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 的移植更进一步，允许完全嵌套模型， 
  优先级介于 RTOS 内核中断优先级和 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 之间的中断可以嵌套 
  并调用相关的 API 函数。优先级高于 `configMAX_SYSCALL_INTERRUPT_PRIORITY` 的中断永远不会 
  因 RTOS 内核活动而延迟。

* 在最高系统调用优先级之上运行的 ISR 永远不会被 RTOS 内核屏蔽，因此其响应度 
  不会受到 RTOS 内核功能的影响。

  这非常适合对时间精度要求极高的中断（例如执行电机换向的中断）。
  但是，此类 ISR 无法使用 FreeRTOS API 函数。

要使用此方案，应用程序设计必须遵循以下规则：**对于使用 FreeRTOS API 的中断，
优先级必须设置为与 RTOS 内核相同（由 
`configKERNEL_INTERRUPT_PRIORITY` 宏配置）；对于包含此功能的移植，
优先级应设置为等于或低于 `configMAX_SYSCALL_INTERRUPT_PRIORITY`。**

ARM Cortex-M3 和 ARM Cortex-M4 用户特别注意事项： 
请参阅[专门介绍如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。
至少请记住，ARM Cortex-M3 核心中，数字越小，中断优先级越高。
这似乎有悖直觉，而且很容易忘记！如果希望 
为中断分配低优先级，请勿将其优先级指定为 0（或其他较小数值）， 
因为这实际上可能会导致该中断在系统中具有最高优先级， 
因此如果此优先级高于 `configMAX_SYSCALL_INTERRUPT_PRIORITY`，则可能导致系统崩溃。

ARM Cortex-M3 核心的最低优先级实际上是 255，但是不同的 ARM Cortex-M3 供应商 
实现的优先级位数不同，并且提供的库函数 
要求以不同的方式指定优先级。例如，在 STM32 上，您可以 
在 ST 驱动程序库调用中指定的最低优先级实际上是 15，而可以指定的最高优先级是 0。


### configASSERT

`configASSERT()` 宏与标准 C `assert()` 宏具有相同的语义。如果
传递给 `configASSERT()` 的参数为零，则会触发断言。

在 FreeRTOS 源文件中，可调用 `configASSERT()` 以检查
应用程序如何使用 FreeRTOS。强烈建议在开发 FreeRTOS
应用程序时定义 `configASSERT()`。

示例定义（在文件顶部显示，复制如下）调用 `vAssertCalled()`， 
传入触发 `configASSERT()` 调用的文件名和行号（\_\_FILE\_\_ 和
\_\_LINE\_\_ 是大多数编译器提供的标准宏）。这只是演示，
因为 `vAssertCalled()` 不是 FreeRTOS 函数，`configASSERT()` 可以定义为
执行应用程序编写者认为合适的任何操作。

通常情况下，会将 `configASSERT()` 定义为
阻止应用程序进一步执行。这有两个原因：
首先，在断言点停止应用程序，可以帮助开发者找出断言失败的原因，从而进行调试；
其次，如果在触发断言后继续执行，应用程序最终
很可能会崩溃。

请注意，定义 `configASSERT()` 会增加应用程序的代码大小和
执行时间。应用程序足够稳定时，
只需注释掉 `configASSERT()` 定义
（在 FreeRTOSConfig.h 中），即可消除额外的开销。

```c
/* Define configASSERT() to call vAssertCalled() if the assertion fails. The assertion
   has failed if the value of the parameter passed into configASSERT() equals zero. */
#define configASSERT ( x )     if( ( x ) == 0 ) vAssertCalled( __FILE__, __LINE__ )
```

如果在调试器的控制下运行 FreeRTOS，则可以将 `configASSERT()`
定义为仅禁用中断并进入循环，如下所示。
这会导致代码停在未能通过断言测试的那一行，
暂停调试器即可立即转到出错行，
方便您查看失败的原因。

```c
/* Define configASSERT() to disable interrupts and sit in a loop. */
#define configASSERT ( x )     if( ( x ) == 0 ) { taskDISABLE_INTERRUPTS(); for( ;; ); }
```


### configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS

`configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS` 仅供 FreeRTOS MPU 使用。

如果 `configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS` 设置为 1,
则应用程序编写者必须提供 "application_defined_privileged_functions.h" 头文件，
在该文件中可以实现需要在特权模式下执行的函数
。请注意，尽管该头文件有 .h 扩展名，但应包含
C 函数的实现，而不仅仅是函数的原型。

在 "application_defined_privileged_functions.h" 中实现的函数必须
分别使用 `prvRaisePrivilege()` 函数
和 `portRESET_PRIVILEGE()` 宏保存和恢复处理器的特权状态。例如，如果库提供的
打印函数访问的 RAM 超出应用程序编写者的控制范围，
因而无法分配给受内存保护的用户模式任务，
则可以使用以下代码将打印函数封装在特权函数中：

```c
void MPU_debug_printf( const char *pcMessage )
{
    /* State the privilege level of the processor when the function was called. */
    BaseType_t xRunningPrivileged = prvRaisePrivilege();

    /* Call the library function, which now has access to all RAM. */
    debug_printf( pcMessage );

    /* Reset the processor privilege level to its original value. */
    portRESET_PRIVILEGE( xRunningPrivileged );
}
```

这种技术应仅在开发过程中使用，而不能用于部署阶段，因为它会
绕过内存保护。


### configTOTAL_MPU_REGIONS

ARM Cortex-M4 微控制器的 FreeRTOS MPU（内存保护单元）移植支持
具有 16 个 MPU 区域的设备。对于具有 16 个 MPU 区域的设备，应将 `configTOTAL_MPU_REGIONS` 设置为 16。
如果未定义，则默认为 8。


### configTEX_S_C_B_FLASH

TEX、可共享 (S)、可缓存 (C) 和可缓冲 (B) 位定义了内存类型，
必要时还可以定义 MPU 区域的可缓存和可共享属性。 `configTEX_S_C_B_FLASH`
允许应用程序编写者
对包含 Flash 的 MPU 区域的 TEX、可共享 (S)、可缓存 (C)、和可缓冲 (B) 位的默认值进行覆盖。如果未定义，
则默认为 0x07UL，即 TEX=000、S=1、C=1、B=1。 


### configTEX_S_C_B_SRAM

TEX、可共享 (S)、可缓存 (C) 和可缓冲 (B) 位定义了内存类型，
必要时还可以定义 MPU 区域的可缓存和可共享属性。 `configTEX_S_C_B_SRAM`
允许应用程序编写者
对包含 RAM 的 MPU 区域的 TEX、可共享 (S)、可缓存 (C)、和可缓冲 (B) 位的默认值进行覆盖。如果未定义，
则默认为 0x07UL，即 TEX=000、S=1、C=1、B=1。 


### configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY

`configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY` 可以定义为 1，以防止
来自内核代码外部的特权升级
（进入中断时硬件本身执行的升级除外 ）。`configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY`
在 FreeRTOSConfig.h 中设置为 1 时，变量 `__syscalls_flash_start__` 
和 `__syscalls_flash_end__` 需要从链接器脚本中导出，以分别指示
系统调用内存的起始和结束地址。为实现最高安全性，建议将其定义为 1。


### configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS

仅用于 ARMv7-M MPU 移植 (ARM Cortex-M3/4/7)。

将其设置为 0，可防止非特权应用程序任务使用 `taskENTER_CRITICAL()` 宏创建 
临界区。将此常量设置为 1 或保留为未定义状态，可允许特权或非特权 
任务创建临界区。注意：为实现最高安全性，建议将此常量定义为 0。 
因此，如果未定义此常量，编译器会输出警告。


### configENABLE_ERRATA_837070_WORKAROUND

仅用于 Cortex-M4 MPU 移植。

在使用 Cortex-M7 r0p0/r0p1 核心上的 Cortex-M4 MPU 移植时，将 `configENABLE_ERRATA_837070_WORKAROUND`
设置为 1，可激活 ARM 勘误表 837070 所需的解决方法。


### configHEAP_CLEAR_MEMORY_ON_FREE

如果设置为 1 ，则使用 `pvPortMalloc()` 分配的内存块 
会在通过 `vPortFree()` 释放时被清除。如果未定义，`configHEAP_CLEAR_MEMORY_ON_FREE` 默认为 0， 
以实现向后兼容。为提高安全性，建议将 `configHEAP_CLEAR_MEMORY_ON_FREE` 设置为 1。


### secureconfigMAX_SECURE_CONTEXTS

仅用于 ARMv8-M 安全端移植。

从 ARMv8-M MCU（ARM Cortex-M23、Cortex-M33 
和 Cortex-M55）非安全端调用安全函数的任务有两种上下文：一种位于非安全端，另一种位于安全端。在 FreeRTOS 
v10.4.5 之前，ARMv8-M 安全端移植会在运行时分配引用安全端上下文的结构体。 
自 FreeRTOS 10.4.5 版本开始，编译时会静态分配结构体。 `secureconfigMAX_SECURE_CONTEXTS` 
可用于设置静态分配的安全上下文的数量。如果未定义，则 `secureconfigMAX_SECURE_CONTEXTS` 默认为 
8。仅在 ARMv8-M 微控制器的非安全端使用 FreeRTOS 代码的应用程序 
（例如在安全端运行第三方代码的应用程序）无需此常量。


## INCLUDE 参数

以 'INCLUDE' 开头的宏允许从构建中排除应用程序未使用的
实时内核组件。这可确保 RTOS 不会使用超出特定嵌入式应用程序所需的 ROM 或 RAM
。

此类宏的形式如下……

```c
INCLUDE_FunctionName ... 
```

其中 FunctionName 表示可以选择排除的 API 函数（或函数集）。要 
包含 API 函数，请将宏设置为 1；要排除该函数，请将宏设置为 0。 
例如，要包含 `vTaskDelete()` API 函数，请使用： 

```c
#define INCLUDE_vTaskDelete 1
```

要从构建中排除 `vTaskDelete()`，请使用： 

```c
#define INCLUDE_vTaskDelete 0  
```

