---
title: "RTOS 任务通知"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 队列
relatedLinks:
  - title: API 引用——信号量与互斥锁
    link: /Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores/
  - title: RTOS 任务通知
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications/
  - title: 用作二进制信号量
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore/
  - title: 用作轻量级事件组
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group/
  - title: 用作邮箱
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/05-As-mailbox/
---

用作轻量级计数信号量

与通过信号量解除任务阻塞状态不同，通过直接通知解除 RTOS 任务阻塞状态的**速度提高 45%**，而且**使用的 RAM**
更少。本页演示如何完成这一操作。

计数信号量指的是计数值范围从 0 到信号量创建时所设最高值
的一种信号量。只有在信号量可用的情况下，任务才能“获取”信号量，
而只有在计数大于零的情况下，信号量才可用。

当使用任务通知代替计数信号量时，接收任务的
 [通知值](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)会用于替代计数信号量的计数值，
而且 [ulTaskNotifyTake()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake)（或 ulTaskNotifyTakeIndexed()）API 函数会用于
代替信号量的 xSemaphoreTake() API 函数。ulTaskNotifyTake() 函数的 xClearOnExit 参数
设置为 pdFALSE，因此每次接收通知时，计数值只会递减（而不是清除），
模拟计数信号量。

同样，[xTaskNotifyGive()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive)（或 xTaskNotifyGiveIndexed()）
或者 [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)（或 vTaskNotifyGiveIndexedFromISR()）函数用于代替信号量的
xSemaphoreGive() 和 xSemaphoreGiveFromISR() 函数。

下面的第一个示例使用接收任务的通知值作为计数
信号量。第二个示例提供了更加实用和有效的实现。

**示例 1：**

```c
/* An interrupt handler that does not process interrupts directly,
   but instead defers processing to a high priority RTOS task. The
   ISR uses RTOS task notifications to both unblock the RTOS task
   and increment the RTOS task's notification value. */
void vANInterruptHandler( void )
{
BaseType_t xHigherPriorityTaskWoken;

    /* Clear the interrupt. */
    prvClearInterruptSource();

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE.
       If calling vTaskNotifyGiveFromISR() unblocks the handling
       task, and the priority of the handling task is higher than
       the priority of the currently running task, then
       xHigherPriorityTaskWoken will be automatically set to pdTRUE. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Unblock the handling task so the task can perform
       any processing necessitated by the interrupt. xHandlingTask
       is the task's handle, which was obtained when the task was
       created. vTaskNotifyGiveFromISR() also increments
       the receiving task's notification value. */
    vTaskNotifyGiveFromISR( xHandlingTask, &xHigherPriorityTaskWoken );

    /* Force a context switch if xHigherPriorityTaskWoken is now
       set to pdTRUE. The macro used to do this is dependent on
       the port and may be called portEND_SWITCHING_ISR. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* A task that blocks waiting to be notified that the peripheral
   needs servicing. */
void vHandlingTask( void *pvParameters )
{
BaseType_t xEvent;
const TickType_t xBlockTime = pdMS_TO_TICKS( 500 );
uint32_t ulNotifiedValue;

    for( ;; )
    {
        /* Block to wait for a notification. Here the RTOS
           task notification is being used as a counting semaphore.
           The task's notification value is incremented each time
           the ISR calls vTaskNotifyGiveFromISR(), and decremented
           each time the RTOS task calls ulTaskNotifyTake() - so in
           effect holds a count of the number of outstanding interrupts.
           The first parameter is set to pdFALSE, so the notification
           value is only decremented and not cleared to zero, and one
           deferred interrupt event is processed at a time. See
           example 2 below for a more pragmatic approach. */
        ulNotifiedValue = ulTaskNotifyTake( pdFALSE,
                                            xBlockTime );

        if( ulNotifiedValue > 0 )
        {
            /* Perform any processing necessitated by the interrupt. */
            xEvent = xQueryPeripheral();

            if( xEvent != NO_MORE_EVENTS )
            {
                vProcessPeripheralEvent( xEvent );
            }
        }
        else
        {
            /* Did not receive a notification within the expected
               time. */
            vCheckForErrorConditions();
        }
    }
}
```

**示例 2：**

此示例显示了
RTOS 任务更实用、更有效的实现。在此实现中，从 ulTaskNotifyTake() 返回的值
用于了解必须处理多少未完成的 ISR 事件，从而
允许在每次调用 ulTaskNotifyTake() 时将RTOS 任务的通知计数
清零。假设中断服务程序 (ISR) 如
上面的示例 1 所示。

```c
/* The index within the target task's array of task notifications
   to use. */
const UBaseType_t xArrayIndex = 0;

/* A task that blocks waiting to be notified that the peripheral
   needs servicing. */
void vHandlingTask( void *pvParameters )
{
BaseType_t xEvent;
const TickType_t xBlockTime = pdMS_TO_TICKS( 500 );
uint32_t ulNotifiedValue;

    for( ;; )
    {
        /* As before, block to wait for a notification form the ISR.
           This time however the first parameter is set to pdTRUE,
           clearing the task's notification value to 0, meaning each
           outstanding outstanding deferred interrupt event must be
           processed before ulTaskNotifyTake() is called again. */
        ulNotifiedValue = ulTaskNotifyTakeIndexed( xArrayIndex,
                                                   pdTRUE,
                                                   xBlockTime );

        if( ulNotifiedValue == 0 )
        {
            /* Did not receive a notification within the expected
               time. */
            vCheckForErrorConditions();
        }
        else
        {
            /* ulNotifiedValue holds a count of the number of
               outstanding interrupts. Process each in turn. */
            while( ulNotifiedValue > 0 )
            {
                xEvent = xQueryPeripheral();

                if( xEvent != NO_MORE_EVENTS )
                {
                    vProcessPeripheralEvent( xEvent );
                    ulNotifiedValue--;
                }
                else
                {
                    break;
                }
            }
        }
    }
}
```
