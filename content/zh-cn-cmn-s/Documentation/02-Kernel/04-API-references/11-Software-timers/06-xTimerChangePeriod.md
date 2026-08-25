---
title: xTimerChangePeriod
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
 BaseType_t xTimerChangePeriod( TimerHandle_t xTimer,
                                TickType_t xNewPeriod,
                                TickType_t xBlockTime );
```

[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)功能由定时器服务/守护进程任务提供。许多
公共 FreeRTOS 定时器 API 函数通过定时器命令队列
向定时器服务任务发送命令。定时器命令队列是
RTOS 内核本身的私有队列，无法被应用程序代码直接访问
。定时器命令队列的长度由 `configTIMER_QUEUE_LENGTH` 配置常量设置。

`xTimerChangePeriod()` 可以改变先前使用
[xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/) API 函数创建的定时器的周期。

可以调用 `xTimerChangePeriod()` 来更改活动
或休眠状态的定时器的周期。更改休眠定时器的周期也会启动
定时器。

必须将 `configUSE_TIMERS` 配置常量设置为 1，
`xTimerChangePeriod()` 才可用。


**参数：** 

- *xTimer*

  其周期将改变的定时器的句柄。
  
- *xNewPeriod*

  `xTimer` 的新周期。定时器周期是以滴答周期为单位指定的，因此常量 `portTICK_PERIOD_MS` 
  可用来转换以毫秒为单位指定的时间。例如，如果定时器必须在 100 个滴答后过期， 
  则 `xNewPeriod` 应该设置为 100。或者，如果定时器必须在 500 毫秒之后过期， 
  则可以将 `xNewPeriod` 设置为 ( 500 / `portTICK_PERIOD_MS` )，前提是 `configTICK_RATE_HZ` 小于
  或等于 1000。定时器周期必须大于 0。
  
- *xBlockTime*

  指定 
  在 
  调用 `xTimerChangePeriod()` 时队列已满的情况下，调用任务应处于阻塞状态以等待更改周期命令成功发送到定时器命令队列的时间（单位：滴答）。在以下情况下，`xBlockTime` 将被忽略：如果 `xTimerChangePeriod()`  
  在 RTOS 调度器启动之前就被调用。


**返回：** 

- 如果在以下情况下，更改周期命令无法发送至定时器命令队列，则返回 `pdFAIL`：
  经过 `xBlockTime` 个滴答之后。
  
- 如果能将此命令成功发送到定时器命令队列，则返回 `pdPASS`
  命令队列。实际处理命令的时间取决于
  定时器服务/守护进程任务相对于系统中其他任务的优先级
  。 
  
  定时器服务/守护进程任务的优先级由 `configTIMER_TASK_PRIORITY` 配置常量设置。


**用法示例：**

```c
/* This function assumes xTimer has already been created. If the timer
   referenced by xTimer is already active when it is called, then the timer
   is deleted. If the timer referenced by xTimer is not active when it is
   called, then the period of the timer is set to 500ms and the timer is
   started. */
void vAFunction( TimerHandle_t xTimer )
{
    /* or more simply and equivalently
       "if( xTimerIsTimerActive( xTimer ) )" */
    if( xTimerIsTimerActive( xTimer ) != pdFALSE )
    {
        /* xTimer is already active - delete it. */
        xTimerDelete( xTimer );
    }
    else
    {
        /* xTimer is not active, change its period to 500ms. This will also
           cause the timer to start. Block for a maximum of 100 ticks if the
           change period command cannot immediately be sent to the timer
           command queue. */
        if( xTimerChangePeriod( xTimer, 500 / portTICK_PERIOD_MS, 100 )
                                                            == pdPASS )
        {
            /* The command was successfully sent. */
        }
        else
        {
            /* The command could not be sent, even after waiting for 100 ticks
               to pass. Take appropriate action here. */
        }
    }
}
```
