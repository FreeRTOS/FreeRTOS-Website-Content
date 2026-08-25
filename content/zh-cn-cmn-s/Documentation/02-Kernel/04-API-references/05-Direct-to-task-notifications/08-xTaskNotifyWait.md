---
title: "xTaskNotifyWait 和 xTaskNotifyWaitIndexed"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 任务通知 API](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h

```c
 BaseType_t xTaskNotifyWait( uint32_t ulBitsToClearOnEntry,
                             uint32_t ulBitsToClearOnExit,
                             uint32_t *pulNotificationValue,
                             TickType_t xTicksToWait );

 BaseType_t xTaskNotifyWaitIndexed( UBaseType_t uxIndexToWaitOn,
                                    uint32_t ulBitsToClearOnEntry,
                                    uint32_t ulBitsToClearOnExit,
                                    uint32_t *pulNotificationValue,
                                    TickType_t xTicksToWait );
```

[如果使用 RTOS 任务通知来实现二进制或计数信号量行为，
则应使用更简单的 [ulTaskNotifyTake()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) API 函数，而不是 xTaskNotifyWait()]

每项任务都有一个“任务通知”数组（或简称“通知”），
每条通知都包含一个状态和一个 32 位的值。[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)是
直接发送给任务的事件，可以解除接收任务的阻塞状态，
还可以通过多种不同的方式更新接收任务的某个通知值。
例如，通知可覆盖接收任务的某个通知值，或仅设置
接收任务某个通知值中的一个或多个位。

xTaskNotifyWait() 用于使调用任务等待接收通知，可以为其设置一个可选的超时时间。
如果接收 RTOS 任务在等待通知时已经处于阻塞状态，则在等待的通知到达时，
接收 RTOS 任务将解除阻塞状态，通知也将清除。

**注意：**数组中的所有通知均独立操作，即一项任务在同一时间只能在数组中的一条通知上处于阻塞状态，
并且不会被发送到其他数组索引的通知解除阻塞状态。

xTaskNotifyWait() 和 xTaskNotifyWaitIndexed() 是等效宏，唯一区别在于
xTaskNotifyWaitIndexed() 可以操作数组中的任何任务通知，
而 xTaskNotifyWait() 总是操作数组中索引为 0 的任务通知。

xTaskNotifyGive() 不能在中断服务程序中调用。
请使用 [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) 代替。

必须在 FreeRTOSConfig.h 中将 [configUSE_TASK_NOTIFICATIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_task_notifications) 设置为 1
（或保留为未定义状态），才可使用这些宏。常量
[configTASK_NOTIFICATION_ARRAY_ENTRIES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries)
决定了每项任务的任务通知数组中的索引数。


**向后兼容性信息：**

在 FreeRTOS V10.4.0 之前，每项任务只有一个“通知值”，
所有任务通知 API 函数都只能操作这一个值。用通知值数组
替代单个通知值需要
一组新的 API 函数，以处理数组中的特定通知。
xTaskNotifyWait() 是原始 API 函数，
为保持向后兼容，
始终操作数组中索引为 0 的通知值。调用 xTaskNotifyWait() 等同于调用
xTaskNotifyWaitIndexed()，其中 uxIndexToWaitOn 参数设置为 0。


**参数：**

* *uxIndexToWaitOn*

  调用任务的通知值数组中用于等待接收通知的索引。
  uxIndexToWaitOn 必须小于
  configTASK_NOTIFICATION_ARRAY_ENTRIES。xTaskNotifyWait() 没有此参数，
  总是在索引 0 的位置等待通知。

* *ulBitsToClearOnEntry*

  调用 xTaskNotifyWait() 时，如果通知已挂起，则在进入 xTaskNotifyWait() 函数（即任务等待新通知之前）时，ulBitsToClearOnEntry 中设置的任何位都会在调用 RTOS 任务的通知值中
  被清除
  。例如，如果 ulBitsToClearOnEntry 设为 0x01，
  则任务通知值中的第 0 位将在进入函数时被清除。
  如果 ulBitsToClearOnEntry 设为 0xffffffff (ULONG_MAX)
  则将清除任务通知值中的所有位，相当于将值清零。

* *ulBitsToClearOnExit*

  如果在调用 xTaskNotifyWait() 函数时收到了通知，则在 xTaskNotifyWait() 函数退出之前，ulBitsToClearOnExit 中设置的任何位都会在调用 RTOS 任务的通知值中
  被清除。RTOS
  任务的通知值保存到 *pulNotificationValue（见下文对 pulNotificationValue 的介绍）之后，
  这些位即被清除。例如，如果 ulBitsToClearOnExit 设为 0x03，
  则在函数退出之前，任务通知值中的第 0 位和第 1 位将被清除。如果 ulBitsToClearOnExit
  设为 0xffffffff（ULONG_MAX），则将清除任务通知值中的所有位，
  相当于将值清零。

* *pulNotificationValue*

  用于传出 RTOS 任务的通知值。复制到 *pulNotificationValue 的值是
  RTOS 任务的通知值，该值是在应用 ulBitsToClearOnExit 设置清除任何位
  之前的值。如果无需通知值，可以将 pulNotificationValue 设置为 NULL。

* *xTicksToWait*

  调用 xTaskNotifyWait() 时没有挂起通知的情况下，
  在阻塞状态下等待接收通知的最长时间。RTOS 任务在阻塞状态下
  不会消耗 CPU 时间。时间以 RTOS 滴答周期为单位。可以使用 pdMS_TO_TICKS() 宏
  将以毫秒为单位的时间转换为以滴答为单位的时间。


**返回：**

如果收到了通知，或者在调用 xTaskNotifyWait() 时通知已挂起，
则返回 pdTRUE。

如果调用 xTaskNotifyWait() 超时且在超时前没有收到通知，
则返回 pdFALSE。


**用法示例：**

[更多示例请参阅 [RTOS 任务通知主页面](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* This task shows bits within the RTOS task notification value being used to pass
   different events to the task in the same way that flags in an [event group](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups) might
   be used for the same purpose. */
void vAnEventProcessingTask( void *pvParameters )
{
uint32_t ulNotifiedValue;

    for( ;; )
    {
        /* Block indefinitely (without a timeout, so no need to check the function's
           return value) to wait for a notification.

           Bits in this RTOS task's notification value are set by the notifying
           tasks and interrupts to indicate which events have occurred. */

        xTaskNotifyWaitIndexed( 0,         /* Wait for 0th notification. */
                                0x00,      /* Don't clear any notification bits on entry. */
                                ULONG_MAX, /* Reset the notification value to 0 on exit. */
                                &ulNotifiedValue, /* Notified value pass out in
                                                     ulNotifiedValue. */
                                portMAX_DELAY );  /* Block indefinitely. */

        /* Process any events that have been latched in the notified value. */

        if( ( ulNotifiedValue & 0x01 ) != 0 )
        {
            /* Bit 0 was set - process whichever event is represented by bit 0. */
            prvProcessBit0Event();
        }

        if( ( ulNotifiedValue & 0x02 ) != 0 )
        {
            /* Bit 1 was set - process whichever event is represented by bit 1. */
            prvProcessBit1Event();
        }

        if( ( ulNotifiedValue & 0x04 ) != 0 )
        {
            /* Bit 2 was set - process whichever event is represented by bit 2. */
            prvProcessBit2Event();
        }

        /* Etc. */
    }
}
```
