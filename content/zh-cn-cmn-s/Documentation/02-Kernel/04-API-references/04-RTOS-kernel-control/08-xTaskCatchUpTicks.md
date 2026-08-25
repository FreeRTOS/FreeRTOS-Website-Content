---
title: xTaskCatchUpTicks
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
BaseType_t xTaskCatchUpTicks( TickType_t xTicksToCatchUp );
```

用于在应用程序代码长时间禁用中断后修正滴答计数值。

此函数与 [vTaskStepTick()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick) 类似， 
但与 [vTaskStepTick()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick) 不同的是，此函数可能会将滴答计数直接推进到
超过解除任务阻塞状态的时间点。这意味着 xTaskCatchUpTicks()
可能会直接解除任务的阻塞状态。


**参数：**

+ *xTicksToCatchUp* 

  由于中断被禁用而错过的滴答中断数。此值不会 
  自动计算，必须由应用程序编写者自行计算。


**返回：**

如果推进滴答计数导致任务从阻塞状态中恢复并且发生了上下文切换， 
则返回 pdTRUE，否则返回 pdFALSE。


**用法示例：**

```c
void vExampleFunction( void )
{
    unsigned long ulTimeBefore, ulTimeAfter;

    /* Read the current time before arbitrary processing takes place. */
    ulTimeBefore = ulGetExternalTime();

    /* Stop the timer that is generating the tick interrupt. */
    prvStopTickInterruptTimer();

    /* Perform some arbitrary processing. */
    arbitrary_processing();
    
    /* Read the current time for computing elapsed time since ticks 
       were disabled. */
    ulTimeAfter = ulGetExternalTime();

    if ( xTaskCatchUpTicks( ulTimeAfter - ulTimeBefore ) == pdTRUE ) 
    {
        /* Moving the tick count forward resulted in a context switch. */
    }
    
    /* Restart the timer that is generating the tick interrupt. */
    prvStartTickInterruptTimer();

}
```
