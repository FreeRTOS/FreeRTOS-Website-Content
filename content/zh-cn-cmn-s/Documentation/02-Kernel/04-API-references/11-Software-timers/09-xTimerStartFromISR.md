---
title: xTimerStartFromISR
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
 BaseType_t xTimerStartFromISR
               (
                  TimerHandle_t xTimer,
                  BaseType_t *pxHigherPriorityTaskWoken
               );
```

可从中断服务例程调用的 [xTimerStart()](/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)
的版本。


**参数：**

+ *xTimer*

  正在启动/重新启动的定时器的句柄。

+ *pxHigherPriorityTaskWoken*

  定时器服务/守护进程任务大部分时间都处于“阻塞”状态，等待消息
  到达定时器命令队列。调用 xTimerStartFromISR() 会将消息写入定时器命令
  队列，从而让定时器服务/守护进程任务转换为非阻塞状态。如果
  调用 xTimerStartFromISR() 导致定时器服务/守护进程任务退出阻塞状态，并且
  定时器服务/守护进程任务的优先级等于或高于当前执行的任务
  （被中断的任务），则 \*pxHigherPriorityTaskWoken
  将在 xTimerStartFromISR() 函数内部被设置为 pdTRUE。如果 xTimerStartFromISR () 将此值设置为 pdTRUE，
  那么应在退出中断之前执行上下文切换。


**返回：**

 如果启动命令无法发送至定时器命令队列，
 则返回 pdFAIL。如果命令成功发送至定时器命令队列，
 则返回 pdPASS。实际处理命令的时间
 取决于定时器服务/守护进程任务相对于系统中其他任务的优先级，
 尽管定时器到期时间
 是相对于实际调用 xTimerStartFromISR() 的时间而言。定时器服务/守护进程
 任务优先级由 configTIMER_TASK_PRIORITY 配置常量设置。


**用法示例：**

```c
/* This scenario assumes xBacklightTimer has already been created. When a
   key is pressed, an LCD back-light is switched on. If 5 seconds pass
   without a key being pressed, then the LCD back-light is switched off. In
   this case, the timer is a one-shot timer, and unlike the example given for
   the xTimerReset() function, the key press event handler is an interrupt
   service routine. */

/* The callback function assigned to the one-shot timer. In this case the
   parameter is not used. */
void vBacklightTimerCallback( TimerHandle_t pxTimer )
{
    /* The timer expired, therefore 5 seconds must have passed since a key
       was pressed. Switch off the LCD back-light. */
    vSetBacklightState( BACKLIGHT_OFF );
}

/* The key press interrupt service routine. */
void vKeyPressEventInterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* Ensure the LCD back-light is on, then restart the timer that is
       responsible for turning the back-light off after 5 seconds of
       key inactivity. This is an interrupt service routine so can only
       call FreeRTOS API functions that end in "FromISR". */
    vSetBacklightState( BACKLIGHT_ON );

    /* xTimerStartFromISR() or xTimerResetFromISR() could be called here
       as both cause the timer to re-calculate its expiry time.
       xHigherPriorityTaskWoken was initialised to pdFALSE when it was
       declared (in this function). */
    if( xTimerStartFromISR( xBacklightTimer,
        &xHigherPriorityTaskWoken ) != pdPASS )
    {
        /* The start command was not executed successfully. Take appropriate
           action here. */
    }

    /* Perform the rest of the key processing here. */

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
