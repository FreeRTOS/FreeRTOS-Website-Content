---
title: "延迟中断处理"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 延迟中断处理相关信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


### 什么是延迟中断处理？

在 FreeRTOS 中，延迟中断处理程序指的是被中断服务程序 (ISR) 解除阻塞（触发）的 RTOS 任务，
因此中断所需要的处理可以在解除阻塞的任务中执行，
而不是直接在 ISR 中执行
。该机制与标准中断处理不同，
在标准中断处理中，所有处理都是在 ISR 中进行的，
因为大部分处理都被延迟到 ISR 退出之后：

* **标准 ISR 处理** 

  标准 ISR 处理通常包括在 ISR 本身内记录中断的原因，清除中断，
  然后执行中断所需的任何处理。

* **延迟中断处理** 

  延迟中断处理通常包括记录中断的原因，
  并在 ISR 中清除中断，
  但随后解除 RTOS 任务的阻塞，
  因此中断所需的处理可以由解除阻塞的任务执行，而不是在 ISR 中执行。

  如果中断处理被延迟的任务被分配了足够高的优先级，
  那么 ISR 将直接返回到未被阻塞的任务
  （中断将中断一个任务，但随后返回到另一个任务），
  结果是中断所需的所有处理在时间上
  被连续执行（没有间隙），
  就像所有处理都在 ISR 本身中执行一样。可以在下图中看到这一点，
  所有中断处理都发生在时间 t2 和 t4 之间，
  尽管部分处理是由一个任务执行的。

  ![使用 rtos 延迟中断处理](/media/2018/rtos_deferred_interrupt_processing.jpg)   
  *延迟处理任务具有高优先级时的延迟中断处理执行顺序* 

  参照上述图片：

  1. 在时间 t2 时：低优先级任务被中断抢占。

  2. 在时间 t3 时：ISR 直接返回到从 ISR 中解除阻塞的任务
     。大多数中断处理是在未被阻塞的任务内执行的。

  3. 在时间 t4 时：被 ISR 解除阻塞状态的任务返回
     阻塞状态以等待下一次中断，同时允许较低
     优先级应用程序任务继续执行。


### 何时使用延迟中断处理

大多数嵌入式工程师会努力减少在 ISR 中花费的时间
（以尽量减少系统中的抖动，使其他相同或更低优先级的中断得以执行，
最大限度地提高中断响应性等等），
而将中断处理延迟到任务的技术提供了实现这一目标的方便方法
。但是，首先解除阻塞，
然后切换到 RTOS 任务本身需要有限的时间，所以通常情况下，
只有当处理满足以下条件时，应用程序才能从延迟中断处理中受益：

* 需要执行冗长的操作，或

* 可以使用完整的 RTOS API，而不是仅使用 ISR 安全的 API，或者

* 需要在合理范围内执行一个不确定的操作。


### 将中断处理延迟到任务的技术

将中断延迟到任务的方法可分为两类：

1. **集中式延迟中断处理** 

   集中式延时中断处理之所以被称为集中式延时中断处理，是因为使用这种方法的每个中断 
   在相同 RTOS 守护进程任务的上下文中执行。RTOS 守护进程任务由 FreeRTOS 创建， 
   也称为[定时器服务任务](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)。

   要将中断处理延迟到 RTOS 守护进程任务，需要传递中断处理函数的一个指针 
   作为 
   [xTimerPendFunctionCallFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/18-xTimerPendFunctionCallFromISR) API 函数调用中的 xFunctionToPend 参数。请参阅 
   xTimerPendFunctionCallFromISR() 文档页面以获取有效示例。

   集中式延迟中断处理的优点包括资源使用量极少，
   这是因为每个延迟中断处理程序均使用相同的任务。

   集中式延迟中断处理的缺点包括：

   * 所有延迟中断处理函数都在
     同一个 RTOS 守护进程任务的上下文中执行，因此它们会以相同的 RTOS 任务优先级执行
     。

   * xTimerPendFunctionCallFromISR() 通过定时器命令队列
     向 RTOS守护进程任务发送指向延迟中断处理函数的指针
     。因此，RTOS 守护进程任务
     会按照在队列中收到的顺序，
     而不一定是按照中断的优先顺序来处理这些函数。

   * 写入定时器命令队列，然后再从该队列中读取，
     会增加一个额外的延迟。

2. **应用程序控制延迟中断处理** 

   应用程序控制延迟中断处理之所以被称为应用程序控制延迟中断处理，是因为使用这种方法的每个中断 
   都在应用程序编写者创建的任务上下文中执行。请参阅 
   [将 RTOS 任务通知用作轻量级计数信号量](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)
   文档页面以获取有效示例。

   应用程序控制延迟中断处理的优点包括：

   * 减少了延迟（函数指针不通过队列传递）。

   * 能够为每个延迟中断处理
     RTOS 任务分配不同的优先级——
     可使延迟中断任务的相对优先级
     与它们各自中断的相对优先级相匹配。
    
   应用程序控制延迟中断处理的缺点包括
   更多的资源消耗，因为通常需要更多的任务。
