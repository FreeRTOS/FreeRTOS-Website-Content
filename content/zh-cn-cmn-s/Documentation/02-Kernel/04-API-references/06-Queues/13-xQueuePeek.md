---
title: xQueuePeek
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[队列管理 ](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h 

```c
 BaseType_t xQueuePeek(
 QueueHandle_t xQueue,
 void *pvBuffer,
 TickType_t xTicksToWait
 );
```

这是一个调用 xQueueGenericReceive() 函数的宏。

从队列中接收项目，而无须从队列中删除该项目。
项目由副本接收，因此必须提供适当大小的缓冲区
。队列创建时，复制到缓冲区中的字节数已定义
。

成功接收的项目仍在队列中，因此将由下一次调用再次返回
或 xQueueReceive () 调用。

中断服务例程中不得使用此宏。


**参数：**

+ *xQueue* 

  要从中接收项目的队列的句柄。

+ *pvBuffer* 

  指向缓冲区的指针，接收到的项目将被复制到这个缓冲区。它必须至少足够大， 
  才能容纳创建队列时定义的队列项的大小。

+ *xTicksToWait* 

  如果在调用时队列为空， 
  则任务应阻塞等待项目接收的最长时间。时间是以滴答周期为单位定义的，因此如果需要，应使用常量 portTICK_PERIOD_MS 
  转换为实时。<br /> 如果 [INCLUDE_vTaskSuspend](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
  设置为 “1”，则将阻塞时间指定为 portMAX_DELAY 会导致任务 
  无限期地阻塞（没有超时）。


**返回：**

如果从队列中成功接收（窥视）项目，则返回 pdTRUE，否则返回 pdFALSE。


**用法示例：** 

```c
struct AMessage
{
    char ucMessageID;
    char ucData[ 20 ];
} xMessage;

QueueHandle_t xQueue;

// Task to create a queue and post a value.
void vATask( void *pvParameters )
{
struct AMessage *pxMessage;

    // Create a queue capable of containing 10 pointers to AMessage structures.
    // These should be passed by pointer as they contain a lot of data.
    xQueue = xQueueCreate( 10, sizeof( struct AMessage * ) );
    if( xQueue == 0 )
    {
        // Failed to create the queue.
    }

    // ...

    // Send a pointer to a struct AMessage object.  Don't block if the
    // queue is already full.
    pxMessage = & xMessage;
    xQueueSend( xQueue, ( void * ) &pxMessage, ( TickType_t ) 0 );

    // ... Rest of task code.
}

// Task to peek the data from the queue.
void vADifferentTask( void *pvParameters )
{
struct AMessage *pxRxedMessage;

    if( xQueue != 0 )
    {
        // Peek a message on the created queue.  Block for 10 ticks if a
        // message is not immediately available.
        if( xQueuePeek( xQueue, &( pxRxedMessage ), ( TickType_t ) 10 ) )
        {
            // pcRxedMessage now points to the struct AMessage variable posted
            // by vATask, but the item still remains on the queue.
        }
    }

    // ... Rest of task code.
}
```
