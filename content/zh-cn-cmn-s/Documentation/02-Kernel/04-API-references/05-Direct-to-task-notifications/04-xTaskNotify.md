---
title: "xTaskNotify 和 xTaskNotifyIndexed"
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
 BaseType_t xTaskNotify( TaskHandle_t xTaskToNotify,
                         uint32_t ulValue,
                         eNotifyAction eAction );


 BaseType_t xTaskNotifyIndexed( TaskHandle_t xTaskToNotify,
                                UBaseType_t uxIndexToNotify,
                                uint32_t ulValue,
                                eNotifyAction eAction );
```

[如果使用 RTOS 任务通知来实现二进制或计数信号量行为，
则应使用更简单的 [xTaskNotifyGive()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) API 函数，而不是 xTaskNotify()]

每项任务都有一个“任务通知”数组（或简称“通知”），每条通知都包含一个状态和
一个 32 位的值。[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)是直接发送给任务的事件，
可以解除接收任务的阻塞状态，还可以通过多种不同的方式
更新接收任务的某个通知值。例如，通知可覆盖接收任务的某个通知值，
或仅设置接收任务某个通知值中的一个或多个位。

xTaskNotify() 用于直接向 RTOS 任务发送事件，并且可能解除该任务的阻塞状态，
同时还可以按照以下任一方式更新接收任务的某个通知值：

* 将一个 32 位数字写入通知值
* 将通知值加一（递增）
* 设置通知值中的一个或多个位
* 保持通知值不变

xTaskNotify() 和 xTaskNotifyIndexed() 是等效函数，唯一区别在于 xTaskNotifyIndexed()
可以操作数组中的任何任务通知，而 xTaskNotify() 总是操作
数组中索引为 0 的任务通知。

不得从中断服务程序 (ISR) 调用此函数。
请使用 [xTaskNotifyFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/07-xTaskNotifyFromISR) 代替。

必须在 FreeRTOSConfig.h 中将 [configUSE_TASK_NOTIFICATIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_task_notifications) 设置为 1
（或保留为未定义状态），才可使用这些函数。常量
[configTASK_NOTIFICATION_ARRAY_ENTRIES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries) 决定了
每项任务的任务通知数组中的索引数。


**向后兼容性信息：**

在 FreeRTOS V10.4.0 之前，每项任务只有一个“通知值”，
所有任务通知 API 函数都只能操作这一个值。用通知值数组组
替代单个通知值需要
一组新的 API 函数，以处理数组中的特定通知。
xTaskNotify() 是原始 API 函数，
为保持向后兼容，
始终操作数组中索引为 0 的通知值。调用 xTaskNotify() 相当于调用 xTaskNotifyIndexed()，
其 uxIndexToNotify 参数设置为 0。


**参数：**

* *xTaskToNotify*

  接收通知的 RTOS 任务（即*目标*任务）的句柄。可通过以下方法获取任务句柄：
  使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务，并通过 pxCreatedTask 参数获取句柄；
  使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，并存储返回值作为句柄；
  调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)，通过任务名称获取句柄。当前正在执行的 RTOS 任务的句柄
  由 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数返回。

* *uxIndexToNotify*

  目标任务的通知值数组中要向其发送通知的索引。uxIndexToNotify
  必须小于 configTASK_NOTIFICATION_ARRAY_ENTRIES。xTaskNotify() 没有此参数，
  并且总是将通知发送到索引 0。

* *ulValue*

  用于更新目标任务的通知值。请参阅下文 eAction 参数的说明。

* *eAction*

  一种枚举类型，可以取下列任一值，以执行相关操作。

  + eNoAction

    目标任务接收事件，但其通知值不会更新。在这种情况下，
    不会使用 ulValue。

  + eSetBits

    目标任务的通知值将与 ulValue 进行按位“或”操作。例如，如果 ulValue
    设置为 0x01，则目标任务通知值中的第 0 位将被设置。同样，如果 ulValue
    设置为 0x04，则目标任务通知值中的第 2 位将被设置。通过这种方式，RTOS 任务
    通知机制可以作为
    [事件组](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)的轻量级替代方案。

  + eIncrement

    目标任务的通知值将增加 1，这样调用 xTaskNotify()
    相当于调用 [xTaskNotifyGive()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive)。在这种情况下，不会使用 ulValue。

  + eSetValueWithOverwrite

    目标任务的通知值无条件设置为 ulValue。通过这种方式，RTOS 任务
    通知机制可以作为 [xQueueOverwrite()](/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite) 的轻量级替代方案。

  + eSetValueWithoutOrwrite

    如果目标任务当前没有挂起的通知，则其通知值将设置为 ulValue。

    如果目标任务已有挂起的通知，则其通知值不会更新，
    以免之前的值在使用前被覆盖。在这种情况下，调用 xTaskNotify() 会失败，
    返回 pdFALSE。

    通过这种方式，RTOS 任务通知机制可以
    在长度为 1 的队列上作为 [xQueueSend()](/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend) 的轻量级替代方案。


**返回：**

除了 eAction 设置为 eSetValueWithoutOverwrite 且目标任务的通知值无法更新（因为目标任务已有挂起的通知）时，
其他情况下均返回 pdPASS。


**用法示例：**

[更多示例请参阅 [RTOS 任务通知主页面](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* Set bit 8 in the 0th notification value of the task referenced by
   xTask1Handle. */
xTaskNotifyIndexed( xTask1Handle, 0, ( 1UL << 8UL ), eSetBits );

/* Send a notification to the task referenced by xTask2Handle, potentially
   removing the task from the Blocked state, but without updating the task's
   notification value. */
xTaskNotify( xTask2Handle, 0, eNoAction );

/* Set the notification value of the task referenced by xTask3Handle to 0x50,
   even if the task had not read its previous notification value. */
xTaskNotify( xTask3Handle, 0x50, eSetValueWithOverwrite );

/* Set the notification value of the task referenced by xTask4Handle to 0xfff,
   but only if to do so would not overwrite the task's existing notification
   value before the task had obtained it (by a call to [xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait)
   or [ulTaskNotifyTake()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake)). */
if( xTaskNotify( xTask4Handle, 0xfff, eSetValueWithoutOverwrite ) == pdPASS )
{
    /* The task's notification value was updated. */
}
else
{
    /* The task's notification value was not updated. */
}
```
