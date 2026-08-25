---
title: "xTaskNotifyFromISR 和 xTaskNotifyIndexedFromISR"
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
 BaseType_t xTaskNotifyFromISR( TaskHandle_t xTaskToNotify,
                                uint32_t ulValue,
                                eNotifyAction eAction,
                                BaseType_t *pxHigherPriorityTaskWoken );

 BaseType_t xTaskNotifyIndexedFromISR( TaskHandle_t xTaskToNotify,
                                       UBaseType_t uxIndexToNotify,
                                       uint32_t ulValue,
                                       eNotifyAction eAction,
                                       BaseType_t *pxHigherPriorityTaskWoken );
```

可在中断服务程序 (ISR) 中使用的 xTaskNotify() 和 xTaskNotifyIndexed() 版本
。请参阅 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) API 函数文档页面，
了解其操作和必要的配置参数，
以及向后兼容性信息。


**参数：**

* *xTaskToNotify*

  接收通知的 RTOS 任务（即*目标*任务）的句柄。  可通过以下方法获取任务句柄：
  使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务，并通过 pxCreatedTask 参数获取句柄；
  使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，并存储返回值作为句柄；
  调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)，通过任务名称获取句柄。当前
  当前正在执行的 RTOS 任务的句柄
  由 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数返回。

* *uxIndexToNotify*

  目标任务的通知值数组中要向其发送通知的索引。
  uxIndexToNotify 必须小于 configTASK_NOTIFICATION_ARRAY_ENTRIES。
  xTaskNotifyFromISR() 没有此参数，并且总是将通知发送到索引 0。

* *ulValue*

  用于更新目标任务的通知值。请参阅下文 eAction 参数的
  说明。

* *eAction*

  一种枚举类型，可以取下列任一值，以执行相关操作。

* *pxHigherPriorityTaskWoken*

  *pxHigherPriorityTaskWoken 必须初始化为 0。
  如果发送通知导致任务解除阻塞，并且解除阻塞的任务的优先级高于当前正在运行的任务，
  则 xTaskNotifyFromISR() 会将 *pxHigherPriorityTaskWoken 设置为 pdTRUE。如果
  xTaskNotifyFromISR() 将此值设置为 pdTRUE，则应在退出中断前
  请求上下文切换。请参阅下方示例。pxHigherPriorityTaskWoken 是可选参数，
  可设置为 NULL。


**eAction 值和相关操作**

+ eNoAction

  目标任务接收事件，但其通知值不会更新。在这种情况下，
  不会使用 ulValue。

+ eSetBits

  目标任务的通知值将与 ulValue 进行按位“或”操作。例如，如果 ulValue
  设置为 0x01，则目标任务通知值中的第 0 位将被设置。同样，如果 ulValue
  设置为 0x04，则目标任务通知值中的第 2 位将被设置。通过这种方式，RTOS 任务
  通知机制可以作为[事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)的轻量级替代方案。

+ eIncrement

  目标任务的通知值将增加 1，这样调用 xTaskNotifyFromISR()
  相当于调用 [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)。在这种情况下，不会使用 ulValue。

+ eSetValueWithOverwrite

  目标任务的通知值无条件设置为 ulValue。通过这种方式，RTOS 任务
  通知机制可以作为 [xQueueOverwrite()](/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite) 的轻量级替代方案。

+ eSetValueWithoutOverwrite

  如果目标任务当前没有挂起的通知，则其通知值
  将设置为 ulValue。  如果目标任务已有挂起的通知，则其通知值
  不会更新，以免之前的值在使用前被覆盖。在这种情况下，
  调用 xTaskNotify() 会失败，返回 pdFALSE。  通过这种方式，RTOS 任务通知机制可以
  在长度为 1 的队列上作为 [xQueueSend()](/Documentation/02-Kernel/04-API-references/06-Queues/03-xQueueSend) 的轻量级替代方案。


**返回：**

除了 eAction 设置为 eSetValueWithoutOverwrite
且目标任务的通知值无法更新（因为目标任务已有挂起的通知）时，
其他情况下
均返回 pdPASS。


**用法示例：**

[更多示例请参阅 [RTOS 任务通知主页面](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

本示例演示了如何结合使用 xTaskNotifyFromISR() 和 eSetBits
操作。请参阅 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) API 文档页面，
查看有关如何使用 eNoAction、eSetValueWithOverwrite 和
eSetValueWithoutOverwrite 的示例。


```c
/* The interrupt handler does not perform any processing itself. Instead it
   it unblocks a high priority task in which the events that generated the
   interrupt are processed. If the priority of the task is high enough then the
   interrupt will return directly to the task (so it will interrupt one task but
   return to a different task), so the processing will occur contiguously in time -
   just as if all the processing had been done in the interrupt handler itself.
   The status of the interrupting peripheral is sent to the task using an RTOS task
   notification. */
void vANInterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken;
uint32_t ulStatusRegister;

    /* Read the interrupt status register which has a bit for each interrupt
       source (for example, maybe an Rx bit, a Tx bit, a buffer overrun bit, etc. */
    ulStatusRegister = ulReadPeripheralInterruptStatus();

    /* Clear the interrupts. */
    vClearPeripheralInterruptStatus( ulStatusRegister );

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE. If calling
       xTaskNotifyFromISR() unblocks the handling task, and the priority of
       the handling task is higher than the priority of the currently running task,
       then xHigherPriorityTaskWoken will automatically get set to pdTRUE. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Unblock the handling task so the task can perform any processing necessitated
       by the interrupt. xHandlingTask is the task's handle, which was obtained
       when the task was created. The handling task's 0th notification value
       is bitwise ORed with the interrupt status - ensuring bits that are already
       set are not overwritten. */
    xTaskNotifyIndexedFromISR( xHandlingTask,
                               0,
                               ulStatusRegister,
                               eSetBits,
                               &xHigherPriorityTaskWoken );

    /* Force a context switch if xHigherPriorityTaskWoken is now set to pdTRUE.
       The macro used to do this is dependent on the port and may be called
       portEND_SWITCHING_ISR. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

/* ----------------------------------------------------------- */


/* A task that blocks waiting to be notified that the peripheral needs servicing,
   processing all the events pending in the peripheral each time it is notified to
   do so. */

void vHandlingTask( void *pvParameters )
{
uint32_t ulInterruptStatus;

    for( ;; )
    {
        /* Block indefinitely (without a timeout, so no need to check the function's
           return value) to wait for a notification. NOTE! Real applications
           should not block indefinitely, but instead time out occasionally in order
           to handle error conditions that may prevent the interrupt from sending
           any more notifications. */
        xTaskNotifyWaitIndexed( 0,                  /* Wait for 0th Notificaition */
                                0x00,               /* Don't clear any bits on entry. */
                                ULONG_MAX,          /* Clear all bits on exit. */
                                &ulInterruptStatus, /* Receives the notification value. */
                                portMAX_DELAY );    /* Block indefinitely. */

        /* Process any bits set in the received notification value. This assumes
           the peripheral sets bit 1 for an Rx interrupt, bit 2 for a Tx interrupt,
           and bit 3 for a buffer overrun interrupt. */
        if( ( ulInterruptStatus & 0x01 ) != 0x00 )
        {
            prvProcessRxInterrupt();
        }

        if( ( ulInterruptStatus & 0x02 ) != 0x00 )
        {
            prvProcessTxInterrupt();
        }

        if( ( ulInterruptStatus & 0x04 ) != 0x00 )
        {
            prvClearBufferOverrun();
        }
    }
}
```
