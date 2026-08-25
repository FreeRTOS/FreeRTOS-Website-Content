---
title: xQueueSendToFront
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
 BaseType_t xQueueSendToFront( QueueHandle_t xQueue,
 const void * pvItemToQueue,
 TickType_t xTicksToWait );
``` 

此宏用于调用 xQueueGenericSend()。

从队列头部入队一个数据项。数据项通过复制
而非引用入队。不得从中断服务程序
调用此函数。请参阅 xQueueSendToFrontFromISR() 了解
可在 ISR 中使用的替代方法。


**参数：**

+ *xQueue* 

  要向其中添加数据项的队列的句柄。

+ *pvItemToQueue* 

  指向待入队数据项的指针。创建队列时定义了队列将保留的项的大小， 
  因此固定数量的字节将从 pvItemToQueue 复制到 
  队列存储区。

+ *xTicksToWait* 

  如果队列已满， 
  则任务应进入阻塞态等待队列上出现可用空间的最大时间。如果设置为 0，调用将立即返回。 
  时间以滴答周期为单位定义，因此如果需要，应使用常量 portTICK_PERIOD_MS 转换为实时 
  。 

  如果 [INCLUDE_vTaskSuspend](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 设置为 “1” ， 
  则将阻塞时间指定为 portMAX_DELAY 会导致任务无限期地阻塞（没有超时）。 |


**返回：**

如果成功发布项目，返回 pdTRUE，否则返回 errQUEUE_FULL。


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

    /* Create a queue capable of containing 10 pointers to AMessage
       structures. These should be passed by pointer as they contain a lot of
       data. */
    xQueue2 = xQueueCreate( 10, sizeof( struct AMessage * ) );

    /* ... */

    if( xQueue1 != 0 )
    {
        /* Send an unsigned long. Wait for 10 ticks for space to become
           available if necessary. */
        if( xQueueSendToFront( xQueue1,
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
        xQueueSendToFront( xQueue2, ( void * ) &pxMessage, ( TickType_t ) 0 );
    }

	/* ... Rest of task code. */
}
```
  
