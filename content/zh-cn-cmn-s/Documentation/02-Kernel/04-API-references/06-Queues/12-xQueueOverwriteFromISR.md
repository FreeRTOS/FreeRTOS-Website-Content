---
title: xQueueOverwriteFromISR
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[队列管理](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
BaseType_t xQueueOverwrite
(
    QueueHandle_t xQueue,
    const void * pvItemToQueue
    BaseType_t *pxHigherPriorityTaskWoken
);
```

此宏用于调用 xQueueGenericSendFromISR() 函数。

可以用于 ISR 的 [xQueueOverwrite()](/Documentation/02-Kernel/04-API-references/06-Queues/11-xQueueOverwrite) 版本。
xQueueOverwriteFromISR() 与 xQueueSendToBackFromISR() 类似，
但即使队列已满，也会将数据写入队列，覆盖队列中
已经存在的数据。

xQueueOverwriteFromISR() 适用于长度为 1 的队列，
即队列要么为空，要么已满。


**参数：**

+ *xQueue*  

  接收数据的队列的句柄。

+ *pvItemToQueue*  

  指向要放入队列中的项目的指针。队列能够存储的项目的大小 
  在[创建队列](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)时即已定义， 
  因此 pvItemToQueue 中的这些字节将复制到队列存储区中。

+ *pxHigherPriorityTaskWoken*  

  如果发送到队列会导致任务解除阻塞，并且解除阻塞的任务的优先级高于当前正在运行的任务， 
  则 xQueueOverwriteFromISR() 会将 *pxHigherPriorityTaskWoken 设置为 pdTRUE。如果 
  xQueueOverwriteFromISR() 将此值设置为 pdTRUE，则应在中断退出前 
  请求上下文切换。请参阅所使用移植配套文档的“中断服务程序”章节， 
  了解如何执行此操作。

**返回：** 

xQueueOverwriteFromISR() 是调用 xQueueGenericSendFromISR() 的宏，
因此与 xQueueSendToFrontFromISR() 具有
相同的返回值。然而，由于 xQueueOverwriteFromISR() 会在队列已满时仍然写入队列，
因此该宏的返回值只有 pdPASS
。


**用法示例：**

```c
QueueHandle_t xQueue;

void vFunction( void *pvParameters )
{
    /* Create a queue to hold one unsigned long value. It is strongly
       recommended **not** to use xQueueOverwriteFromISR() on queues that can
       contain more than one value, and doing so will trigger an assertion
       if configASSERT() is defined. */
    xQueue = xQueueCreate( 1, sizeof( unsigned long ) );
}

void vAnInterruptHandler( void )
{
/* xHigherPriorityTaskWoken must be set to pdFALSE before it is used. */
BaseType_t xHigherPriorityTaskWoken = pdFALSE;
unsigned long ulVarToSend, ulValReceived;

    /* Write the value 10 to the queue using xQueueOverwriteFromISR(). */
    ulVarToSend = 10;
    xQueueOverwriteFromISR( xQueue, &ulVarToSend, &xHigherPriorityTaskWoken );

    /* The queue is full, but calling xQueueOverwriteFromISR() again will still
       pass because the value held in the queue will be overwritten with the
       new value. */
    ulVarToSend = 100;
    xQueueOverwriteFromISR( xQueue, &ulVarToSend, &xHigherPriorityTaskWoken );

    /* Reading from the queue will now return 100. */

    /* ... */

    if( xHigherPrioritytaskWoken == pdTRUE )
    {
        /* Writing to the queue caused a task to unblock and the unblocked task
           has a priority higher than or equal to the priority of the currently
           executing task (the task this interrupt interrupted). Perform a
           context switch so this interrupt returns directly to the unblocked
           task. */
        portYIELD_FROM_ISR(); /* or portEND_SWITCHING_ISR() depending on the
                                 port.*/
    }
}
```
