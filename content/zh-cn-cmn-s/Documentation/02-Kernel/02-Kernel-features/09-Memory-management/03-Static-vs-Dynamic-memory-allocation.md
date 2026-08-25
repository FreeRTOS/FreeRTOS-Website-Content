---
title: "静态内存分配 vs 动态内存分配"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 本页记录了静态内存分配和动态内存分配之间的差异
relatedLinks:
  - title: 静态内存分配 vs 动态内存分配
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation/
---

### 引言

在 FreeRTOS V9.0.0 之前的版本中，下列 RTOS 对象使用的内存
是从[专用 FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)中分配的。
从 FreeRTOS V9.0.0 开始，应用程序编写者可以选择自行提供内存，
从而使得以下对象在创建时可以选择不进行
动态内存分配：

- 任务
- 软件定时器
- 队列
- 事件组
- 二进制信号量
- 计数信号量
- 递归信号量
- 互斥锁

选择使用静态还是动态内存分配取决于
应用程序和应用程序编写者的偏好。两种方法
各有优缺点，且可以在同一个 RTOS 应用程序中同时使用。

位于 
[FreeRTOS/Source/WIN32-MSVC-Static-Allocation-Only 目录](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo) 
（在主 FreeRTOS 下载中）的简单 Win32 示例演示了如何在以下情况中创建 FreeRTOS 应用程序： 
项目中不包含任何 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)实现。


### 使用动态分配的 RAM 创建 RTOS 对象

动态创建 RTOS 对象的优势在于化繁为简，并且
有可能减少应用程序的最大 RAM 使用量：

- 创建对象时所需的函数参数较少。

- 内存分配会在 RTOS API 函数内部自动进行。

- 应用程序编写者无需担心自行分配内存。

- 如果 RTOS 对象被删除，它所使用的 RAM 可以被重新利用， 
  从而有可能减少应用程序的最大 RAM 占用。

- RTOS 提供的 API 函数可以返回堆内存使用情况的信息，帮助优化堆的大小 
  。

- 可以根据应用程序的需求选择合适的内存分配方案，
  例如 heap_1.c 提供简单且确定的分配方式，
  适用于安全关键应用；heap_4.c 提供碎片保护；heap_5.c
  支持将堆分配到多个 RAM 区域；也可以使用应用程序编写者
  提供的分配方案。

以下 API 函数 
在 [configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) 设置为 1 或未定义时可用， 
用于通过动态分配的 RAM 创建 RTOS 对象：

- [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/)
- [xQueueCreate()](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)
- [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
- [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate)
- [xSemaphoreCreateBinary()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary)
- [xSemaphoreCreateCounting()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting)
- [xSemaphoreCreateMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)
- [xSemaphoreCreateRecursiveMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)


### 使用静态分配的 RAM 创建 RTOS 对象

使用静态分配的 RAM 创建 RTOS 对象具有以下优势，可为应用程序编写者 
提供更大的控制权限：

- RTOS 对象可以放置在特定的内存位置。

- 最大 RAM 占用可以在链接时（而不是在运行时）确定。

- 应用程序编写者无需担心如何合理处理内存分配失败的情形 
  。

- 可在不允许动态内存分配的应用程序中使用 RTOS 
  （尽管 FreeRTOS 提供的分配方案有助于克服大多数反对意见）。

以下 API 函数 
在 [configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation) 设置为 1 时可用，允许使用应用程序编写者提供的内存来创建 RTOS 对象 
。要提供内存，应用程序编写者
只需声明适当对象类型的变量，然后将变量的地址传递给
RTOS API 函数即可。 
提供的 [StaticAllocation.c](https://sourceforge.net/p/freertos/code/HEAD/tree/trunk/FreeRTOS/Demo/Common/Minimal/StaticAllocation.c)
标准演示/测试任务演示了这些函数的使用方法：

- [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
- [xQueueCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic)
- [xTimerCreateStatic()](/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic)
- [xEventGroupCreateStatic()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/02-xEventGroupCreateStatic)
- [xSemaphoreCreateBinaryStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic)
- [xSemaphoreCreateCountingStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/05-xSemaphoreCreateCountingStatic)
- [xSemaphoreCreateMutexStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic)
- [xSemaphoreCreateRecursiveMutexStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/09-xSemaphoreCreateRecursiveMutexStatic)
