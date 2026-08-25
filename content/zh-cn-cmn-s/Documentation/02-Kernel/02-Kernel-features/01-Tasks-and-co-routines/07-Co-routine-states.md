---
title: "FreeRTOS 协程"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: API 引用——协程
    link: /Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine API/
  - title: 协程示例
    link: /Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Co-routine-example/
---

[[更多关于协程的信息……](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### 协程状态

协程仅用于 RAM 严重受限的极小处理器，
通常不会用于 32 位微控制器。协程可以存在于以下状态中：

* **运行**   

  当协程实际执行时，它被称为处于运行状态。协程当前正在使用处理器。
  
* **就绪**   

  就绪的协程是那些能够执行（未阻塞）但目前未执行的协程。 
  协程处于就绪状态的可能情况包括：

  1. 另一个具有相同或更高优先级的协程已处于运行状态，或
  2. 任务处于运行状态——只有在应用程序同时使用任务和协程时才会出现这种情况。
     
* **阻塞**   

  如果协程当前正在等待时间事件或外部事件，则该协程被称为处于阻塞状态 
  。例如，如果协程调用 crDELAY()，它将阻塞（被置于阻塞状态）， 
  直到延迟期结束（即时间事件）。阻塞的协程不可用于 
  调度。

当前没有等同于任务挂起状态的协程。

![](/media/2018/crstate.gif)**有效的协程状态转换**  
