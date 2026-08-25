---
title: vTimerSetTimerID
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
 void vTimerSetTimerID( TimerHandle_t xTimer, void *pvNewID );
```

创建定时器时，会为[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)分配一个标识符 (ID)，
您随时可以使用 `vTimerSetTimerID()` API 函数更改此 ID。

如果将同一个回调函数分配给多个定时器，
则可以在回调函数内检查定时器标识符，
以确定哪个定时器实际已到期。

在定时器回调函数的调用之间，定时器标识符也可用于将数据存储在定时器中
。


**参数：**

- *xTimer*

  更新的计时器。


- *pvNewID*

  句柄，定时器标识符将被设置为此句柄。


**用法示例：**

```c
/* A callback function assigned to a timer. */
void TimerCallbackFunction( TimerHandle_t pxExpiredTimer )
{
uint32_t ulCallCount;

    /* A count of the number of times this timer has expired
       and executed its callback function is stored in the
       timer's ID. Retrieve the count, increment it, then save
       it back into the timer's ID. */
    ulCallCount =
        ( uint32_t ) [pvTimerGetTimerID](/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID)( pxExpiredTimer );
    ulCallCount++;
    vTimerSetTimerID( pxExpiredTimer, ( void * ) ulCallCount );
}
```
