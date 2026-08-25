---
title: "xTaskNotifyAndQuery 和 xTaskNotifyAndQueryIndexed"
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
 BaseType_t xTaskNotifyAndQuery( TaskHandle_t xTaskToNotify,
                                 uint32_t ulValue,
                                 eNotifyAction eAction,
                                 uint32_t *pulPreviousNotifyValue );

 BaseType_t xTaskNotifyAndQueryIndexed( TaskHandle_t xTaskToNotify,
                                        UBaseType_t uxIndexToNotify,
                                        uint32_t ulValue,
                                        eNotifyAction eAction,
                                        uint32_t *pulPreviousNotifyValue );
```

有关详细信息，请参阅 [RTOS 任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。

xTaskNotifyAndQueryIndexed() 执行的操作与 [xTaskNotifyIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) 相同，
另外还可通过额外的 pulPreviousNotifyValue 参数返回目标任务之前的通知值
（函数被调用时的通知值，而不是函数返回时的通知值）
。

xTaskNotifyAndQuery() 执行的操作与 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) 相同，
另外还可通过额外的 pulPreviousNotifyValue 参数返回目标任务之前的通知值
（函数被调用时的通知值，而不是函数返回时的通知值）
。

不得从中断服务程序 (ISR) 调用此函数。
请使用 [xTaskNotifyAndQueryFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/06-xTaskNotifyAndQueryFromISR) 代替。


**参数：**

* *xTaskToNotify*

  接收通知的 RTOS 任务（即*目标*任务）的句柄。可通过以下方法获取任务句柄：
  使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务，并通过 pxCreatedTask 参数获取句柄；
  使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，并存储返回值作为句柄；
  调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)，并通过任务名称获取句柄。当前正在执行的 RTOS 任务的句柄
  由 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数返回。

* *uxIndexToNotify*

  目标任务的通知值数组中要向其发送通知的索引。uxIndexToNotify
  必须小于 configTASK_NOTIFICATION_ARRAY_ENTRIES。

* *ulValue*
  用于更新目标任务的通知值。请参阅下文 eAction 参数的说明。

* *eAction*

  一种枚举类型，可以取下列任一值，以执行相关操作。

* *pulPreviousNotifyValue*

  可用于在 xTaskNotifyAndQuery() 修改任何位之前传出目标任务的通知值。
  pulPreviousNotifyValue 是可选参数，如果不需要，可设置为 NULL。如果不使用 pulPreviousNotifyValue，
  可以考虑使用 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) 替代 xTaskNotifyAndQuery()。


**eAction 值和相关操作**

+ eNoAction

  目标任务接收事件，但其通知值不会更新。在这种情况下，
  不会使用 ulValue。

+ eSetBits

  目标任务的通知值将与 ulValue 进行按位“或”操作。例如，如果 ulValue
  设置为 0x01，则目标任务通知值中的第 0 位将被设置。同样，如果 ulValue
  设置为 0x04，则目标任务通知值中的第 2 位将被设置。通过这种方式，RTOS 任务
  通知机制可以作为[事件组](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)的轻量级替代方案。

+ eIncrement

  目标任务的通知值将增加 1，这样调用 xTaskNotify()
  相当于调用 [xTaskNotifyGive()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive)。在这种情况下，不会使用 ulValue。

+ eSetValueWithOverwrite

  目标任务的通知值无条件设置为 ulValue。通过这种方式，RTOS 任务
  通知机制可以作为 [xQueueOverwrite()](/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite) 的轻量级替代方案。

+ eSetValueWithoutOrwrite

  如果目标任务当前没有挂起的通知，则其通知值
  将设置为 ulValue。如果目标任务已有挂起的通知，则其通知值
  不会更新，以免之前的值在使用前被覆盖。在这种情况下,
  调用 xTaskNotify() 会失败，返回 pdFALSE。通过这种方式，RTOS 任务通知机制可以
  在长度为 1 的队列上作为 [xQueueSend()](/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend) 的轻量级替代方案。


**返回：**

 除了 eAction 设置为 eSetValueWithoutOverwrite
 且目标任务的通知值无法更新（因为目标任务已有挂起的通知）时，
 其他情况下
 均返回 pdPASS。


**用法示例：**

```c
uint32_t ulPreviousValue;

/* Set bit 8 in the 0th notification value of the task referenced
   by xTask1Handle. Store the task's previous 0th notification
   value (before bit 8 is set) in ulPreviousValue. */
xTaskNotifyAndQueryIndexed( xTask1Handle,
                            0,
                            ( 1UL << 8UL ),
                            eSetBits,
                            &ulPreviousValue );

/* Send a notification to the task referenced by xTask2Handle,
   potentially removing the task from the Blocked state, but without
   updating the task's notification value. Store the tasks notification
   value in ulPreviousValue. */
xTaskNotifyAndQuery( xTask2Handle, 0, eNoAction, &ulPreviousValue );

/* Set the notification value of the task referenced by xTask3Handle
   to 0x50, even if the task had not read its previous notification value.
   The task's previous notification value is of no interest so the last
   parameter is set to NULL. */
xTaskNotifyAndQuery( xTask3Handle, 0x50, eSetValueWithOverwrite,  NULL );

/* Set the notification value of the task referenced by xTask4Handle
   to 0xfff, but only if to do so would not overwrite the task's existing
   notification value before the task had obtained it (by a call to
   xTaskNotifyWait()) or ulTaskNotifyTake(). The task's previous
   notification value is saved in ulPreviousValue. */
if( xTaskNotifyAndQuery( xTask4Handle,
                         0xfff,
                         eSetValueWithoutOverwrite,
                         &ulPreviousValue ) == pdPASS )
{
    /* The task's notification value was updated. */
}
else
{
    /* The task's notification value was not updated. */
}
```
