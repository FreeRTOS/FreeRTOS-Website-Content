---
title: xTimerStopFromISR
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
 BaseType_t xTimerStopFromISR
             (
                 TimerHandle_t xTimer,
                 BaseType_t *pxHigherPriorityTaskWoken
             );
```

可从中断服务例程调用的 [xTimerStop()](/Documentation/02-Kernel/04-API-references/11-Software-timers/05-xTimerStop)
的版本。


**参数：**

- *xTimer*

  正在停止的定时器的句柄。

- *pxHigherPriorityTaskWoken*

  定时器服务/守护进程任务大部分时间都处于“阻塞”状态，等待消息
  到达定时器命令队列。调用 `xTimerStopFromISR()` 会将消息写入定时器命令
  队列，从而让定时器服务/守护进程任务转换为非阻塞状态。如果
  调用 `xTimerStopFromISR()` 导致定时器服务/守护进程任务退出阻塞状态，并且
  定时器服务/守护进程任务的优先级等于或高于当前执行的任务
  （被中断的任务），则 `pxHigherPriorityTaskWoken` 将被设置为 `pdTRUE`
  （从 `xTimerStopFromISR()` 函数内部设置）。如果 `xTimerStopFromISR()` 将此值设置为 `pdTRUE`，
  那么应在退出中断之前执行上下文切换。


**返回：**

- *pdFAIL*

  如果无法向定时器命令队列发送停止命令，则返回 `pdFAIL`。

- *pdPASS*

  如果命令成功发送至定时器命令队列，则返回 `pdPASS`
  。实际处理命令的时间
  取决于定时器服务/守护进程任务相对于系统中其他任务的
  优先级。定时器服务/守护进程
  任务的优先级由 `configTIMER_TASK_PRIORITY` 配置常量设置。


**用法示例：**

```c
/* This scenario assumes xTimer has already been created and started. When
   an interrupt occurs, the timer should be simply stopped. */

/* The interrupt service routine that stops the timer. */
void vAnExampleInterruptServiceRoutine( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* The interrupt has occurred - simply stop the timer.
       xHigherPriorityTaskWoken was set to pdFALSE where it was defined
       (within this function). As this is an interrupt service routine, only
       FreeRTOS API functions that end in "FromISR" can be used. */
    if( xTimerStopFromISR( xTimer, &xHigherPriorityTaskWoken ) != pdPASS )
    {
        /* The stop command was not executed successfully. Take appropriate
           action here. */
    }

    /* If xHigherPriorityTaskWoken equals pdTRUE, then a context switch
       should be performed. The syntax required to perform a context switch
       from inside an ISR varies from port to port, and from compiler to
       compiler. Inspect the demos for the port you are using to find the
       actual syntax required. */
    if( xHigherPriorityTaskWoken != pdFALSE )
    {
        /* Call the interrupt safe yield function here (actual function
           depends on the FreeRTOS port being used). */
    }
}
```
