---
title: "FreeRTOS V9"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 路线图和版本说明
description: 关于 FreeRTOS V9 的信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


### 序言

请参阅[变更历史记录](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history)了解有关最终 FreeRTOS
V9.0.0 版本与之前候选版本之间差异的完整信息，尤其是
与新 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
API 函数原型相关的信息。


### FreeRTOS V9 亮点

#### 向后兼容性

FreeRTOS V9.x.x 是 FreeRTOS V8.x.x 的直接兼容替代产品，
包含新的功能、增强功能和新的移植。


#### 完全静态分配系统

引入了两个新的配置常量，允许 FreeRTOS
[在无需动态内存分配的情况下](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)选择性使用
。更多信息，请参阅
[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
和 [configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) 常量的说明，
特别是注意当 configSUPPORT_STATIC_ALLOCATION 设置为 1 时，
应用程序写入器需要提供两个回调函数。

我们提供了位于 /FreeRTOS/demo/WIN32-MSVC-Static-Allocation-Only 目录[(/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo)中的 ]Win32 演示作为参考，
说明如何创建一个完全不包含
[FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)的项目，
从而保证不执行动态内存分配。


#### 使用静态分配的 RTOS 创建任务和其他 RAM对象

另请参阅 [[静态内存分配 Vs 动态内存分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面]

每个 [object]Create() RTOS API 函数现在都有一个新的 [object]CreateStatic()
等价函数。更简单的 Create() 函数将使用动态内存分配，
而功能更强大的 CreateStatic() 函数将
使用应用程序写入器传递到该函数的内存。这
允许使用静态分配或动态分配的内存来
创建任务、队列、信号量、软件定时器、互斥锁和事件组。
例如：


* [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)
  将[动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
  创建任务所需的内存
  。 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
  不会执行任何动态内存分配，
  而是使用函数参数传递给函数的内存。

* [xQueueCreate()](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate) 将动态分配
  创建队列所需的内存
  。 [xQueueCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic)
  不会执行任何动态内存分配，
  而是使用函数参数传递给函数的内存。

* 同样，可使用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate)
  或 [xEventGroupCreateStatic()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/02-xEventGroupCreateStatic) 创建事件组，
  可使用 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
  或 [xTimerCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic) 创建软件定时器，
  可使用
  使用 [xSemaphoreCreateBinary()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary)
  或 [xSemaphoreCreateBinaryStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic) 创建二进制信号量，
  可使用 [xSemaphoreCreateCounting()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting)
  或 [xSemaphoreCreateCountingStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/05-xSemaphoreCreateCountingStatic) 创建计数信号量，
  可使用 [xSemaphoreCreateMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)
  或 [xSemaphoreCreateMutexStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic)创建互斥锁。

configSUPPORT_DYNAMIC_ALLOCATION 必须在 FreeRTOSConfig.h 中设置为 1
（或者不定义，因为它默认为 1），创建函数的“动态”版本
才可用。

configSUPPORT_STATIC_ALLOCATION 必须在 FreeRTOSConfig.h 中设置为 1，
创建函数的“静态”版本才可用——还需注意，
当
[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation) 设置为 1 时，
应用程序写入器需要提供两个回调函数。

提供 [StaticAllocation.c](https://sourceforge.net/p/freertos/code/HEAD/tree/trunk/FreeRTOS/Demo/Common/Minimal/StaticAllocation.c)
标准演示任务是用于演示如何使用新的 CreateStatic() 函数。


#### 强制 RTOS 任务离开阻塞状态

RTOS 任务进入阻塞状态，
以确保它们在等待时间推移或事件发生时不使用任何处理时间。例如，
如果一个任务调用 [vTaskDelay](/Documentation/02-Kernel/04-API-references/02-Task-control/02-vTaskDelayUntil)( 100 )，
它将进入“阻塞”状态，保持 100 的滴答的时间。另一个例子是，
如果一个任务调用 [xSemaphoreTake](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)( xSemaphore, 50 )，
那么它将进入阻塞状态，直到信号量可用，
或者直到因为 50 个滴答过去了而信号量没有变得可用而超时。
[注意：在实际应用中，最好使用 pdMS\\_TO\\_TICKS() 宏
而不是滴答来指定以毫秒为单位的时间。］

新的 [xTaskAbortDelay](/Documentation/02-Kernel/04-API-references/02-Task-control/09-xTaskAbortDelay)() RTOS API 函数可使一个任务
迫使另一个任务立即脱离阻塞状态。这在以下情况下是可取的：
系统中其他地方发生的事件意味着阻塞状态的任务应该停止等待事件，
或者阻塞状态的任务有更紧急的事情要做
。

INCLUDE_xTaskAbortDelay 必须在 FreeRTOSConfig.h 中设置为 1，
xTaskAbortDelay() 函数才可用。

[AbortDelay.c](https://sourceforge.net/p/freertos/code/HEAD/tree/trunk/FreeRTOS/Demo/Common/Minimal/AbortDelay.c)
标准演示任务是用于演示如何使用 xTaskAbortDelay() 函数。


#### 删除任务

在 V9 之前的 FreeRTOS 版本中，每当一个任务被删除，
FreeRTOS 分配给该任务的内存就会被空闲任务释放。在 FreeRTOS V9 中，
如果一个任务删除了另一个任务，则 FreeRTOS 分配给
被删除任务的内存会立即被释放。但是，如果某个任务自己删除了自己，
空闲任务仍然会释放 FreeRTOS 分配给该任务的内存。
请注意，在任何情况下，
只有 RTOS 分配给任务的堆栈和任务控制块 (TCB) 才会被自动释放。


#### 从任务名称中获取任务句柄

新的 [xTaskGetHandle](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)() API 函数
从任务的人类可读文本名称中获取任务句柄。

xTaskGetHandle() 使用多字符串比较操作，
所以建议每个任务只调用一次。然后，
xTaskGetHandle() 返回的句柄可存储在本地，以备日后重用。


### 其他变更

更多详细信息，请参阅[变更历史记录](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history)。

* 允许 FreeRTOS 在 64 位架构上运行所需的更新。

* 针对移植如何使用浮点单元方面增强了 GCC ARM Cortex-A 移植层
  。

* 使用(MPU)更新配置了内存保护的 ARM Cortex-M RTOS 移植。

* 增加了 vApplicationDaemonTaskStartupHook()，当 RTOS
  守护进程任务（以前称为定时器服务任务）开始运行时执行
  。如果应用程序包含会从调度器启动后执行中受益的初始化代码，
  这将非常有用。

* 新增了 pcQueueGetName() API 函数，
  该函数从队列的句柄中获取队列名称。

* 当 configUSE_PREEMPTION 为 0 时，也可以使用无滴答闲置（适用于低功耗应用）。

* 如果一个任务通知被用来从 ISR 中解锁一个任务，
  但没有使用 xHigherPriorityTaskWoken 参数，那么就挂起一个上下文切换，
  然后在下一个滴答中断期间发生。

* Heap_1.c 和 Heap_2.c 现在使用之前仅由 heap_4.c 使用的 [configAPPLICATION_ALLOCATED_HEAP](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configapplication_allocated_heap) 设置
  。
  configAPPLICATION_ALLOCATED_HEAP 允许应用程序写入器声明
  将被用作 FreeRTOS 堆的数组，
  并在这样做时将堆放在一个特定的内存位置。

* 用于获取任务详情的 TaskStatus_t 结构体，现在包含了任务堆栈的基地址。

* 新增了 vTaskGetInfo() API 函数，该函数返回一个包含单个任务信息的 TaskStatus_t 结构体。
  此前，只能一次性获得所有任务的此类信息，作为 TaskStatus_t 结构体的数组。

* 新增了 uxSemaphoreGetCount() API 函数。

* 在一些 Cortex-M3 移植层中复制以前的 Cortex-M4F 和 Cortex-M7 优化。

* 常规重构。

* 支持多个附加设备。
