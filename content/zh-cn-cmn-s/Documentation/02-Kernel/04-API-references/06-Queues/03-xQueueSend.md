---
title: xQueueSend
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
 BaseType_t xQueueSend(
                        QueueHandle_t xQueue,
                        const void * pvItemToQueue,
                        TickType_t xTicksToWait
                      );
```

此宏用于调用 `xQueueGenericSend()` 函数。之所以包含此宏，是为了 
向后兼容那些未提供 `xQueueSendToFront()` 和 `xQueueSendToBack()` 宏的 FreeRTOS 版本。其功能
等同于 `xQueueSendToBack()`。

在队列中发布项目。项目通过复制而非引用的方式入队。不得从中断服务程序中调用 
此函数。请参阅 `xQueueSendFromISR()`，这是一个可在 ISR 中使用的替代函数。


**参数：**

- *xQueue*

  要向其中发布项目的队列的句柄。

- *pvItemToQueue*

  指向要放入队列中的项目的指针。队列能够存储的项目的大小在创建队列时即已定义， 
  因此 `pvItemToQueue`中的这些字节将复制到 
  队列存储区中。

- *xTicksToWait*

  队列已满的情况下，任务处于阻塞状态且愿意等待队列中出现可用空间的 
  最长时间。如果队列已满且 `xTicksToWait` 设置为 0， 
  则调用将立即返回。时间以滴答周期为单位定义，如果需要转换为实际时间，可以使用 `portTICK_PERIOD_MS` 常量 
  。 

  如果 [INCLUDE_vTaskSuspend](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 设置为 1，则将阻塞时间指定为 `portMAX_DELAY` 
  会导致任务无限期地阻塞（没有超时限制）。


**返回：**

- 如果成功发布项目，返回 *pdTRUE*， 
- 否则返回 *errQUEUE_FULL*。


**用法示例：**

```c
struct AMessage
 {
    char ucMessageID;
    char ucData[ 20 ];
 } xMessage;

 unsigned long ulVar = 10UL;

 void vATask( void *pvParameters )
 {
 QueueHandle_t xQueue1, xQueue2;
 struct AMessage *pxMessage;

    /* Create a queue capable of containing 10 unsigned long values. */
    xQueue1 = xQueueCreate( 10, sizeof( unsigned long ) );

    /* Create a queue capable of containing 10 pointers to AMessage structures.
       These should be passed by pointer as they contain a lot of data. */
    xQueue2 = xQueueCreate( 10, sizeof( struct AMessage * ) );

    /* ... */

    if( xQueue1 != 0 )
    {
        /* Send an unsigned long. Wait for 10 ticks for space to become
           available if necessary. */
        if( xQueueSend( xQueue1,
                       ( void * ) &ulVar,
                       ( TickType_t ) 10 ) != pdPASS )
        {
            /* Failed to post the message, even after 10 ticks. */
        }
    }

    if( xQueue2 != 0 )
    {
        /* Send a pointer to a struct AMessage object. Don't block if the
           queue is already full. */
        pxMessage = & xMessage;
        xQueueSend( xQueue2, ( void * ) &pxMessage, ( TickType_t ) 0 );
    }

	/* ... Rest of task code. */
 }
```
