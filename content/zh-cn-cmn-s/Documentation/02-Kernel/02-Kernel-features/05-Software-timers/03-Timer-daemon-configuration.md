---
title: "FreeRTOS 软件定时器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 软件定时器
relatedLinks:
  - title: API 引用 — 软件定时器
    link: /Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/
---

[[关于软件定时器的更多信息……](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

### 配置应用程序以使用软件定时器

要使 [FreeRTOS 软件计时器 API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/) 在应用程序中可用，
只需：

1. 将 FreeRTOS/Source/timers.c 源文件添加到项目中，以及
2. 在应用程序 FreeRTOSConfig.h 头文件中定义下表详述的常量。

**常量**

- configUSE_TIMERS

  设置为 1 以包括定时器功能。当 configUSE_TIMERS 设置为 1 时，
  RTOS 定时器服务任务将在调度器启动时自动创建。

- configTIMER_TASK_PRIORITY

  设置定时器服务任务的优先级。与所有任务一样，定时器服务任务可以
  在 0 到 (configMAX_PRIORITIES - 1) 之间的任何优先级运行。

  需要仔细选择此数值，以满足应用程序的要求。例如，如果
  定时器服务任务被设置为系统中最高优先级的任务，
  则发送到定时器服务任务（当调用定时器 API 函数时）和过期的定时器的命令都将立即得到处理。
  相反，如果定时器服务任务被赋予低优先级，
  则发送到定时器服务任务和过期定时器的命令将不会被处理，
  直到定时器服务任务成为能够运行的最高优先级任务。然而，值得注意的是，定时器到期时间是相对于发送命令的时间计算的，
  而不是相对于处理命令的时间计算的。

- configTIMER_QUEUE_LENGTH

  这设置了定时器命令队列在任一时间可以容纳的未处理命令的最大数量
  。定时器命令队列可能已满的原因包括：

  - 在 RTOS 调度器启动之前（即创建定时器服务任务之前）
    进行多次定时器 API 函数调用。
  - 从中断服务程序 (ISR) 进行多次（中断安全）定时器 API 函数调用。
  - 从优先级高于定时器服务任务的任务进行多次定时器 API 函数调用。

- configTIMER_TASK_STACK_DEPTH

  设置分配给定时器服务任务的堆栈大小<br /> （以字为单位，而不是以字节为单位）。定时器回调
  函数在定时器服务任务的上下文中执行。因此，定时器服务任务的堆栈要求
  取决于定时器回调函数的堆栈要求。
