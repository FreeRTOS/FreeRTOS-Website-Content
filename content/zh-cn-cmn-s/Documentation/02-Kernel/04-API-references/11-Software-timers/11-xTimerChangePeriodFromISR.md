---
title: xTimerChangePeriodFromISR
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
 BaseType_t xTimerChangePeriodFromISR
           (
              TimerHandle_t xTimer,
              TickType_t xNewPeriod,
              BaseType_t *pxHigherPriorityTaskWoken
           );
```

可从中断服务例程调用的 [xTimerChangePeriod()](/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod)
的版本。


**参数：**

- *xTimer*

  正在更改其周期的[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)的句柄。

- *xNewPeriod*

  xTimer 的新周期。定时器周期是以滴答周期为单位指定的，因此常量 portTICK_PERIOD_MS
  可用来转换以毫秒为单位指定的时间。例如，如果定时器必须在 100 个滴答后过期，
  则 xNewPeriod 应该设置为 100。或者，如果定时器必须在 500 毫秒之后过期，
  则 xNewPeriod 可设置为 (500 / portTICK_PERIOD_MS)，前提是 configTICK_RATE_HZ 小于或
  等于 1000。

- *pxHigherPriorityTaskWoken*

  定时器服务/守护进程任务大部分时间都处于“阻塞”状态，等待消息
  到达定时器命令队列。调用 xTimerChangePeriodFromISR() 会将消息写入定时器
  命令队列，从而让定时器服务/守护进程任务转换为非阻塞状态
  。如果调用 xTimerChangePeriodFromISR() 导致定时器服务/守护进程任务退出阻塞状态，
  并且定时器服务/守护进程任务的优先级等于或高于当前执行的任务
  （被中断的任务），则 *pxHigherPriorityTaskWoken*
  将在 xTimerChangePeriodFromISR() 函数内部被设置为 pdTRUE。如果 xTimerChangePeriodFromISR() 将此值设置为 pdTRUE，
  那么应在退出中断之前执行上下文切换。


**返回：**

- 如果更改定时器周期的命令无法发送到定时器命令队列，
  则返回 pdFAIL。

- 如果能将此命令成功发送到定时器命令队列，则返回 pdPASS。

- 实际处理命令的时间取决于定时器服务/守护进程任务
  相对于系统中其他任务的优先级定时器服务/守护进程任务
  优先级由 configTIMER_TASK_PRIORITY 配置常量设置。


**用法示例：**

```c
/* This scenario assumes xTimer has already been created and started. When
   an interrupt occurs, the period of xTimer should be changed to 500ms. */

/* The interrupt service routine that changes the period of xTimer. */
void vAnExampleInterruptServiceRoutine( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* The interrupt has occurred - change the period of xTimer to 500ms.
       xHigherPriorityTaskWoken was set to pdFALSE where it was defined
       (within this function). As this is an interrupt service routine, only
       FreeRTOS API functions that end in "FromISR" can be used. */
    if( xTimerChangePeriodFromISR( xTimer,
                                   pdMS_TO_TICKS( 500 ),
                                   &xHigherPriorityTaskWoken ) != pdPASS )
    {
        /* The command to change the timers period was not executed
           successfully. Take appropriate action here. */
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
