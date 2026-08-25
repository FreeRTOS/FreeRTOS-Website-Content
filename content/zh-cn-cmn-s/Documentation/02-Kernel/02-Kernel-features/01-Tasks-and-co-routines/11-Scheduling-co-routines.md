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


### 调度协程

通过重复调用 [vCoRoutineSchedule()](/Documentation/02-Kernel/04-API-references/14-Co-routines/07-vCoRoutineSchedule)来调度协程。调用 vCoRoutineSchedule() 
的最佳位置为[空闲任务钩子](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task)。即使应用程序
仅使用协程也是如此，因为一旦启动调度器，将仍然会自动
创建空闲任务。[请参阅后续示例](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Scheduling-co-routines)。

---
### 混合任务和协程

从空闲任务中调度协程，可在同一应用程序中轻松混合任务和
协程。这种情况下，只有在没有优先级高于
空闲任务的任务可以执行时，协程才会执行。

[请参阅后续示例](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Scheduling-co-routines)。
