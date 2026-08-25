---
title: xTimerGetPeriod
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
 TickType_t xTimerGetPeriod( TimerHandle_t xTimer );
```

返回[软件计时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)的周期。周期以滴答为单位。

定时器的周期最初是通过调用
[xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/) 创建定时器时使用的 xTimerPeriod 参数来设置的。可以使用
[xTimerChangePeriod()](/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod) 和 [xTimerChangePeriodFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR) API 函数来更改周期。


**参数：**

- *xTimer*

  被查询的定时器。


**返回：**

- 定时器的周期，以滴答为单位。


**用法示例：**

```c
/* A callback function assigned to a software timer. */
static void prvExampleTimerCallback( TimerHandle_t xTimer )
{
TickType_t xTimerPeriod;

    /* Query the period of the timer that expires. */
    xTimerPeriod = xTimerGetPeriod( xTimer );
}
```
