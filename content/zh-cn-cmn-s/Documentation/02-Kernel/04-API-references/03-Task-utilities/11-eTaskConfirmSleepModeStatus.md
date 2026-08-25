---
title: eTaskConfirmSleepModeStatus
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 内核控制](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h

```c
 eSleepModeStatus eTaskConfirmSleepModeStatus( void );
```

无滴答空闲模式的特定函数。

提供此函数在 [portSUPPRESS_TICKS_AND_SLEEP()](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) 中使用，
以允许移植特定的睡眠函数确定是否可以继续睡眠，以及是否可以无限期睡眠。

该函数是必要的，因为 `portSUPPRESS_TICKS_AND_SLEEP()` 只在调度器挂起时被调用， 
而不是从临界区内被调用。因此， 
中断有可能要求在调用 `portSUPPRESS_TICKS_AND_SLEEP()` 和实际进入低功耗模式之间进行上下文切换。
`eTaskConfirmSleepModeStatus()` 应在定时器停止和进入睡眠模式之间的短暂临界区内调用 
。

必须将 `configUSE_TICKLESS_IDLE` 配置常量设置为 1，`eTaskConfirmSleepModeStatus()` 
才可用。


**参数：** 

无。


**返回：** 

如果在调用 `portSUPPRESS_TICKS_AND_SLEEP()` 后，任务已从阻塞状态转出， 
或上下文切被挂起（因为调度器被暂停），则 `eTaskConfirmSleepModeStatus()` 将返回 
`eAbortSleep`，且不得进入睡眠模式。

如果未使用软件定时器，并且所有应用任务都被无限期超时阻塞或挂起， 
那么 `eTaskConfirmSleepModeStatus()` 将返回 `eNoTasksWaitingTimeout`， 
`portSUPPRESS_TICKS_AND_SLEEP()` 可以进入深度睡眠状态，而无需首先配置一个定时器， 
使微控制器在未来某个预定时间从睡眠状态中脱离。

在所有其他情况下，`eTaskConfirmSleepModeStatus()` 将返回 `eStandardSleep`。


**用法示例：**

`eTaskConfirmSleepModeStatus()` 用于 
[portSUPPRESS_TICKS_AND_SLEEP() 的实现示例。](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support/#the-portsuppress_ticks_and_sleep-macro)
  
