---
title: xTimerIsTimerActive
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
 BaseType_t xTimerIsTimerActive( TimerHandle_t xTimer );
```

查询[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)是否处于活动或休眠状态。

如果出现以下情况，定时器将处于休眠状态：

1. 已创建但尚未启动，或
2. 这是一个尚未重启的过期的一次性计时器。


定时器是在休眠状态下创建的。[xTimerStart()](/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)、
 [xTimerReset()](/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset)、
 [xTimerStartFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/09-xTimerStartFromISR)、
 [xTimerResetFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/12-xTimerResetFromISR)、
 [xTimerChangePeriod()](/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod)
 和 [xTimerChangePeriodFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR) API 函数
 都可以用于将定时器转换为活跃状态。


**参数：**

- *xTimer*

  被查询的定时器。


**返回：**

- 如果定时器处于休眠状态，将返回 pdFALSE。

- 如果定时器处于活动状态，将返回 pdFALSE 以外的值。


**用法示例：**

```c
 /* This function assumes xTimer has already been created. */
 void vAFunction( TimerHandle_t xTimer )
 {
     /* or more simply and equivalently
        "if( xTimerIsTimerActive( xTimer ) )" */
     if( xTimerIsTimerActive( xTimer ) != pdFALSE )
     {
         /* xTimer is active, do something. */
     }
     else
     {
         /* xTimer is not active, do something else. */
     }
 }
```
