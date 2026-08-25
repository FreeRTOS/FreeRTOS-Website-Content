---
title: xTimerStop
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
 BaseType_t xTimerStop( TimerHandle_t xTimer,
                        TickType_t xBlockTime );
```

[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)功能由定时器服务/守护进程任务提供。许多
公共 FreeRTOS 定时器 API 函数通过定时器命令队列
向定时器服务任务发送命令。定时器命令队列是
RTOS 内核本身的私有队列，
应用程序代码无法直接访问该队列。定时器命令队列的长度
由 configTIMER_QUEUE_LENGTH 配置常量设置。

xTimerStop() 停止先前使用
 [xTimerStart()](/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)、
 [xTimerReset()](/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset)、
 [xTimerStartFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/09-xTimerStartFromISR)、
 [xTimerResetFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/12-xTimerResetFromISR)、
 [xTimerChangePeriod()](/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod)
 和 [xTimerChangePeriodFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR) API 函数创建的定时器。

停用定时器可确保定时器不处于活跃状态。

`configUSE_TIMERS` 配置常量必须设置为 1，xTimerStop()
才可用。


**参数：**

- *xTimer*

  正在停止的定时器的句柄。

- *xBlockTime*

  指定在调用
  `xTimerStop()` 时队列已满的情况下，调用任务处于阻塞状态以等待停止命令成功发送到定时器命令队列的时间（单位：滴答）。
  如果在启动 RTOS 调度器之前就已调用 `xTimerStop()`，则 `xBlockTime` 会被忽略。


**返回：**

- *pdFAIL*

  如果在 xBlockTime 滴答已过之后仍无法向定时器命令队列发送删除命令，则返回 `pdFAIL`
  。

- *pdPASS*

  如果能将此命令成功发送到定时器命令队列，则返回 `pdPASS`。
  实际处理命令的时间取决于
  定时器服务/守护进程任务相对于系统中其他任务的优先级。定时器服务/守护进程任务的优先级
  由 `configTIMER_TASK_PRIORITY`
  配置常量设置。


**用法示例：**

请参阅 [xTimerCreate() 文档页面](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)上的示例。
