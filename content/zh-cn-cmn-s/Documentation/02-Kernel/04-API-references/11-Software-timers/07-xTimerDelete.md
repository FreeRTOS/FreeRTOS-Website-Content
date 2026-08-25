---
title: xTimerDelete
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[定时器 API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/)]

timers.h


```c
 BaseType_t xTimerDelete( TimerHandle_t xTimer,
                          TickType_t xBlockTime );
```

[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)功能由定时器服务/守护进程任务提供。许多
公共 FreeRTOS 定时器 API 函数通过一个名为
“定时器命令队列”的队列向定时器服务任务发送命令。定时器命令队列对 RTOS 内核本身是私有的，
应用程序代码无法直接访问。定时器命令队列的长度由 configTIMER_QUEUE_LENGTH
配置常量设置。

xTimerDelete() 可删除之前使用 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
API 函数创建的定时器。请注意，删除静态分配的定时器时，
在 [xTimerIsTimerActive()](/Documentation/02-Kernel/04-API-references/11-Software-timers/03-xTimerIsTimerActive) 指示该定时器处于非活动状态之前，无法重复使用其静态内存。

configUSE_TIMERS 配置常量必须设置为 1，xTimerDelete() 才可用。


**参数：**

- *xTimer*

  正在删除的定时器的句柄。

- *xBlockTime*

  指定在调用 xTimerDelete() 时队列已满的情况下，
  调用任务处于阻塞状态以等待删除命令成功发送到定时器命令队列的时间
  （单位：滴答）。如果
  在 RTOS 调度器启动前调用 xTimerDelete()，xBlockTime 将被忽略。


**返回：**

- 如果在 xBlockTime 滴答已过之后仍无法向定时器命令队列发送删除命令，
  则返回 pdFAIL。

- 如果能将此命令成功发送到定时器命令队列，则返回 pdPASS。实际处理命令的时间
  取决于定时器服务/守护进程任务相对于系统中其他任务的优先级
  。定时器服务/守护进程任务的优先级由 configTIMER_TASK_PRIORITY
  配置常量设置。


**用法示例：**

请参阅 [xTimerChangePeriod() 文档页面](/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod)上的示例。
