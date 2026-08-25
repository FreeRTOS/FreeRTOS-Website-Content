---
title: vCoRoutineSchedule
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
void vCoRoutineSchedule( void );
```

运行协程。

`vCoRoutineSchedule()` 执行优先级最高的可运行协程
。协程保持执行，直到它阻塞、挂起或
被任务抢占。协同间互相协作执行，因此
一个协程无法被另一个协程抢占，但可以被一个任务抢占。

如果应用程序同时包含任务和协程，那么
应从空闲任务（在空闲任务钩子中）调用 `vCoRoutineSchedule`
。


**用法示例：**

```c
    void vApplicationIdleHook( void )
    {
        vCoRoutineSchedule( void );
    }
```

如果空闲任务没有执行任何其他函数，那按以下方式在循环中调用
`vCoRoutineSchedule()`：

```c
    void vApplicationIdleHook( void )
    {
        for( ;; )
        {
            vCoRoutineSchedule( void );
        }
    }
```

