---
title: vTaskSuspendAll
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 内核控制](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task. h 

```c
void vTaskSuspendAll( void );
```

挂起调度器。挂起调度器会阻止上下文切换， 
但会让中断处于启用状态。如果调度器被挂起时，中断请求切换上下文， 
那么请求将会被挂起。而且只有在调度器恢复（取消挂起）时才会执行。

在以下情况下调用 [xTaskResumeAll()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/06-xTaskResumeAll) 会转换调度器的状态，取消其阻塞状态： 
在 `vTaskSuspendAll()` 之后调用。

对 `vTaskSuspendAll()` 的调用可以嵌套。调用 `xTaskResumeAll()` 的次数 
必须与先前调用 `vTaskSuspendAll()` 的次数相同， 
然后调度器将取消挂起状态并重新进入活动状态。

`xTaskResumeAll()` 只能在正在执行的任务中调用， 
因此不能在调度器处于初始化状态时（启动调度器之前）调用。

不得在调度器挂起时调用其他 FreeRTOS API 函数。

调度器挂起时，禁止调用可能切换上下文的 API 函数（例如 `vTaskDelayUntil()`、`xQueueSend()` 
等等）。****


**用法示例：**

```c
/* A function that suspends then resumes the scheduler. */
void vDemoFunction( void )
{
    /* This function suspends the scheduler. When it is called from vTask1 the 
       scheduler is already suspended, so this call creates a nesting depth of 2. */
    vTaskSuspendAll();

    /* Perform an action here. */

    /* As calls to vTaskSuspendAll() are nested, resuming the scheduler here will 
       not cause the scheduler to re-enter the active state. */
    xTaskResumeAll();
}


void vTask1( void * pvParameters )
{
    for( ;; )
    {
        /* Perform some actions here. */

        /* At some point the task wants to perform an operation during which it does 
           not want to get swapped out, or it wants to access data which is also 
           accessed from another task (but not from an interrupt). It cannot use
           taskENTER_CRITICAL()/taskEXIT_CRITICAL() as the length of the operation may
           cause interrupts to be missed. */

        /* Prevent the scheduler from performing a context switch. */
        vTaskSuspendAll();

        /* Perform the operation here. There is no need to use critical sections as 
           the task has all the processing time other than that utilized by interrupt 
           service routines.*/ 

        /* Calls to vTaskSuspendAll() can be nested so it is safe to call a (non API) 
           function which also contains calls to vTaskSuspendAll(). API functions 
           should not be called while the scheduler is suspended. */
        vDemoFunction();

        /* The operation is complete. Set the scheduler back into the Active 
           state. */
        if( xTaskResumeAll() == pdTRUE )
        {
            /* A context switch occurred within xTaskResumeAll(). */
        }
        else
        {
            /* A context switch did not occur within xTaskResumeAll(). */
        }
    }
}
```
