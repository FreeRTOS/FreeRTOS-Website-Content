---
title: "任务和协程"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 任务和协程的概念
relatedLinks:
  - title: API 引用——任务创建
    link: /Documentation/02-Kernel/04-API-references/01-Task-creation/00-TaskHandle/
  - title: API 引用——任务控制
    link: /Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control/
  - title: API 引用——任务实用程序
    link: /Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/
---

有关多任务基本概念的介绍，请参阅 [FreeRTOS 的工作原理](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation)部分。

[任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview/)
与[协程](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview/)
文件页面提供相关信息，帮助您确定何时使用协程是恰当的，何时使用协程
是不恰当的。以下是简要总结。请注意，单纯使用任务或协程，或者结合使用任务与协程
均可设计应用程序——不过，任务与协程使用不同的 API 函数，因此
不可通过队列（或信号量）在任务和协程之间传递数据。

协程实际上仅用于具有严格 RAM 限制的非常小型的处理器。


### “任务”的特点

**简而言之**：使用 RTOS 的实时应用程序可以构建为一组独立的任务。每个任务
在自己的上下文中执行，不会碰巧依赖于系统内的其他任务或 RTOS 调度器
本身。在任何时间点，应用程序中只能执行一个任务，实时 RTOS 调度器
负责决定应该执行哪个任务。因此 RTOS 调度器可能在应用程序执行过程中
反复启动并停止每个任务（换入并换出每个任务）。由于任务不了解 RTOS 调度器的
情况，实时 RTOS 调度器须确保换入任务时，处理器的上下文（寄存器
值、堆栈内容等）与换出该任务时完全相同。
为实现这一点，每个任务都分配有自己的堆栈。换出任务时，执行上下文
被保存到该任务的堆栈中，以便以后再换入相同的任务时可以准确地恢复其执行上下文。请参阅
[FreeRTOS 的工作原理](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/01-RTOS-implementation)部分，以获取更多信息。


#### 任务总结

+ 操作简单。

+ 没有使用限制。

+ 支持完全抢占式机制。

+ 完全按优先顺序排列。

+ 每个任务都保留自己的堆栈，从而提高 RAM 使用率。

+ 如果使用抢占式机制，则必须谨慎考虑重入问题。


### “协程”的特点

**请注意：**协程是为了在非常小型的设备上使用而实现的，但现在很少在实际情况中使用。
因此尽管没有计划从代码中删除协程，但也没有计划进一步开发
这些协程。

协程在概念上类似于任务，但有以下根本差异（详述在
[协程文档页面](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview/)）：

1. **堆栈使用**

   应用程序中的所有协程共用一个堆栈。与使用任务编写的类似应用程序相比，这样所需的 RAM 
   大大减少。

2. **调度和优先级**

   协程间使用优先级协同调度，但可以包含在使用抢占式任务
   的应用程序中。

3. **宏实现**

   协程是通过一组宏实现的。

4. **使用限制**

   减少 RAM 使用是以一些严格限制协程构造为代价的。


#### 协程总结

+ 协程间共享堆栈导致 RAM 使用率大大降低。

+ 协作操作减少了重入问题。

+ 可以在不同架构间移植。

+ 相对于其他协程完全优先，但如果混用协程和任务，那么总是会被任务抢占。

+ 需要特别考虑堆栈不足的问题。

+ 对 API 调用位置有限制。

+ 只在协程间进行协作操作。
