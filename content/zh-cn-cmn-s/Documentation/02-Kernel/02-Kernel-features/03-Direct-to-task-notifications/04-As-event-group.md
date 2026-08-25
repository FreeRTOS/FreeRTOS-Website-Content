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
  - title: 用作轻量级计数信号量
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore/
  - title: 用作邮箱
    link: /Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/05-As-mailbox/
---


用作轻量级事件组

[事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)是一组二进制标志（或位） ，
应用程序编写者可以对其中的每一个指定含义。RTOS 任务可以
进入“阻塞”状态以等待组内的一个或多个标志激活。待验证的 RTOS
任务处于“阻塞”状态时不会占用任何 CPU 时间。

当使用任务通知代替事件组时，使用接收任务的
[通知值](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)代替事件组，接收任务通知值中的位被用作
事件标志， [xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait)
API 函数被用于代替事件组的 xEventGroupWaitBits () API 函数。

同样，使用 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) 和 [xTaskNotifyFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/07-xTaskNotifyFromISR)
API 函数（其 eAction 参数设置为 eSetBits）分别代替 xEventGroupSetBits()
和 xEventGroupSetBitsFromISR() 函数来设置位。

与 xEventGroupSetBitsFromISR() 相比，xTaskNotifyFromISR() 具有**显著的性能优势**，
这是因为 xTaskNotifyFromISR () 完全在 ISR 中执行，而 xEventGroupSetBitsFromISR() 必须
将某些处理推迟到 RTOS 守护程序任务。

与使用事件组时的情况不同的是，接收任务无法指定它
它只想在位组合同时处于活动状态时解除阻塞状态。相反，任务在任何位变为活动状态时结束阻塞，并且必须
测试位组合本身。

请参阅下方示例：

```c
/* This example demonstrates a single RTOS task being used to process
   events that originate from two separate interrupt service routines -
   a transmit interrupt and a receive interrupt. Many peripherals will
   use the same handler for both, in which case the peripheral's
   interrupt status register can simply be bitwise ORed with the
   receiving task's notification value.

   First, bits are defined to represent each interrupt source. */
#define TX_BIT    0x01
#define RX_BIT    0x02

/* The handle of the task that will receive notifications from the
   interrupts. The handle was obtained when the task was created. */
static TaskHandle_t xHandlingTask;

/*-----------------------------------------------------------*/

/* The implementation of the transmit interrupt service routine. */
void vTxISR( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

   /* Clear the interrupt source. */
   prvClearInterrupt();

   /* Notify the task that the transmission is complete by setting the TX_BIT
      in the task's notification value. */
   xTaskNotifyFromISR( xHandlingTask,
                       TX_BIT,
                       eSetBits,
                       &xHigherPriorityTaskWoken );

   /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context switch
      should be performed to ensure the interrupt returns directly to the highest
      priority task. The macro used for this purpose is dependent on the port in
      use and may be called portEND_SWITCHING_ISR(). */
   portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* The implementation of the receive interrupt service routine is identical
   except for the bit that gets set in the receiving task's notification value. */
void vRxISR( void )
{
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

   /* Clear the interrupt source. */
   prvClearInterrupt();

   /* Notify the task that the reception is complete by setting the RX_BIT
      in the task's notification value. */
   xTaskNotifyFromISR( xHandlingTask,
                       RX_BIT,
                       eSetBits,
                       &xHigherPriorityTaskWoken );

   /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context switch
      should be performed to ensure the interrupt returns directly to the highest
      priority task. The macro used for this purpose is dependent on the port in
      use and may be called portEND_SWITCHING_ISR(). */
   portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
/*-----------------------------------------------------------*/

/* The implementation of the task that is notified by the interrupt service
   routines. */
static void prvHandlingTask( void *pvParameter )
{
const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 500 );
BaseType_t xResult;

   for( ;; )
   {
      /* Wait to be notified of an interrupt. */
      xResult = xTaskNotifyWait( pdFALSE,          /* Don't clear bits on entry. */
                                 ULONG_MAX,        /* Clear all bits on exit. */
                                 &ulNotifiedValue, /* Stores the notified value. */
                                 xMaxBlockTime );

      if( xResult == pdPASS )
      {
         /* A notification was received. See which bits were set. */
         if( ( ulNotifiedValue & TX_BIT ) != 0 )
         {
            /* The TX ISR has set a bit. */
            prvProcessTx();
         }

         if( ( ulNotifiedValue & RX_BIT ) != 0 )
         {
            /* The RX ISR has set a bit. */
            prvProcessRx();
         }
      }
      else
      {
         /* Did not receive a notification within the expected time. */
         prvCheckForErrors();
      }
   }
}
```

