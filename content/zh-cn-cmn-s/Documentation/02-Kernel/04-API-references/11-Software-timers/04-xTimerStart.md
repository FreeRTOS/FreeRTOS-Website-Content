---
title: xTimerStart
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
 BaseType_t xTimerStart( TimerHandle_t xTimer,
                            TickType_t xBlockTime );
```

[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)功能由定时器服务/守护进程任务提供。许多
公共 FreeRTOS 定时器 API 函数通过定时器命令队列
向定时器服务任务发送命令。定时器命令队列是
RTOS 内核本身的私有队列，
。定时器命令队列的长度由 `configTIMER_QUEUE_LENGTH` 配置常量设置。

`xTimerStart()` 启动之前使用 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
API 函数创建的定时器。如果定时器已经启动且已处于活跃状态，
则 `xTimerStart()` 具有与 [xTimerReset()](/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset) API 函数相同的功能。

启动定时器可确保定时器处于活跃状态。如果定时器
在此期间没有被停用、删除或重置，
那么在调用 `xTimerStart()` 并经过了 “n” 个滴答之后，将调用与定时器相关联的回调函数，
其中 “n” 表示规定的定时器周期。

在 RTOS 调度器启动之前调用 `xTimerStart()` 是有效的，
但是完成此操作后，直到启动 RTOS 调度器之前，定时器都不会真正启动，
并且定时器的到期时间与 RTOS 调度器的启动时间有关，
与调用 `xTimerStart()` 的时间无关。

必须将 `configUSE_TIMERS` 配置常量设置为 1，`xTimerStart()`
 才可用。


**参数：**

- *xTimer*

  正在启动/重新启动的定时器的句柄。

- *xBlockTime*

  指定
  在
  调用 `xTimerStart()` 时队列已满的情况下，调用任务处于阻塞状态以等待启动命令成功发送到定时器命令队列的时间（单位：滴答）。在以下情况下，`xBlockTime` 将被忽略：`xTimerStart()`
  在 RTOS 调度器启动之前就被调用。


**返回：**

- 如果在以下情况下，启动命令无法发送至定时器命令队列，则返回 `pdFAIL`：
  即使在经过 `xBlockTime` 个滴答后。

- 如果能将此命令成功发送到定时器命令队列，则返回 `pdPASS`。

  实际处理命令的时间取决于
  定时器服务/守护进程任务相对于系统中其他任务的优先级，
  尽管定时器到期时间与实际调用 `xTimerStart(` 的时间有关。定时器服务/守护进程任务的优先级
  由 `configTIMER_TASK_PRIORITY`
  配置常量设置。


**用法示例：**

请参阅 [xTimerCreate() 文档页面](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)上的示例。
