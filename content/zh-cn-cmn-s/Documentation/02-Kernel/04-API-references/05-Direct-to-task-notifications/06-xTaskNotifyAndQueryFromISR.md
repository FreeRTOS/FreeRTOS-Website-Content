---
title: "xTaskNotifyAndQueryFromISR 和 xTaskNotifyAndQueryIndexedFromISR"
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
 BaseType_t xTaskNotifyAndQueryFromISR(
                      TaskHandle_t xTaskToNotify,
                      uint32_t ulValue,
                      eNotifyAction eAction,
                      uint32_t *pulPreviousNotifyValue,
                      BaseType_t *pxHigherPriorityTaskWoken );

 BaseType_t xTaskNotifyAndQueryIndexedFromISR(
                      TaskHandle_t xTaskToNotify,
                      UBaseType_t uxIndexToNotify
                      uint32_t ulValue,
                      eNotifyAction eAction,
                      uint32_t *pulPreviousNotifyValue,
                      BaseType_t *pxHigherPriorityTaskWoken );
```

有关详细信息，请参阅 [RTOS 任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。

xTaskNotifyAndQueryIndexedFromISR() 执行的操作
与 [xTaskNotifyIndexedFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/07-xTaskNotifyFromISR) 相同，另外还可
通过额外的 pulPreviousNotifyValue 参数返回目标任务之前的通知值
（函数被调用时的通知值，而不是函数返回时的通知值）。

xTaskNotifyAndQueryFromISR() 执行的操作与 [xTaskNotifyFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/07-xTaskNotifyFromISR) 相同，
另外还可通过额外的 pulPreviousNotifyValue 参数返回目标任务之前的通知值
（函数被调用时的通知值，而不是函数返回时的通知值）
。


**参数：**

* *xTaskToNotify*

  接收通知的 RTOS 任务（即*目标*任务）的句柄。可通过以下方法获取任务句柄：
  使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务，并通过 pxCreatedTask 参数获取句柄；
  使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，并存储返回值作为句柄；
  调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)，并通过任务名称获取句柄。当前正在执行的 RTOS 任务的句柄
  由 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数返回。

* *uxIndexToNotify*

  目标任务的通知值数组中要向其发送通知的索引。
  uxIndexToNotify 必须小于 configTASK_NOTIFICATION_ARRAY_ENTRIES。

* *ulValue*

  用于更新目标任务的通知值。请参阅下文 eAction 参数的说明。

* *eAction*

  一种枚举类型，可以取下列任一值，以执行相关操作。

* *pulPreviousNotifyValue*

  可用于在 xTaskNotifyAndQueryFromISR() 修改任何位之前传出目标任务的通知值。
  pulPreviousNotifyValue 是可选参数，
  如果不需要，可设置为 NULL。如果不使用 pulPreviousNotifyValue，可以考虑使用 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify)
  替代 xTaskNotifyAndQueryFromISR()。

* *pxHigherPriorityTaskWoken*

  *pxHigherPriorityTaskWoken 必须初始化为 pdFALSE (0)。
  如果发送通知导致任务解除阻塞，并且解除阻塞的任务的优先级高于当前正在运行的任务，
  则 xTaskNotifyAndQueryFromISR() 会将 *pxHigherPriorityTaskWoken 设置为 pdTRUE。如果 xTaskNotifyAndQueryFromISR()
  将此值设置为 pdTRUE，则应在退出中断前请求上下文切换。
  请参阅下方示例。pxHigherPriorityTaskWoken 是可选参数，<br /> 可设置为 NULL。


**eAction 值和相关操作**

+ eNoAction

  目标任务接收事件，<br /> 但其通知值不会更新。在这种情况下，
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

+ eSetValueWithoutOverwrite

  如果目标任务当前没有挂起的通知，则其通知值将设置为
  ulValue。如果目标任务已有挂起的通知，则其通知值不会更新，
  以免之前的值在使用前被覆盖。在这种情况下，
  调用 xTaskNotify() 会失败，返回 pdFALSE。通过这种方式，RTOS 任务通知机制可以
  在长度为 1 的队列上作为 [xQueueSend()](/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend) 的轻量级替代方案。


**返回：**

除了 eAction 设置为 eSetValueWithoutOverwrite 且目标任务的通知值无法更新（因为目标任务已有挂起的通知）时，
其他情况下均返回 pdPASS。


**用法示例：**

```c
void vAnISR( void )
{
/* Must be Initialised to pdFALSE! */
BaseType_t xHigherPriorityTaskWoken = pdFALSE.
uint32_t ulPreviousValue;

    /* Set bit 8 in the 0th notification value of the task referenced
       by xTask1Handle. Store the task's previous 0th notification value
       (before bit 8 is set) in ulPreviousValue. */
    xTaskNotifyAndQueryIndexedFromISR( xTask1Handle,
                                       0,
                                       ( 1UL << 8UL ),
                                       eSetBits,
                                       &ulPreviousValue,
                                       &xHigherPriorityTaskWoken );

    /* The task's previous notification value is saved in
       ulPreviousValue. */

   /* If the task referenced by xTask1Handle was in the Blocked
      state, waiting for the notification, then it will now have been
      moved from the Blocked state to the Ready state. If its priority
      is higher than the priority of the currently executing task (the
      task this interrupt interrupted) then xHigherPriorityTaskWoken will
      have been set to pdTRUE, and passing the variable into a call to
      portYIELD_FROM_ISR() will result in the interrupt returning directly
      to the unblocked task. If xHigherPriorityTaskWoken is still pdFALSE
      then passing it into portYIELD_FROM_ISR() will have no effect. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
