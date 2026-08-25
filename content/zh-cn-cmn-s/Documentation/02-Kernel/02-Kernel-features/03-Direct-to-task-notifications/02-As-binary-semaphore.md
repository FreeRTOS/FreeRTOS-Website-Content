---
title: "RTOS 任务通知"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 队列
relatedLinks:
  - title: API 引用 — 信号量与互斥锁
    link: /Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores/
  - title: RTOS 任务通知
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications/
  - title: 用作轻量级计数信号量
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore/
  - title: 用作轻量级事件组
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/04-As-event-group/
  - title: 用作邮箱
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/05-As-mailbox/
---

用作轻量级二进制信号量

与通过二进制信号量解除任务阻塞状态不同，通过直接通知解除 RTOS 任务阻塞状态的速度**提高 45%**，
而且**使用的 RAM 减少**。本页
演示了如何实现这一点。

二进制信号量是一种最大计数为 1 的信号量，因此称为“二进制”。
只有在信号量可用的情况下，任务才能“获取”信号量，
而只有在其计数为 1 的情况下，信号量才可用。

当使用任务通知代替二进制信号量时，接收任务的
[通知值](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)会用于替代二进制信号量的计数值，
而且 [ulTaskNotifyTake()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake)（或 ulTaskNotifyTakeIndexed()）API 函数
会用于代替信号量的 xSemaphoreTake() API 函数。ulTaskNotifyTake() 函数的
xClearOnExit 参数设置为 pdTRUE，这样每次获取通知时计数值均归零
——模拟二进制信号量。

同样，[xTaskNotifyGive()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive)（或 xTaskNotifyGiveIndexed()）
或者 [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)（或 vTaskNotifyGiveIndexedFromISR()）函数用于代替信号量的
xSemaphoreGive() 和 xSemaphoreGiveFromISR() 函数。

请参阅以下示例。

```c
/* This is an example of a transmit function in a generic
   peripheral driver. An RTOS task calls the transmit function,
   then waits in the Blocked state (so not using an CPU time)
   until it is notified that the transmission is complete. The
   transmission is performed by a DMA, and the DMA end interrupt
   is used to notify the task. */

/* Stores the handle of the task that will be notified when the
   transmission is complete. */
static TaskHandle_t xTaskToNotify = NULL;

/* The index within the target task's array of task notifications
   to use. */
const UBaseType_t xArrayIndex = 1;

/* The peripheral driver's transmit function. */
void StartTransmission( uint8_t *pcData, size_t xDataLength )
{
    /* At this point xTaskToNotify should be NULL as no transmission
       is in progress. A mutex can be used to guard access to the
       peripheral if necessary. */
    configASSERT( xTaskToNotify == NULL );

    /* Store the handle of the calling task. */
    xTaskToNotify = xTaskGetCurrentTaskHandle();

    /* Start the transmission - an interrupt is generated when the
       transmission is complete. */
    vStartTransmit( pcData, xDatalength );
}
/*-----------------------------------------------------------*/

/* The transmit end interrupt. */
void vTransmitEndISR( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* At this point xTaskToNotify should not be NULL as
       a transmission was in progress. */
    configASSERT( xTaskToNotify != NULL );

    /* Notify the task that the transmission is complete. */
    vTaskNotifyGiveIndexedFromISR( xTaskToNotify,
                                   xArrayIndex,
                                   &xHigherPriorityTaskWoken );

    /* There are no transmissions in progress, so no tasks
       to notify. */
    xTaskToNotify = NULL;

    /* If xHigherPriorityTaskWoken is now set to pdTRUE then a
       context switch should be performed to ensure the interrupt
       returns directly to the highest priority task. The macro used
       for this purpose is dependent on the port in use and may be
       called portEND_SWITCHING_ISR(). */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* The task that initiates the transmission, then enters the
   Blocked state (so not consuming any CPU time) to wait for it
   to complete. */
void vAFunctionCalledFromATask( uint8_t ucDataToTransmit,
                                size_t xDataLength )
{
uint32_t ulNotificationValue;
const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 200 );

    /* Start the transmission by calling the function shown above. */
    StartTransmission( ucDataToTransmit, xDataLength );

    /* Wait to be notified that the transmission is complete. Note
       the first parameter is pdTRUE, which has the effect of clearing
       the task's notification value back to 0, making the notification
       value act like a binary (rather than a counting) semaphore. */
    ulNotificationValue = ulTaskNotifyTakeIndexed( xArrayIndex,
                                                   pdTRUE,
                                                   xMaxBlockTime );

    if( ulNotificationValue == 1 )
    {
        /* The transmission ended as expected. */
    }
    else
    {
        /* The call to ulTaskNotifyTake() timed out. */
    }
}
```
