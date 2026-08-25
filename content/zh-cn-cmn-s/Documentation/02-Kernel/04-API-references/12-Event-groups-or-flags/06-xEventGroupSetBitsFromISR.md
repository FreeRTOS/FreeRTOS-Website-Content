---
title: xEventGroupSetBitsFromISR()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[事件组 API](00-Event-groups)]


event_groups.h

```c
BaseType_t xEventGroupSetBitsFromISR(
                         EventGroupHandle_t xEventGroup,
                         const EventBits_t uxBitsToSet,
                         BaseType_t *pxHigherPriorityTaskWoken );
```

在 RTOS [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)中设置位（标志）。
可以从中断服务程序 (ISR) 调用的 [xEventGroupSetBits()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/05-xEventGroupSetBits) 版本
。

在事件组中设置位将自动解除
所有等待位的任务的阻塞状态。

在事件组中设置位不是确定性操作，因为
可能有未知数量的任务正在等待设置一个或多个位。
FreeRTOS 不允许在中断或临界区
中执行不确定的操作。因此，`xEventGroupSetBitFromISR()`
会向 RTOS 守护进程任务发送一条消息，
从而在守护进程任务的上下文中执行设置操作，其中使用的是调度器锁
而非临界区。

**注意：**如上文所述，从中断服务程序中设置位
会将设置操作推迟到 RTOS 守护进程任务（也叫定时器服务任务）
。RTOS 守护进程任务
与其他RTOS任务一样， 都是根据优先级进行调度的。因此，如果置位操作必须立即完成
（在应用程序创建的任务执行之前），
那么RTOS守护进程任务的优先级必须要高于
其他使用事件组的任务。RTOS 守护进程任务的优先级由
[configTIMER_TASK_PRIORITY](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/03-Timer-daemon-configuration)
定义设置（该定义位于 FreeRTOSConfig.h 中）。

在FreeRTOSConfig.h 的 `xEventGroupSetBitsFromISR()` 函数中，
`configUSE_TIMERS` 和 `INCLUDE_xTimerPendFunctionCall` 必须设置为1。

必须将 RTOS 源文件 FreeRTOS/source/event_groups.c
包含在构建中，`xEventGroupSetBitsFromISR()` 函数才可用。


**参数：**

- *xEventGroup*

  要设置位的事件组。必须事先通过调用
  [xEventGroupCreate()](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/01-xEventGroupCreate) 创建事件组。

- *uxBitsToSet*

  指定要设置的一个或多个位的按位值。例如，将 `uxBitsToSe`
  设置为 0x08，则只设置第 3 位。将 `uxBitsToSet` 设置为 0x09，即可设置第 3 位和第 0 位。

- *pxHigherPriorityTaskWoken*

  如上所述，调用该函数将导致向 RTOS 守护进程任务发送一条消息。
  如果守护进程任务的优先级高于当前运行任务
  （被中断的任务）的优先级，那么 `*pxHigherPriorityTaskWoken` 将被设置为 `pdTRUE`
  （被 `xEventGroupSetBitsFromISR()` 设置），表示应在中断退出前请求上下文切换
  。因此，`*pxHigherPriorityTaskWoken` 必须初始化为 `pdFALSE`。请参阅
  下面的示例代码。


**返回：**

- 如果消息已发送到 RTOS 守护进程任务，则返回 pdPASS，否则返回 `pdFAIL`。
  如果[定时器服务队列](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)已满，则返回 `pdFAIL`
  。


**用法示例：**

```c
#define BIT_0    ( 1 << 0 )
#define BIT_4    ( 1 << 4 )

/* An event group which it is assumed has already been created by a call to
   xEventGroupCreate(). */
EventGroupHandle_t xEventGroup;

void anInterruptHandler( void )
{
    BaseType_t xHigherPriorityTaskWoken, xResult;

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Set bit 0 and bit 4 in xEventGroup. */
    xResult = xEventGroupSetBitsFromISR(
                                xEventGroup,   /* The event group being updated. */
                                BIT_0 | BIT_4, /* The bits being set. */
                                &xHigherPriorityTaskWoken );

    /* Was the message posted successfully? */
    if( xResult != pdFAIL )
    {
        /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context
           switch should be requested. The macro used is port specific and will
           be either portYIELD_FROM_ISR() or portEND_SWITCHING_ISR() - refer to
           the documentation page for the port being used. */
        portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
    }
}
```
