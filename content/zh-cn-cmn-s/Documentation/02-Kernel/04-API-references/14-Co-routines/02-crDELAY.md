---
title: crDELAY
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[协程专用](/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
void crDELAY( CoRoutineHandle_t xHandle,
              TickType_t xTicksToDelay )
```

`crDELAY` 是一个宏。上面原型中的数据类型仅供参考。

将协程延迟一段固定时间。

`crDELAY` 只能从协程函数本身调用，不能
从协程函数调用的函数调用。这是因为
协程无法维持自己的堆栈。

**参数：**

- *xHandle*

  要推迟协程的句柄。这是协程函数的 xHandle 参数。

- *xTickToDelay*

  协程应推迟的滴答数。此滴答数可以转换为实际时间，实际时间
  由 `configTICK_RATE_HZ` （在 FreeRTOSConfig.h 中设置）定义。可以通过常量 `portTICK_PERIOD_MS`
  将滴答数转换为毫秒。

**用法示例：**

```c
// Co-routine to be created.
void vACoRoutine( CoRoutineHandle_t xHandle,
                  UBaseType_t uxIndex )
{
    // Variables in co-routines must be declared static if they must maintain
    // value across a blocking call. This may not be necessary for const
    // variables. We are to delay for 200ms.
    static const xTickType xDelayTime = 200 / portTICK_PERIOD_MS;

    // Must start every co-routine with a call to crSTART();
    crSTART( xHandle );

    for( ;; )
    {
        // Delay for 200ms.
        crDELAY( xHandle, xDelayTime );

        // Do something here.
    }

    // Must end every co-routine with a call to crEND();
    crEND();
}
```

