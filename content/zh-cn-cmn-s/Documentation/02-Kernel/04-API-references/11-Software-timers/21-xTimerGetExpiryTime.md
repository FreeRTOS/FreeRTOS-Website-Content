---
title: xTimerGetExpiryTime
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
 TickType_t xTimerGetExpiryTime( TimerHandle_t xTimer );
```

返回[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)到期的时间，
即执行定时器回调函数的时间。

如果 xTimerGetExpiryTime() 返回的值小于当前时间，
则定时器将在 tick 计数溢出并返回 0 时失效。
计数溢出在 RTOS 实现中进行处理，
因此定时器的回调函数会在正确时间执行，
无论是在 tick 计数溢出之前还是之后。


**参数：**

- *xTimer*

  被查询的定时器。


**返回：**

- 如果 xTimer 引用的定时器处于[活动](/Documentation/02-Kernel/04-API-references/11-Software-timers/03-xTimerIsTimerActive)状态，
  则会返回定时器下次到期的时间（可能是在当前 tick 计数溢出后，
  请参阅上文的注释）。

- 如果 xTimer 引用的定时器未处于活动状态，
  则未定义返回值。


**用法示例：**

```c
static void prvAFunction( TimerHandle_t xTimer )
{
TickType_t xRemainingTime;

    /* Calculate the time that remains before the timer referenced by xTimer
       expires. TickType_t is an unsigned type, so the subtraction will result in
       the correct answer even if the timer will not expire until after the tick
       count has overflowed. */
    xRemainingTime = xTimerGetExpiryTime( xTimer ) - xTaskGetTickCount();
}
```
