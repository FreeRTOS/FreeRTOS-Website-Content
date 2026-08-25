---
title: xTimerReset
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
 BaseType_t xTimerReset( TimerHandle_t xTimer,
                         TickType_t xBlockTime );
```

[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)功能由定时器服务/守护进程任务提供。许多
公共 FreeRTOS 定时器 API 函数通过定时器命令队列
向定时器服务任务发送命令。定时器命令队列是
RTOS 内核本身的私有队列，
。定时器命令队列的长度由 `configTIMER_QUEUE_LENGTH` 配置常量设置。

`xTimerReset()` 重启之前使用 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
API 函数创建的定时器。如果定时器已经启动且已处于活跃状态，则 `xTimerReset()`
将使定时器重新评估其到期时间，因此到期时间与 `xTimerReset()`
的调用时间有关。如果定时器处于休眠状态，那么 `xTimerReset()` 的功能
与 [xTimerStart()](/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart) API 函数相同。

重置定时器可确保定时器处于活跃状态。如果定时器
在此期间没有被停用、删除或重置，
那么在调用 `xTimerReset()` 并经过了 “n” 个滴答之后，将调用与定时器相关联的回调函数，
其中 “n” 表示规定的定时器周期。

在 RTOS 调度器启动之前调用 `xTimerReset()` 是有效的，
但是完成此操作后，直到启动 RTOS 调度器之前，定时器都不会真正启动，
并且定时器的到期时间与 RTOS 调度器的启动时间有关，
与调用 `xTimerReset()` 的时间无关。

必须将 `configUSE_TIMERS` 配置常量设置为 1，`xTimerReset()`
才可用。


**参数：**

- *xTimer*

  正在重置/启动/重新启动的定时器的句柄。

- *xBlockTime*

  指定
  在
  调用 `xTimerReset()` 时队列已满的情况下，调用任务处于阻塞状态以等待停止命令成功发送到定时器命令队列的时间（单位：滴答）。在以下情况下，`xBlockTime` 将被忽略：`xTimerReset()`
  在 RTOS 调度器启动之前就被调用。


**返回：**

- 如果在以下情况下，重置命令无法发送至定时器命令队列，则返回 `pdFAIL`：
  经过 `xBlockTime` 个滴答之后。

- 如果能将此命令成功发送到定时器命令队列，则返回 `pdPASS`
  。实际处理命令的时间取决于
  定时器服务/守护进程任务相对于系统中其他任务的优先级，
  尽管定时器到期时间与实际调用 `xTimerReset()` 的时间有关。定时器服务/守护进程任务的优先级
  由 `configTIMER_TASK_PRIORITY`
  配置常量设置。


**用法示例：**

```c
/* When a key is pressed, an LCD back-light is switched on. If 5 seconds pass
   without a key being pressed, then the LCD back-light is switched off. In
   this case, the timer is a one-shot timer. */

TimerHandle_t xBacklightTimer = NULL;

/* The callback function assigned to the one-shot timer. In this case the
   parameter is not used. */
void vBacklightTimerCallback( TimerHandle_t pxTimer )
{
    /* The timer expired, therefore 5 seconds must have passed since a key
       was pressed. Switch off the LCD back-light. */
    vSetBacklightState( BACKLIGHT_OFF );
}

/* The key press event handler. */
void vKeyPressEventHandler( char cKey )
{
    /* Ensure the LCD back-light is on, then reset the timer that is
       responsible for turning the back-light off after 5 seconds of
       key inactivity. Wait 10 ticks for the command to be successfully sent
       if it cannot be sent immediately. */
    vSetBacklightState( BACKLIGHT_ON );
    if( xTimerReset( xBacklightTimer, 10 ) != pdPASS )
    {
        /* The reset command was not executed successfully. Take appropriate
           action here. */
    }

    /* Perform the rest of the key processing here. */
}

void main( void )
{
long x;

    /* Create then start the one-shot timer that is responsible for turning
       the back-light off if no keys are pressed within a 5 second period. */
    xBacklightTimer = xTimerCreate
             (
                  /* Just a text name, not used by the RTOS kernel */
                  "BacklightTimer",
                  /* The timer period in ticks. */
                  ( 5000 / portTICK_PERIOD_MS),
                  /* The timer is a one-shot timer. */
                  pdFALSE,
                  /* The id is not used by the callback so can take any value */
                  0,
                  /* The callback function that switches the LCD back-light off */
                  vBacklightTimerCallback
              );

    if( xBacklightTimer == NULL )
    {
        /* The timer was not created. */
    }
    else
    {
        /* Start the timer. No block time is specified, and even if one was it
           would be ignored because the RTOS scheduler has not yet been started */
        if( xTimerStart( xBacklightTimer, 0 ) != pdPASS )
        {
            /* The timer could not be set into the Active state */
        }
    }

    /* ...
       Create tasks here
    ... */

    /* Starting the RTOS scheduler will start the timer running as it has
       already been set into the active state. */
    vTaskStartScheduler();

    /* Should not reach here. */
    for( ;; );
}
```
